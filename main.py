from pathlib import Path

from PIL import Image

from common import paths
from image_manipulation import remove_watermark


def zoom_out(path: Path):
    im = Image.open(path).convert('RGBA')
    assert im.size == (1024, 1024)

    # remove watermark
    im = remove_watermark(im)

    # zoom out
    new_size = (1024*3, 1024*3)
    new_im = Image.new('RGBA', new_size)
    new_im.paste(im, (1024, 1024))

    # show the image
    # new_im.show()

    # save the image
    out_path = path.with_suffix('.zoomed.png')
    if not out_path.exists():
        new_im.save(out_path)
    else:
        print(f'{out_path} already exists')


for path in paths:
    file = Path(path)
    zoom_out(file)
