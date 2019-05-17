from tkinter import *
from PIL import Image, ImageTk


class Gif(object):
    MODE = 'RGBA'

    def __init__(self, file_name, mode='RGBA'):
        im = Image.open(file_name)
        seq = []

        # append frames
        while 1:
            seq.append(im.copy())
            try:
                im.seek(len(seq))
            except EOFError:
                break

        self.delay = im.info.get('duration', 100)

        self.frames = []
        frame = seq[0]
        for diff in seq:
            frame.paste(diff)
            self.frames.append(ImageTk.PhotoImage(frame.convert(mode)))

