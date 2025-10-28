from typing import Optional, Tuple


def _get_file_size(f) -> int:
    pos = f.tell()
    f.seek(0, 2)
    size = f.tell()
    f.seek(pos)
    return size


def _read(f, n: int) -> bytes:
    data = f.read(n)
    return data if data is not None else b""


def _png_size(f) -> Optional[Tuple[int, int]]:
    sig = _read(f, 8)
    if sig != b"\x89PNG\r\n\x1a\n":
        return None
    header = _read(f, 25)
    if len(header) < 17:
        return None
    if header[4:8] != b"IHDR":
        return None
    w = int.from_bytes(header[8:12], "big")
    h = int.from_bytes(header[12:16], "big")
    return w, h


def _jpeg_size(f) -> Optional[Tuple[int, int]]:
    if _read(f, 2) != b"\xff\xd8":
        return None
    while True:
        marker_prefix = _read(f, 1)
        if not marker_prefix:
            return None
        if marker_prefix != b"\xff":
            continue
        marker = _read(f, 1)
        if not marker:
            return None
        while marker == b"\xff":
            marker = _read(f, 1)
            if not marker:
                return None
        if marker in (b"\xd8", b"\x01"):
            continue
        if marker == b"\xd9":
            return None
        seg_len_bytes = _read(f, 2)
        if len(seg_len_bytes) != 2:
            return None
        seg_len = int.from_bytes(seg_len_bytes, "big")
        if seg_len < 2:
            return None
        if marker in (b"\xc0", b"\xc1", b"\xc2", b"\xc3"):
            sof_data = _read(f, seg_len - 2)
            if len(sof_data) < 7:
                return None
            h = int.from_bytes(sof_data[1:3], "big")
            w = int.from_bytes(sof_data[3:5], "big")
            return w, h
        else:
            f.seek(seg_len - 2, 1)


def _detect_image_size_and_format(f) -> Tuple[str, Optional[Tuple[int, int]]]:
    pos = f.tell()
    f.seek(0)
    size = None
    fmt = ""
    f.seek(0)
    size = _png_size(f)
    if size:
        fmt = "png"
    else:
        f.seek(0)
        size = _jpeg_size(f)
        if size:
            fmt = "jpeg"
    f.seek(pos)
    return fmt, size
