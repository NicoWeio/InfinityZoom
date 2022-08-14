import math

from manim import *
from PIL import Image

from common import paths
from image_manipulation import remove_watermark, transparent_padding

TIME_PER_IMAGE = 3
FRAME_SIZE = 3  # see config


def gen_image(path, i, is_last=False):
    im = Image.open(path).convert('RGBA')

    if not is_last:
        im = remove_watermark(im)
        im = transparent_padding(im, border_size=128)

    img = ImageMobject(np.array(im))
    # img.height = FRAME_SIZE * (3**i)  # consistent sizes relative to each other
    img.height = FRAME_SIZE * 3  # useful when scaling only active images

    # img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])  # TODO: seems to be the default
    # img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])  # testing

    return img.set_z_index(-i)


class ImageFromArray(Scene):
    def construct(self):
        # images = [gen_image(path, i) for i, path in enumerate(paths)]
        images = [gen_image(path, i, is_last=i == len(paths)-1) for i, path in enumerate(paths)]

        # initialize the first image
        images[0].height = FRAME_SIZE
        self.add(images[0])

        # main loop for the zoom animation
        for i in range(len(images) - 1):
            self.add(images[i+1])  # add new, larger image in the background
            if i+2 < len(images):
                self.add(images[i+2])  # add new, larger image in the background

            t_tracker = ValueTracker(0)

            def img1_updater(img):
                t = t_tracker.get_value()
                img.height = FRAME_SIZE / (3**(t-0))
                img.fade(t)
                return img

            def img2_updater(img):
                t = t_tracker.get_value()
                img.height = FRAME_SIZE / (3**(t-1))
                # img.fade(t)
                return img

            def img3_updater(img):
                t = t_tracker.get_value()
                img.height = FRAME_SIZE / (3**(t-2))
                # img.fade(t)
                return img

            images[i].add_updater(img1_updater)
            images[i+1].add_updater(img2_updater)
            if i+2 < len(images):
                images[i+2].add_updater(img3_updater)

            self.play(
                t_tracker.animate.set_value(1),
                rate_func=linear,
                run_time=TIME_PER_IMAGE,
            )

            images[i].clear_updaters()
            images[i+1].clear_updaters()
            if i+2 < len(images):
                images[i+2].clear_updaters()

            # self.wait(1)
            self.remove(images[i])  # remove the now-invisible smaller image

        # keep the last image for a while
        self.wait(1)
