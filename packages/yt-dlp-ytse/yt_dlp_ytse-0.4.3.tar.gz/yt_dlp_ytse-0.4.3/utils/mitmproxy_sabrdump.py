# usage: PYTHONPATH='.' mitmproxy -s utils/mitmproxy_sabrdump.py

import base64
import io

import protobug
from mitmproxy import http
from yt_dlp.networking import Response

from yt_dlp_plugins.extractor._ytse.protos import (
    MediaHeader,
    SabrRedirect,
    NextRequestPolicy,
    FormatInitializationMetadata,
    StreamProtectionStatus,
    VideoPlaybackAbrRequest,
    PlaybackStartPolicy,
    RequestCancellationPolicy,
    SabrSeek,
    LiveMetadata,
    unknown_fields,
    SelectableFormats,
    PrewarmConnection,
    AllowedCachedFormats,
    SabrContextUpdate,
    SabrContextSendingPolicy,
    TimelineContext,
    ReloadPlayerResponse,
    PlaybackDebugInfo,
    SnackbarMessage
)
from yt_dlp_plugins.extractor._ytse.ump import UMPPartType, UMPParser


def write_unknown_fields(f, protobug_obj):
    uf = list(unknown_fields(protobug_obj))
    if uf:
        f.write(f'Unknown Fields: {uf}\n')


class SABRParser:
    def response(self, flow: http.HTTPFlow) -> None:
        if "application/vnd.yt-ump" in flow.response.headers.get("Content-Type", ""):
            res = Response(fp=io.BytesIO(flow.response.content), url=flow.request.url, headers={})
            parser = UMPParser(res)
            rn = flow.request.query.get("rn")
            n = flow.request.query.get("n")
            expire = flow.request.query.get("expire")

            with open(f'dumps/{n or expire}-{rn}.dump', 'w') as f:
                f.write(f'URL: {flow.request.url}\n')
                f.write(f'request body base64: {base64.b64encode(flow.request.content).decode("utf-8")}\n')

                try:
                    vpar = protobug.loads(flow.request.content, VideoPlaybackAbrRequest)
                    f.write(f'request body decoded: {vpar}\n')
                    write_unknown_fields(f, vpar)
                except Exception as e:
                    print(f'not a sabr request: ({e})')

                for part in parser.iter_parts():
                    print(f'Part type: {part.part_type}, Part size: {part.size}')
                    f.write(
                        f'Part type: {part.part_type} ({part.part_type.name}), Part size: {part.size}\n')

                    if part.part_type != UMPPartType.MEDIA:
                        f.write(f'Part data base64: {part.get_b64_str()}\n')

                    if part.part_type == UMPPartType.MEDIA_HEADER:
                        media_header = protobug.loads(part.data, MediaHeader)
                        f.write(f'Media Header: {media_header}\n')
                        write_unknown_fields(f, media_header)

                    elif part.part_type == UMPPartType.SABR_REDIRECT:
                        sabr_redirect = protobug.loads(part.data, SabrRedirect)
                        f.write(f'SABR Redirect: {sabr_redirect}\n')
                        write_unknown_fields(f, sabr_redirect)

                    elif part.part_type == UMPPartType.NEXT_REQUEST_POLICY:
                        nrp = protobug.loads(part.data, NextRequestPolicy)
                        f.write(f'Next Request Policy: {nrp}\n')
                        write_unknown_fields(f, nrp)

                    elif part.part_type == UMPPartType.FORMAT_INITIALIZATION_METADATA:
                        fim = protobug.loads(part.data, FormatInitializationMetadata)
                        f.write(f'Format Initialization Metadata {fim}\n')
                        write_unknown_fields(f, fim)

                    elif part.part_type == UMPPartType.STREAM_PROTECTION_STATUS:
                        sps = protobug.loads(part.data, StreamProtectionStatus)
                        f.write(f'Stream Protection Status: {sps}\n')
                        write_unknown_fields(f, sps)

                    elif part.part_type == UMPPartType.PLAYBACK_START_POLICY:
                        psp = protobug.loads(part.data, PlaybackStartPolicy)
                        f.write(f'Playback Start Policy: {psp}\n')
                        write_unknown_fields(f, psp)

                    elif part.part_type == UMPPartType.REQUEST_CANCELLATION_POLICY:
                        rcp = protobug.loads(part.data, RequestCancellationPolicy)
                        f.write(f'Request Cancellation Policy: {rcp}\n')
                        write_unknown_fields(f, rcp)

                    elif part.part_type == UMPPartType.SABR_SEEK:
                        sabr_seek = protobug.loads(part.data, SabrSeek)
                        f.write(f'Sabr Seek: {sabr_seek}\n')
                        write_unknown_fields(f, sabr_seek)

                    elif part.part_type == UMPPartType.LIVE_METADATA:
                        lm = protobug.loads(part.data, LiveMetadata)
                        f.write(f'Live Metadata: {lm}\n')
                        write_unknown_fields(f, lm)

                    elif part.part_type == UMPPartType.SELECTABLE_FORMATS:
                        sf = protobug.loads(part.data, SelectableFormats)
                        f.write(f'Selectable Formats: {sf}\n')
                        write_unknown_fields(f, sf)

                    elif part.part_type == UMPPartType.PREWARM_CONNECTION:
                        pc = protobug.loads(part.data, PrewarmConnection)
                        f.write(f'Prewarm Connection: {pc}\n')
                        write_unknown_fields(f, pc)

                    elif part.part_type == UMPPartType.ALLOWED_CACHED_FORMATS:
                        acf = protobug.loads(part.data, AllowedCachedFormats)
                        f.write(f'Allowed Cached Formats: {acf}\n')
                        write_unknown_fields(f, acf)

                    elif part.part_type == UMPPartType.SABR_CONTEXT_UPDATE:
                        scu = protobug.loads(part.data, SabrContextUpdate)
                        f.write(f'Sabr Context Update: {scu}\n')
                        write_unknown_fields(f, scu)

                    elif part.part_type == UMPPartType.SABR_CONTEXT_SENDING_POLICY:
                        scsp = protobug.loads(part.data, SabrContextSendingPolicy)
                        f.write(f'Sabr Context Sending Policy: {scsp}\n')
                        write_unknown_fields(f, scsp)

                    elif part.part_type == UMPPartType.TIMELINE_CONTEXT:
                        tc = protobug.loads(part.data, TimelineContext)
                        f.write(f'Timeline Context: {tc}\n')
                        write_unknown_fields(f, tc)

                    elif part.part_type == UMPPartType.RELOAD_PLAYER_RESPONSE:
                        rpr = protobug.loads(part.data, ReloadPlayerResponse)
                        f.write(f'Reload Player Response: {rpr}\n')
                        write_unknown_fields(f, rpr)

                    elif part.part_type == UMPPartType.PLAYBACK_DEBUG_INFO:
                        pdi = protobug.loads(part.data, PlaybackDebugInfo)
                        f.write(f'Playback Debug Info: {pdi}\n')
                        write_unknown_fields(f, pdi)

                    elif part.part_type == UMPPartType.SNACKBAR_MESSAGE:
                        sm = protobug.loads(part.data, SnackbarMessage)
                        f.write(f'Snackbar Message: {sm}\n')
                        write_unknown_fields(f, sm)


                    elif part.part_type == UMPPartType.MEDIA or part.part_type == UMPPartType.MEDIA_END:
                        f.write(f'Media Header Id: {part.data[0]}\n')

addons = [
    SABRParser()
]