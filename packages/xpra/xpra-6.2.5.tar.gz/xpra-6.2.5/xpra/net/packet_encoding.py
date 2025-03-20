#!/usr/bin/env python3
# This file is part of Xpra.
# Copyright (C) 2011-2024 Antoine Martin <antoine@xpra.org>
# Copyright (C) 2008, 2009, 2010 Nathaniel Smith <njs@pobox.com>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

# pylint: disable=import-outside-toplevel

from typing import Any
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass

from xpra.log import Logger
from xpra.common import SizedBuffer
from xpra.net.protocol.header import FLAGS_RENCODE, FLAGS_RENCODEPLUS, FLAGS_YAML, FLAGS_NOHEADER, pack_header
from xpra.util.str_fn import strtobytes, memoryview_to_bytes
from xpra.util.env import envbool

# all the encoders we know about:
ALL_ENCODERS: Sequence[str] = ("rencodeplus", "none")
# the encoders we may have, in the best compatibility order
TRY_ENCODERS: Sequence[str] = ("rencodeplus", "none")
# order for performance:
PERFORMANCE_ORDER: Sequence[str] = ("rencodeplus",)


@dataclass
class PacketEncoder:
    name: str
    flag: int
    version: str
    encode: Callable[[Any], tuple[SizedBuffer, int]]
    decode: Callable[[SizedBuffer], Any]


ENCODERS: dict[str, PacketEncoder] = {}


def init_rencodeplus() -> PacketEncoder:
    from xpra.net.rencodeplus import rencodeplus  # type: ignore[attr-defined]
    rencodeplus_dumps = rencodeplus.dumps  # @UndefinedVariable

    def do_rencodeplus(value) -> tuple[SizedBuffer, int]:
        return rencodeplus_dumps(value), FLAGS_RENCODEPLUS

    return PacketEncoder("rencodeplus", FLAGS_RENCODEPLUS, rencodeplus.__version__, do_rencodeplus, rencodeplus.loads)


def b(value) -> bytes:
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes, memoryview, bytearray)):
        return b" ".join(b(item) for item in value)
    return memoryview_to_bytes(value)


def none_encode(value) -> tuple[bytes, int]:
    # just send data as a byte string for clients that don't understand xpra packet format:
    bdata = b(value) + b"\n"
    return bdata, FLAGS_NOHEADER


def none_decode(data: SizedBuffer) -> SizedBuffer:
    return data


def init_none() -> PacketEncoder:
    return PacketEncoder("none", FLAGS_NOHEADER, "0", none_encode, none_decode)


def init_encoders(*names) -> None:
    for x in names:
        if x not in TRY_ENCODERS:
            logger = Logger("network", "protocol")
            logger.warn("Warning: invalid encoder '%s'", x)
            continue
        if not envbool("XPRA_" + x.upper(), True):
            continue
        fn = globals().get(f"init_{x}")
        try:
            assert callable(fn)
            e = fn()
            assert e
            ENCODERS[x] = e
        except (ImportError, AttributeError, AssertionError):
            logger = Logger("network", "protocol")
            logger.debug("no %s", x, exc_info=True)


def init_all() -> None:
    init_encoders(*(list(TRY_ENCODERS) + ["none"]))


def get_packet_encoding_caps(full_info: int = 1) -> dict[str, Any]:
    caps: dict[str, Any] = {}
    for name in TRY_ENCODERS:
        d = caps.setdefault(name, {})
        e = ENCODERS.get(name)
        d[""] = e is not None
        if e is None:
            continue
        if full_info > 1 and e.version:
            d["version"] = e.version
    return caps


def get_enabled_encoders(order: Iterable[str] = TRY_ENCODERS) -> Sequence[str]:
    return tuple(x for x in order if x in ENCODERS)


def get_encoder(e) -> Callable:
    if e not in ALL_ENCODERS:
        raise ValueError(f"invalid encoder name {e!r}")
    if e not in ENCODERS:
        raise ValueError(f"{e!r} is not available")
    return ENCODERS[e].encode


def get_packet_encoding_type(protocol_flags: int) -> str:
    if protocol_flags & FLAGS_RENCODEPLUS:
        return "rencodeplus"
    if protocol_flags & FLAGS_RENCODE:
        return "rencode"
    if protocol_flags & FLAGS_YAML:
        return "yaml"
    return "bencode"


class InvalidPacketEncodingException(Exception):
    pass


def pack_one_packet(packet: tuple) -> bytes:
    ee = get_enabled_encoders()
    if ee:
        e = get_encoder(ee[0])
        data, flags = e(packet)
        return pack_header(flags, 0, 0, len(data)) + data
    return strtobytes(packet)


def decode(data, protocol_flags: int):
    if isinstance(data, memoryview):
        data = data.tobytes()
    ptype = get_packet_encoding_type(protocol_flags)
    e = ENCODERS.get(ptype)
    if e:
        return e.decode(data)
    raise InvalidPacketEncodingException(f"{ptype!r} decoder is not available")


def main():  # pragma: no cover
    from xpra.util.str_fn import print_nested_dict
    from xpra.platform import program_context
    with program_context("Packet Encoding", "Packet Encoding Info"):
        init_all()
        print_nested_dict(get_packet_encoding_caps())


if __name__ == "__main__":  # pragma: no cover
    main()
