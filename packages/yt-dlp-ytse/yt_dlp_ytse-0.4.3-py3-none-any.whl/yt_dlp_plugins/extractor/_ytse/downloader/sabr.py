import collections
import itertools
from yt_dlp.downloader import FileDownloader

try:
    from yt_dlp.extractor.youtube._base import INNERTUBE_CLIENTS
except ImportError:
    from yt_dlp.extractor.youtube import INNERTUBE_CLIENTS

from yt_dlp.utils import traverse_obj, int_or_none, DownloadError
from yt_dlp.utils._utils import _YDLLogger
from yt_dlp.utils.progress import ProgressCalculator

from ..protos import (
    FormatId,
    ClientInfo
)
from ..sabr import SABRStream, FormatRequest, SABRStatus, FormatType


class SABRFDWriter:
    def __init__(self, fd, filename, infodict, progress_idx=0):
        self.fd = fd
        self.fp = None
        self.filename = filename
        self._tmp_filename = None
        self._open_mode = 'wb'
        self._progress = None
        self.info_dict = infodict
        self._downloaded_bytes = 0
        self.progress_idx = progress_idx
        self._state = {}

    def _open(self):
        self._tmp_filename = self.fd.temp_name(self.filename)
        try:
            self.fp, self._tmp_filename = self.fd.sanitize_open(self._tmp_filename, self._open_mode)
            assert self.fp is not None
            self.filename = self.fd.undo_temp_name(self._tmp_filename)
            self.fd.report_destination(self.filename)
        except OSError as err:
            raise DownloadError(f'unable to open for writing: {err}')

    def write(self, data: bytes, metadata: SABRStatus):
        if not self._progress:
            self._progress = ProgressCalculator(metadata.start_bytes)

        if not self.fp:
            self._open()
        if self.fp.closed:
            raise ValueError('File is closed')
        self.fp.write(data)

        self._downloaded_bytes += len(data)
        self._progress.total = self.info_dict.get('filesize')
        self._progress.update(self._downloaded_bytes)
        self._state = {
            'status': 'downloading',
            'downloaded_bytes': self._downloaded_bytes,
            'total_bytes': self.info_dict.get('filesize'),
            'tmpfilename': self._tmp_filename,
            'filename': self.filename,
            'eta': self._progress.eta.smooth,
            'speed': self._progress.speed.smooth,
            'elapsed': self._progress.elapsed,
            'progress_idx': self.progress_idx,
            'fragment_count': metadata.fragment_count,
            'fragment_index': metadata.fragment_index,
        }
        self.fd._hook_progress(self._state, self.info_dict)

    def finish(self):
        self._state['status'] = 'finished'
        self.fd._hook_progress(self._state, self.info_dict)
        if self.fp:
            self.fp.close()
            self.fd.try_rename(self._tmp_filename, self.filename)


class SABRFD(FileDownloader):

    @classmethod
    def can_download(cls, info_dict):
        return (
            info_dict.get('requested_formats') and
            all(format_info.get('protocol') == 'sabr' for format_info in info_dict['requested_formats'])
        )

    def real_download(self, filename, info_dict):
        requested_formats = info_dict.get('requested_formats') or [info_dict]
        sabr_format_groups = collections.defaultdict(dict, {})

        for idx, f in enumerate(requested_formats):
            sabr_config = f.get('_sabr_config')
            client_name = sabr_config.get('client_name')
            server_abr_streaming_url = f.get('url')
            video_playback_ustreamer_config = sabr_config.get('video_playback_ustreamer_config')

            if not video_playback_ustreamer_config:
                self.report_error('Video playback ustreamer config not found')
                return

            sabr_format_group_config = sabr_format_groups.get(client_name)

            if not sabr_format_group_config:
                po_token = sabr_config.get('po_token')
                innertube_client = INNERTUBE_CLIENTS.get(client_name)
                sabr_format_group_config = sabr_format_groups[client_name] = {
                    'server_abr_streaming_url': server_abr_streaming_url,
                    'video_playback_ustreamer_config': video_playback_ustreamer_config,
                    'formats': [],
                    'po_token_fn': lambda: po_token,
                    'reload_config_fn': sabr_config.get('reload_config_fn'),
                    # todo: pass this information down from YoutubeIE
                    'client_info': ClientInfo(
                        client_name=innertube_client['INNERTUBE_CONTEXT_CLIENT_NAME'],
                        client_version=traverse_obj(innertube_client, ('INNERTUBE_CONTEXT', 'client', 'clientVersion')),
                        os_version=traverse_obj(innertube_client, ('INNERTUBE_CONTEXT', 'client', 'osVersion')),
                        os_name=traverse_obj(innertube_client, ('INNERTUBE_CONTEXT', 'client', 'osName')),
                        device_model=traverse_obj(innertube_client, ('INNERTUBE_CONTEXT', 'client', 'deviceModel')),
                        device_make=traverse_obj(innertube_client, ('INNERTUBE_CONTEXT', 'client', 'deviceMake')),
                    ),
                    'writers': [],
                    # Number.MAX_SAFE_INTEGER
                    'start_time_ms': ((2**53) - 1) if info_dict.get('live_status') == 'is_live' and not f.get('is_from_start') else 0,
                }

            else:
                if sabr_format_group_config['server_abr_streaming_url'] != server_abr_streaming_url:
                    self.report_error('Server ABR streaming URL mismatch')
                    return

                if sabr_format_group_config['video_playback_ustreamer_config'] != video_playback_ustreamer_config:
                    self.report_error('Video playback ustreamer config mismatch')
                    return

            itag = int_or_none(sabr_config.get('itag'))
            sabr_format_group_config['formats'].append({
                'format_id': itag and FormatId(itag=itag, last_modified=int_or_none(sabr_config.get('last_modified')), xtags=sabr_config.get('xtags')),
                'format_type': FormatType.VIDEO if f.get('acodec') == 'none' else FormatType.AUDIO,
                'quality': sabr_config.get('quality'),
                'height': sabr_config.get('height'),
                'filename': f.get('filepath', filename),
                'info_dict': f,
                'target_duration_sec': sabr_config.get('target_duration_sec'),
            })

        for name, format_group in sabr_format_groups.items():
            formats = format_group['formats']

            self.write_debug(f'Downloading formats for client {name}')

            # Group formats into video_audio pairs. SABR can currently download video+audio or audio.
            # Just video requires the audio stream to be discarded.
            audio_formats = (f for f in formats if f['format_type'] == FormatType.AUDIO)
            video_formats = (f for f in formats if f['format_type'] == FormatType.VIDEO)
            for audio_format, video_format in itertools.zip_longest(audio_formats, video_formats):
                audio_format_writer = audio_format and SABRFDWriter(self, audio_format.get('filename'), audio_format['info_dict'], 0)
                video_format_writer = video_format and SABRFDWriter(self, video_format.get('filename'), video_format['info_dict'], 1 if audio_format else 0)
                if not audio_format and video_format:
                    self.write_debug('Downloading a video stream without audio. SABR does not allow video-only, so an additional audio stream will be downloaded but discarded.')

                stream = SABRStream(
                    urlopen=self.ydl.urlopen,
                    logger=_YDLLogger(self.ydl),
                    debug=bool(traverse_obj(self.ydl.params, ('extractor_args', 'youtube', 'sabr_debug', 0, {int_or_none}), get_all=False)),
                    server_abr_streaming_url=format_group['server_abr_streaming_url'],
                    video_playback_ustreamer_config=format_group['video_playback_ustreamer_config'],
                    po_token_fn=format_group['po_token_fn'],
                    video_formats=video_format and [FormatRequest(
                        format_id=video_format['format_id'],
                        format_type=FormatType.VIDEO,
                        quality=video_format['quality'],
                        height=video_format['height'],
                        write_callback=video_format_writer.write
                    )],
                    audio_formats=audio_format and [FormatRequest(
                        format_id=audio_format['format_id'],
                        format_type=FormatType.AUDIO,
                        quality=audio_format['quality'],
                        height=audio_format['height'],
                        write_callback=audio_format_writer.write
                    )],
                    start_time_ms=format_group['start_time_ms'],
                    client_info=format_group['client_info'],
                    reload_config_fn=format_group['reload_config_fn'],
                    live_segment_target_duration_sec=format_group.get('target_duration_sec'),  # todo: should this be with the format request?
                )
                self._prepare_multiline_status(int(bool(audio_format and video_format)) + 1)

                try:
                    stream.download()
                except KeyboardInterrupt:
                    if not info_dict.get('is_live'):
                        raise
                    self.to_screen(f'Interrupted by user')
                    return True
                finally:
                    if audio_format_writer:
                        audio_format_writer.finish()
                    if video_format_writer:
                        video_format_writer.finish()

        return True
