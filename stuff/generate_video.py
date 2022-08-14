# works, but slow

import moviepy.editor as mpy
from PIL import Image
from pathlib import Path
import numpy as np

path = 'DALL·E 2022-08-13 22.45.48 - A man and woman lie on a striped picnic blanket in the grass; photorealistic.png'

im = Image.open(path)
im_np = np.array(im)

# im_clip = mpy.ImageClip(path)

W, H = 128, 128  # width, height, in pixels
duration = 2  # duration of the clip, in seconds


def make_frame(t):
    t_rel = t / duration  # goes from 0 to 1

    # out_im = im.rotate(t_rel * 360)

    # scale = t/2
    d = int(im.size[0]*t_rel)+1
    print(d)
    out_im = im.resize((d, d))

    return np.array(out_im)


clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_videofile("zoom.mp4", fps=10)
