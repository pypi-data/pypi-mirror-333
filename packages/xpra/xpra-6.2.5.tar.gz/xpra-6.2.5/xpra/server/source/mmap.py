# This file is part of Xpra.
# Copyright (C) 2010-2024 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

from random import randint
from typing import Any

from xpra.util.objects import typedict
from xpra.server.source.stub_source_mixin import StubSourceMixin

from xpra.log import Logger

log = Logger("mmap")


class MMAP_Connection(StubSourceMixin):

    @classmethod
    def is_needed(cls, caps: typedict) -> bool:
        v = typedict(caps.get("mmap") or {})
        return v.intget("size", 0) > 0

    def __init__(self):
        self.supports_mmap = False
        self.mmap_filename = ""
        self.min_mmap_size = 0

    def init_from(self, _protocol, server) -> None:
        self.supports_mmap = server.supports_mmap
        self.mmap_filename = server.mmap_filename
        self.min_mmap_size = server.min_mmap_size

    def init_state(self) -> None:
        self.mmap = None
        self.mmap_size = 0
        self.mmap_client_token = 0  # the token we write that the client may check
        self.mmap_client_token_index = 512
        self.mmap_client_token_bytes = 0

    def cleanup(self) -> None:
        mmap = self.mmap
        if mmap:
            self.mmap = None
            self.mmap_size = 0
            mmap.close()

    def parse_client_caps(self, c: typedict) -> None:
        # pylint: disable=import-outside-toplevel
        import os
        from xpra.os_util import WIN32
        mmap_caps = c.dictget("mmap")
        c = typedict(mmap_caps or {})
        mmap_filename = c.strget("file")
        if not mmap_filename:
            return
        mmap_size = c.intget("size", 0)
        log("client supplied mmap_file=%s", mmap_filename)
        mmap_token = c.intget("token")
        log(f"mmap supported={self.supports_mmap}, token={mmap_token:x}")
        if self.mmap_filename:
            if os.path.isdir(self.mmap_filename):
                # use the client's filename, but at the server path:
                mmap_filename = os.path.join(self.mmap_filename, os.path.basename(mmap_filename))
                log(f"using global server specified mmap directory: {self.mmap_filename!r}")
            else:
                log(f"using global server specified mmap file path: {self.mmap_filename!r}")
                mmap_filename = self.mmap_filename
        if not self.supports_mmap:
            log("client enabled mmap but mmap mode is not supported")
        elif WIN32 and mmap_filename.startswith("/"):
            log(f"mmap_file {mmap_filename!r} is a unix path")
        elif not os.path.exists(mmap_filename):
            log(f"mmap_file {mmap_filename!r} cannot be found!")
        else:
            from xpra.net.mmap import init_server_mmap, read_mmap_token, write_mmap_token, DEFAULT_TOKEN_BYTES
            self.mmap, self.mmap_size = init_server_mmap(mmap_filename, mmap_size)
            log("found client mmap area: %s, %i bytes - min mmap size=%i in '%s'",
                self.mmap, self.mmap_size, self.min_mmap_size, mmap_filename)
            if self.mmap_size > 0 and self.mmap is not None:
                index = c.intget("token_index", 0)
                count = c.intget("token_bytes", DEFAULT_TOKEN_BYTES)
                v = read_mmap_token(self.mmap, index, count)
                if v != mmap_token:
                    log.warn("Warning: mmap token verification failed, not using mmap area!")
                    log.warn(f" expected {mmap_token:x}, found {v:x}")
                    self.mmap.close()
                    self.mmap = None
                    self.mmap_size = 0
                elif self.mmap_size < self.min_mmap_size:
                    log.warn("Warning: client supplied mmap area is too small, discarding it")
                    log.warn(" we need at least %iMB and this area is %iMB",
                             self.min_mmap_size // 1024 // 1024, self.mmap_size // 1024 // 1024)
                    self.mmap.close()
                    self.mmap = None
                    self.mmap_size = 0
                else:
                    from xpra.os_util import get_int_uuid
                    self.mmap_client_token = get_int_uuid()
                    self.mmap_client_token_bytes = DEFAULT_TOKEN_BYTES
                    self.mmap_client_token_index = randint(0, self.mmap_size - self.mmap_client_token_bytes)
                    write_mmap_token(self.mmap,
                                     self.mmap_client_token,
                                     self.mmap_client_token_index,
                                     self.mmap_client_token_bytes)
        if self.mmap_size > 0:
            from xpra.util.stats import std_unit
            log.info(" mmap is enabled using %sB area in %s", std_unit(self.mmap_size, unit=1024), mmap_filename)

    def get_caps(self) -> dict[str, Any]:
        mmap_caps: dict[str, Any] = {}
        if self.mmap_size > 0:
            mmap_caps["enabled"] = True
            if self.mmap_client_token:
                mmap_caps.update({
                    "token": self.mmap_client_token,
                    "token_index": self.mmap_client_token_index,
                    "token_bytes": self.mmap_client_token_bytes,
                })
        return {"mmap": mmap_caps}

    def get_info(self) -> dict[str, Any]:
        return {
            "mmap": {
                "supported": self.supports_mmap,
                "enabled": self.mmap is not None,
                "size": self.mmap_size,
                "filename": self.mmap_filename,
            },
        }
