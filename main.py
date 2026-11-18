#!/usr/bin/env python3
"""Entry program for news-image-20261118 (make.fun).

Copies the repo's entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output). Standard library only, no network.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    src_size = os.path.getsize(SRC)
    dst_size = os.path.getsize(dst)
    if src_size != dst_size:
        raise SystemExit(
            "copy-size mismatch: source %d bytes, destination %d bytes"
            % (src_size, dst_size)
        )
    print("wrote %s (%d bytes)" % (dst, dst_size))


if __name__ == "__main__":
    main()
