#!/usr/bin/env python3
"""Конвертер изображений для ЛР №2: PNG/JPG <-> бинарный формат курса.

Формат: int32 w, int32 h, затем w*h пикселей по 4 байта (r, g, b, a), построчно.

Использование:
    python3 converter.py to_bin  picture.png  image.data
    python3 converter.py to_img  image.data   result.png
Требуется: pip install pillow numpy
"""
import sys
import numpy as np
from PIL import Image


def to_bin(src, dst):
    img = np.array(Image.open(src).convert("RGBA"), dtype=np.uint8)
    h, w = img.shape[:2]
    with open(dst, "wb") as f:
        f.write(np.array([w, h], dtype="<i4").tobytes())
        f.write(img.tobytes())


def to_img(src, dst):
    with open(src, "rb") as f:
        w, h = np.frombuffer(f.read(8), dtype="<i4")
        data = np.frombuffer(f.read(), dtype=np.uint8).reshape(h, w, 4)
    Image.fromarray(data, "RGBA").save(dst)


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[1] not in ("to_bin", "to_img"):
        print(__doc__)
        sys.exit(1)
    (to_bin if sys.argv[1] == "to_bin" else to_img)(sys.argv[2], sys.argv[3])
