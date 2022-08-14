import functools

import numpy as np
from PIL import Image


def prepare_image(func):
    @functools.wraps(func)
    def with_prepare_image(im, **kwargs):
        assert im.size == (1024, 1024)
        assert im.mode == 'RGBA', f"Image mode is {im.mode}, not RGBA"
        # alternatively: im = im.convert('RGBA')

        return func(im, **kwargs)
    return with_prepare_image


@prepare_image
def remove_watermark(im):
    """
    Replaces the DALL·E watermark on the bottom right with transparency.
    """
    rect_size = (80, 16)
    rect_pos = (944, 1008)
    watermark_rect = Image.new('RGBA', rect_size)
    im.paste(watermark_rect, rect_pos)
    return im


@prepare_image
def transparent_padding(im, border_size=12):
    """
    Replaces the padding with transparency.
    """
    # █ variant 1
    # region_to_keep = im.crop((border_size, border_size, im.size[0]-border_size, im.size[1]-border_size))
    # im = Image.new('RGBA', im.size, (255, 0, 0, 0))
    # im.paste(region_to_keep, (border_size, border_size))
    # return im

    # █ variant 2
    BORDER_VAL = 0  # transparent
    # BORDER_VAL = 127  # semi-transparent, for testing
    im_np = np.array(im)
    # top bar
    im_np[:border_size, :, :] = BORDER_VAL
    # bottom bar
    im_np[-border_size:, :, :] = BORDER_VAL
    # left bar
    im_np[:, :border_size, :] = BORDER_VAL
    # right bar
    im_np[:, -border_size:, :] = BORDER_VAL

    return Image.fromarray(im_np, mode='RGBA')
