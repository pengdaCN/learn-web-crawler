import io
import typing

import ddddocr
from PIL import Image


def read_file(p: str, mode='r') -> str | bytes:
    with open(p, mode=mode) as f:
        return f.read()


def write_file(p: str, bs: bytes):
    with open(p, mode='wb') as w:
        w.write(bs)


def image_to_png(src: bytes) -> bytes:
    data = io.BytesIO()
    img = Image.open(io.BytesIO(src))
    img.save(data, format='png')

    return data.getvalue()


def words(bs: bytes) -> typing.Iterator[tuple[str, [str]]]:
    ocr = ddddocr.DdddOcr()
    det = ddddocr.DdddOcr(det=True)

    img = Image.open(io.BytesIO(bs))
    for x in det.detection(bs):
        crop = img.crop(x)
        data = io.BytesIO()
        crop.save(data, format='png')

        w = ocr.classification(data.getvalue())

        yield w, x
