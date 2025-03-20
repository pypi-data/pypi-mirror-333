#!/usr/bin/env python3
# This file is part of Xpra.
# Copyright (C) 2013-2024 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import sys
import traceback
from threading import Lock
from typing import Any
from collections.abc import Callable, Sequence, Iterable

from xpra.common import Self
from xpra.scripts.config import csvstrl
from xpra.codecs.constants import VideoSpec, CodecSpec, CSCSpec
from xpra.codecs.loader import load_codec, get_codec, get_codec_error, autoprefix
from xpra.util.str_fn import csv, print_nested_dict
from xpra.log import Logger

log = Logger("codec", "video")

# the codec loader uses the names...
# but we need the module name to be able to probe without loading the codec:
CODEC_TO_MODULE: dict[str, str] = {
    "enc_vpx"       : "vpx.encoder",
    "dec_vpx"       : "vpx.decoder",
    "enc_x264"      : "x264.encoder",
    "enc_openh264"  : "openh264.encoder",
    "nvenc"         : "nvidia.nvenc",
    "nvdec"         : "nvidia.nvdec",
    "csc_cython"    : "csc_cython.converter",
    "csc_libyuv"    : "libyuv.converter",
    "dec_openh264"  : "openh264.decoder",
    "enc_jpeg"      : "jpeg.encoder",
    "enc_webp"      : "webp.encoder",
    "enc_nvjpeg"    : "nvidia.nvjpeg.encoder",
    "dec_nvjpeg"    : "nvidia.nvjpeg.decoder",
    "dec_gstreamer" : "gstreamer.decoder",
    "enc_gstreamer" : "gstreamer.encoder",
}


def has_codec_module(module_name: str) -> bool:
    top_module = f"xpra.codecs.{module_name}"
    try:
        __import__(top_module, {}, {}, [])
        log("codec module %s is installed", module_name)
        return True
    except Exception as e:
        log("codec module %s cannot be loaded: %s", module_name, e)
        return False


def try_import_modules(prefix: str, *codec_names: str) -> list[str]:
    names = []
    for codec_name in codec_names:
        codec_name = autoprefix(prefix, codec_name)
        module_name = CODEC_TO_MODULE[codec_name]
        if has_codec_module(module_name):
            names.append(codec_name)
    return names


# all the codecs we know about:
ALL_VIDEO_ENCODER_OPTIONS: Sequence[str] = ("x264", "openh264", "vpx", "nvenc", "nvjpeg", "jpeg", "webp", "gstreamer")
HARDWARE_ENCODER_OPTIONS: Sequence[str] = ("nvenc", "nvjpeg")
ALL_CSC_MODULE_OPTIONS: Sequence[str] = ("cython", "libyuv")
ALL_VIDEO_DECODER_OPTIONS: Sequence[str] = ("openh264", "vpx", "gstreamer", "nvdec")

PREFERRED_ENCODER_ORDER: Sequence[str] = tuple(
    autoprefix("enc", x) for x in (
        "nvenc", "nvjpeg", "x264", "vpx", "jpeg", "webp", "gstreamer")
)
log("video: ALL_VIDEO_ENCODER_OPTIONS=%s", ALL_VIDEO_ENCODER_OPTIONS)
log("video: ALL_CSC_MODULE_OPTIONS=%s", ALL_CSC_MODULE_OPTIONS)
log("video: ALL_VIDEO_DECODER_OPTIONS=%s", ALL_VIDEO_DECODER_OPTIONS)
# for client side, using the gfx card for csc is a bit silly:
# use it for OpenGL or don't use it at all
# on top of that, there are compatibility problems with gtk at times: OpenCL AMD and TLS don't mix well


def get_encoder_module_name(x: str) -> str:
    return autoprefix("enc", x)


def get_decoder_module_name(x: str) -> str:
    return autoprefix("dec", x)


def get_csc_module_name(x: str) -> str:
    return autoprefix("csc", x)


def get_video_encoders(names=ALL_VIDEO_ENCODER_OPTIONS) -> list[str]:
    """ returns all the video encoders installed """
    return try_import_modules("enc", *names)


def get_csc_modules(names=ALL_CSC_MODULE_OPTIONS) -> list[str]:
    """ returns all the csc modules installed """
    return try_import_modules("csc", *names)


def get_video_decoders(names=ALL_VIDEO_DECODER_OPTIONS) -> list[str]:
    """ returns all the video decoders installed """
    return try_import_modules("dec", *names)


def get_hardware_encoders(names=HARDWARE_ENCODER_OPTIONS) -> list[str]:
    return try_import_modules("enc", *names)


def filt(prefix: str, name: str,
         inlist: Iterable[str],
         all_fn: Callable[[], list[str]],
         all_options: Iterable[str]) -> list[str]:
    # log("filt%s", (prefix, name, inlist, all_fn, all_list))
    instr = csvstrl(set(inlist or ())).strip(",")
    if instr == "none":
        return []

    def ap(v: str) -> str:
        if v.startswith("-"):
            return "-"+autoprefix(prefix, v[1:])
        if v.startswith("no-"):
            return "-"+autoprefix(prefix, v[3:])
        return autoprefix(prefix, v)

    def apl(items: Iterable[str]) -> list[str]:
        return [ap(v) for v in items]

    inlist = [x for x in instr.split(",") if x.strip()]
    while "all" in inlist:
        i = inlist.index("all")
        inlist = inlist[:i]+all_fn()+inlist[i+1:]
    exclist = apl(x[1:] for x in inlist if x and x.startswith("-"))
    inclist = apl(x for x in inlist if x and not x.startswith("-"))
    if not inclist and exclist:
        inclist = apl(all_fn())
    lists = exclist + inclist
    all_list = apl(all_options)
    unknown = tuple(x for x in lists if ap(x) not in CODEC_TO_MODULE and x.lower() != "none")
    if unknown:
        log.warn(f"Warning: ignoring unknown {name}: "+csv(unknown))
    notfound = tuple(x for x in lists if (x and ap(x) not in all_list and x not in unknown and x != "none"))
    if notfound:
        log.warn(f"Warning: {name} not found: "+csv(notfound))
    r = apl(x for x in inclist if x not in exclist and x != "none")
    # log("filt%s=%s", (prefix, name, inlist, all_fn, all_list), r)
    return r


VdictEntry = dict[str, list[CodecSpec]]
Vdict = dict[str, VdictEntry]


# manual deep-ish copy: make new dictionaries and lists,
# but keep the same codec specs:
def deepish_clone_dict(indict: Vdict) -> Vdict:
    outd: Vdict = {}
    for enc, d in indict.items():
        for ifmt, l in d.items():
            for v in l:
                outd.setdefault(enc, {}).setdefault(ifmt, []).append(v)
    return outd


def modstatus(x: str, def_list: Sequence[str], active_list: Sequence[str]):
    # the module is present
    if x in active_list:
        return "active"
    if x in def_list:
        return "disabled"
    return "not found"


class VideoHelper:
    """
        This class is a bit like a registry of known encoders, csc modules and decoders.
        The main instance, obtained by calling getVideoHelper, can be initialized
        by the main class, using the command line arguments.
        We can also clone it to modify it (used by per client proxy encoders)
    """

    def __init__(self,
                 vencspecs: Vdict | None=None,
                 cscspecs: Vdict | None=None,
                 vdecspecs: Vdict | None=None,
                 init=False):
        self._video_encoder_specs: Vdict = vencspecs or {}
        self._csc_encoder_specs: Vdict = cscspecs or {}
        self._video_decoder_specs: Vdict = vdecspecs or {}
        self.video_encoders = []
        self.csc_modules = []
        self.video_decoders = []

        self._cleanup_modules = []

        # bits needed to ensure we can initialize just once
        # even when called from multiple threads:
        self._initialized = init
        self._init_from = []
        self._lock = Lock()

    def is_initialized(self) -> bool:
        return self._initialized

    def set_modules(self,
                    video_encoders: Sequence[str] = (),
                    csc_modules: Sequence[str] = (),
                    video_decoders: Sequence[str] = (),
                    ):
        log("set_modules%s", (video_encoders, csc_modules, video_decoders))
        if self._initialized:
            log.error("Error: video helper modules have already been initialized")
            for ifrom in self._init_from:
                log.error("from:")
                for tb in ifrom:
                    log.error(" %s", tb.strip("\n\r"))
            raise RuntimeError("too late to set modules, the helper is already initialized")
        self.video_encoders = filt("enc", "video encoders", video_encoders,
                                   get_video_encoders, ALL_VIDEO_ENCODER_OPTIONS)
        self.csc_modules = filt("csc", "csc modules", csc_modules,
                                get_csc_modules, ALL_CSC_MODULE_OPTIONS)
        self.video_decoders = filt("dec", "video decoders", video_decoders,
                                   get_video_decoders, ALL_VIDEO_DECODER_OPTIONS)
        log("VideoHelper.set_modules(%r, %r, %r) video encoders=%s, csc=%s, video decoders=%s",
            csv(video_encoders), csv(csc_modules), csv(video_decoders),
            csv(self.video_encoders), csv(self.csc_modules), csv(self.video_decoders))

    def cleanup(self) -> None:
        with self._lock:
            # check again with lock held (in case of race):
            if not self._initialized:
                return
            cmods = self._cleanup_modules
            self._cleanup_modules = []
            log("VideoHelper.cleanup() cleanup modules=%s", cmods)
            for module in cmods:
                with log.trap_error(f"Error cleaning up {module}"):
                    module.cleanup_module()
            self._video_encoder_specs = {}
            self._csc_encoder_specs = {}
            self._video_decoder_specs = {}
            self.video_encoders = []
            self.csc_modules = []
            self.video_decoders = []
            self._initialized = False

    def clone(self) -> Self:
        if not self._initialized:
            self.init()
        ves = deepish_clone_dict(self._video_encoder_specs)
        ces = deepish_clone_dict(self._csc_encoder_specs)
        vds = deepish_clone_dict(self._video_decoder_specs)
        return VideoHelper(ves, ces, vds, True)

    def get_info(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        if not (self.video_encoders or self.csc_modules or self.video_decoders):
            # shortcut out: nothing to show
            return d
        einfo = d.setdefault("encoding", {})
        dinfo = d.setdefault("decoding", {})
        cinfo = d.setdefault("csc", {})
        for encoding, encoder_specs in self._video_encoder_specs.items():
            for in_csc, specs in encoder_specs.items():
                for spec in specs:
                    einfo.setdefault(f"{in_csc}_to_{encoding}", []).append(spec.codec_type)
        for in_csc, out_specs in self._csc_encoder_specs.items():
            for out_csc, specs in out_specs.items():
                cinfo[f"{in_csc}_to_{out_csc}"] = [spec.codec_type for spec in specs]
        for encoding, decoder_specs in self._video_decoder_specs.items():
            for out_csc, decoders in decoder_specs.items():
                for decoder in decoders:
                    dinfo.setdefault(f"{encoding}_to_{out_csc}", []).append(decoder.codec_type)
        venc = einfo.setdefault("video-encoder", {})
        for x in ALL_VIDEO_ENCODER_OPTIONS:
            venc[x] = modstatus(get_encoder_module_name(x), get_video_encoders(), self.video_encoders)
        cscm = einfo.setdefault("csc-module", {})
        for x in ALL_CSC_MODULE_OPTIONS:
            cscm[x] = modstatus(get_csc_module_name(x), get_csc_modules(), self.csc_modules)
        d["gpu"] = {
            "encodings": tuple(self.get_gpu_encodings().keys()),
            "csc": tuple(self.get_gpu_csc().keys()),
            "decodings": tuple(self.get_gpu_decodings().keys()),
        }
        return d

    def init(self) -> None:
        log("VideoHelper.init()")
        with self._lock:
            self._init_from.append(traceback.format_stack())
            # check again with lock held (in case of race):
            log("VideoHelper.init() initialized=%s", self._initialized)
            if self._initialized:
                return
            self.init_video_encoders_options()
            self.init_csc_options()
            self.init_video_decoders_options()
            self._initialized = True
        log("VideoHelper.init() done")

    def get_gpu_options(self, codec_specs: Vdict, out_fmts=("*", )) -> dict[str, list[CodecSpec]]:
        gpu_fmts: dict[str, list[CodecSpec]] = {}
        for in_fmt, vdict in codec_specs.items():
            for out_fmt, codecs in vdict.items():
                if "*" not in out_fmts and out_fmt not in out_fmts:
                    continue
                for codec in codecs:
                    if codec.gpu_cost > codec.cpu_cost:
                        log(f"get_gpu_options {out_fmt}: {codec}")
                        gpu_fmts.setdefault(in_fmt, []).append(codec)
        log(f"get_gpu_options({codec_specs})={gpu_fmts}")
        return gpu_fmts

    def get_gpu_encodings(self) -> dict[str, list[CodecSpec]]:
        return self.get_gpu_options(self._video_encoder_specs)

    def get_gpu_csc(self) -> dict[str, list[CodecSpec]]:
        return self.get_gpu_options(self._csc_encoder_specs)

    def get_gpu_decodings(self) -> dict[str, list[CodecSpec]]:
        return self.get_gpu_options(self._video_decoder_specs)

    def get_encodings(self) -> Sequence[str]:
        return tuple(self._video_encoder_specs.keys())

    def get_decodings(self) -> Sequence[str]:
        return tuple(self._video_decoder_specs.keys())

    def get_csc_inputs(self) -> Sequence[str]:
        return tuple(self._csc_encoder_specs.keys())

    def get_encoder_specs(self, encoding: str) -> VdictEntry:
        return self._video_encoder_specs.get(encoding, {})

    def get_csc_specs(self, src_format: str) -> VdictEntry:
        return self._csc_encoder_specs.get(src_format, {})

    def get_decoder_specs(self, encoding: str) -> VdictEntry:
        return self._video_decoder_specs.get(encoding, {})

    def init_video_encoders_options(self) -> None:
        log("init_video_encoders_options()")
        log(" will try video encoders: %s", csv(self.video_encoders))
        for x in self.video_encoders:
            try:
                mod = get_encoder_module_name(x)
                load_codec(mod)
                log(" encoder for %s: %s", x, mod)
                try:
                    self.init_video_encoder_option(mod)
                except Exception as e:
                    log(" init_video_encoder_option(%s) error", mod, exc_info=True)
                    log.warn("Warning: cannot load %s video encoder:", mod)
                    log.warn(" %s", e)
                    del e
            except Exception as e:
                log("error on %s", x, exc_info=True)
                log.warn("Warning: cannot add %s encoder: %s", x, e)
                del e
        log("found %i video encoder formats: %s",
            len(self._video_encoder_specs), csv(self._video_encoder_specs))

    def init_video_encoder_option(self, encoder_name: str) -> None:
        encoder_module = get_codec(encoder_name)
        log("init_video_encoder_option(%s)", encoder_name)
        log(" module=%s", encoder_module)
        if not encoder_module:
            log(" video encoder '%s' could not be loaded:", encoder_name)
            log(" %s", get_codec_error(encoder_name))
            return
        encoder_type = encoder_module.get_type()
        encodings = encoder_module.get_encodings()
        log(" %12s encodings=%s", encoder_type, csv(encodings))
        for encoding in encodings:
            colorspaces = encoder_module.get_input_colorspaces(encoding)
            log(" %9s  input colorspaces for %5s: %s", encoder_type, encoding, csv(colorspaces))
            for colorspace in colorspaces:
                specs = encoder_module.get_specs(encoding, colorspace)
                for spec in specs:
                    self.add_encoder_spec(encoding, colorspace, spec)
        log("video encoder options: %s", self._video_encoder_specs)

    def add_encoder_spec(self, encoding: str, colorspace: str, spec: VideoSpec):
        self._video_encoder_specs.setdefault(encoding, {}).setdefault(colorspace, []).append(spec)

    def init_csc_options(self) -> None:
        log("init_csc_options()")
        log(" will try csc modules: %s", csv(self.csc_modules))
        for x in self.csc_modules:
            try:
                mod = get_csc_module_name(x)
                load_codec(mod)
                self.init_csc_option(mod)
            except ImportError:
                log.warn(f"Warning: cannot add {x!r} csc", exc_info=True)
        log(" csc specs: %s", csv(self._csc_encoder_specs))
        for src_format, d in sorted(self._csc_encoder_specs.items()):
            log(" %s - %s options:", src_format, len(d))
            for dst_format, specs in sorted(d.items()):
                log("  * %7s via: %s", dst_format, csv(sorted(spec.codec_type for spec in specs)))
        log("csc options: %s", self._csc_encoder_specs)

    def init_csc_option(self, csc_name: str) -> None:
        csc_module = get_codec(csc_name)
        log("init_csc_option(%s)", csc_name)
        log(" module=%s", csc_module)
        if csc_module is None:
            log(" csc module %s could not be loaded:", csc_name)
            log(" %s", get_codec_error(csc_name))
            return
        in_cscs = csc_module.get_input_colorspaces()
        for in_csc in in_cscs:
            out_cscs = csc_module.get_output_colorspaces(in_csc)
            log("%9s output colorspaces for %7s: %s", csc_module.get_type(), in_csc, csv(out_cscs))
            for out_csc in out_cscs:
                spec = csc_module.get_spec(in_csc, out_csc)
                self.add_csc_spec(in_csc, out_csc, spec)

    def add_csc_spec(self, in_csc: str, out_csc: str, spec: CSCSpec) -> None:
        self._csc_encoder_specs.setdefault(in_csc, {}).setdefault(out_csc, []).append(spec)

    def init_video_decoders_options(self) -> None:
        log("init_video_decoders_options()")
        log(" will try video decoders: %s", csv(self.video_decoders))
        for x in self.video_decoders:
            try:
                mod = get_decoder_module_name(x)
                load_codec(mod)
                self.init_video_decoder_option(mod)
            except ImportError:
                log.warn(f"Warning: cannot add {x!r} decoder", exc_info=True)
        log("found %s video decoder formats: %s",
            len(self._video_decoder_specs), csv(self._video_decoder_specs))
        log("video decoder options: %s", self._video_decoder_specs)

    def init_video_decoder_option(self, decoder_name: str) -> None:
        decoder_module = get_codec(decoder_name)
        log("init_video_decoder_option(%s)", decoder_name)
        log(" module=%s", decoder_module)
        if not decoder_module:
            log(" video decoder %s could not be loaded:", decoder_name)
            log(" %s", get_codec_error(decoder_name))
            return
        decoder_type = decoder_module.get_type()
        encodings = decoder_module.get_encodings()
        log(" %s encodings=%s", decoder_type, csv(encodings))
        for encoding in encodings:
            colorspaces = decoder_module.get_input_colorspaces(encoding)
            log(" %s input colorspaces for %s: %s", decoder_type, encoding, csv(colorspaces))
            for colorspace in colorspaces:
                specs = decoder_module.get_specs(encoding, colorspace)
                for spec in specs:
                    self.add_decoder_spec(encoding, colorspace, spec)

    def add_decoder_spec(self, encoding: str, colorspace: str, decoder_spec: VideoSpec):
        self._video_decoder_specs.setdefault(encoding, {}).setdefault(colorspace, []).append(decoder_spec)

    def get_server_full_csc_modes(self, *client_supported_csc_modes: str) -> dict[str, list[str]]:
        """ given a list of CSC modes the client can handle,
            returns the CSC modes per encoding that the server can encode with.
            (taking into account the decoder's actual output colorspace for each encoding)
        """
        log("get_server_full_csc_modes(%s) decoder encodings=%s",
            client_supported_csc_modes, csv(self._video_decoder_specs.keys()))
        full_csc_modes: dict[str, list[str]] = {}
        for encoding, encoding_specs in self._video_decoder_specs.items():
            assert encoding_specs is not None
            for colorspace, decoder_specs in sorted(encoding_specs.items()):
                for decoder_spec in decoder_specs:
                    for output_colorspace in decoder_spec.output_colorspaces:
                        log("found decoder %12s for %5s with %7s mode, outputs '%s'",
                            decoder_spec.codec_type, encoding, colorspace, output_colorspace)
                        if output_colorspace in client_supported_csc_modes:
                            encoding_colorspaces = full_csc_modes.setdefault(encoding, [])
                            if colorspace not in encoding_colorspaces:
                                encoding_colorspaces.append(colorspace)
        log("get_server_full_csc_modes(%s)=%s", client_supported_csc_modes, full_csc_modes)
        return full_csc_modes

    def get_server_full_csc_modes_for_rgb(self, *target_rgb_modes: str) -> dict[str, list[str]]:
        """ given a list of RGB modes the client can handle,
            returns the CSC modes per encoding that the server can encode with,
            this will include the RGB modes themselves too.
        """
        log("get_server_full_csc_modes_for_rgb%s", target_rgb_modes)
        supported_csc_modes = list(target_rgb_modes)
        for src_format, specs in self._csc_encoder_specs.items():
            for dst_format, csc_specs in specs.items():
                if dst_format in target_rgb_modes and csc_specs:
                    supported_csc_modes.append(src_format)
                    break
        supported_csc_modes = sorted(supported_csc_modes)
        return self.get_server_full_csc_modes(*supported_csc_modes)


instance = None


def getVideoHelper() -> VideoHelper:
    global instance
    if instance is None:
        instance = VideoHelper()
    return instance


def main():
    # pylint: disable=import-outside-toplevel
    from xpra.codecs.loader import load_codecs, show_codecs
    from xpra.log import enable_color, consume_verbose_argv
    from xpra.platform import program_context
    with program_context("Video Helper"):
        enable_color()
        consume_verbose_argv(sys.argv, "video", "encoding")
        load_codecs()
        show_codecs()
        vh = getVideoHelper()
        vh.set_modules(ALL_VIDEO_ENCODER_OPTIONS, ALL_CSC_MODULE_OPTIONS, ALL_VIDEO_DECODER_OPTIONS)
        vh.init()
        info = vh.get_info()
        print_nested_dict(info)


if __name__ == "__main__":
    main()
