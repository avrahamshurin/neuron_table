from tkinter import *
from pathlib import Path
from src.slide import Slide
from src.gif import Gif, GifPlayer


class ControlsWindow(Toplevel):

    RES_PATH = Path(r'../res')
    NEURON_IMG_PATH = RES_PATH / 'neuron' / 'neuron_{}_{}.png'
    GIF_PATH = RES_PATH / 'gifs' / 'gif_{}_{}.gif'
    SLIDES = [['Desire:', 4], ['Fear:', 3]]
    PADS = {'padx': 5, 'pady': 5}
    LEFT_OFFSET = 10

    def __init__(self, master=None, cnf={}, **kw):
        # save reference to neuron window
        self.neuron = kw.pop('neuron')
        Toplevel.__init__(self, master, cnf, **kw)
        self.geometry("+{}+{}".format(self.neuron.DISPLAY_SIZE - self.LEFT_OFFSET, 0))
        self.bind("<Destroy>", self.neuron.exit)
        self.title('Neuron V1.0.0')

        self.reload_button = Button(self, text='Reload', command=self.load_media)
        self.reload_button.pack(in_=self, fill=BOTH, **self.PADS)

        self.swap_screen_button = Button(self, text='Swap Screen', command=self.neuron.swap_screen)
        self.swap_screen_button.pack(in_=self, fill=BOTH, **self.PADS)

        self.controls_frame = LabelFrame(self, text='Controls:')
        self.controls_frame.pack(**self.PADS)

        self.slides_frame = Frame(self)
        self.slides_frame.pack(in_=self.controls_frame, **self.PADS)

        self.slides = []
        for name, size in self.SLIDES:
            slide = Slide(self, size=size, command=self.slide_command, text=name)
            slide.pack(in_=self.slides_frame, side=LEFT, fill=Y, **self.PADS)
            self.slides.append(slide)

        self.decide_button = Button(self, text='Decide!', command=self.decide_command)
        self.decide_button.pack(in_=self.controls_frame, fill=BOTH, **self.PADS)

        self.gifs = []
        self.load_media()
        self.gif_player = GifPlayer(self.neuron)
        self.decide_command()

    def load_media(self):
        self.gifs.clear()
        for i in range(self.SLIDES[0][1]):
            for j in range(self.SLIDES[1][1]):
                self.gifs.append(Gif(str(self.GIF_PATH).format(i, j)))

    def decide_command(self):
        if self.gif_player.play_count:
            return
        self.gif_player.play(
            self.gifs[self.slides[1].value.get() + self.slides[0].value.get() * self.SLIDES[1][1]])

    def slide_command(self, *_, **__):
        print('slide_command')


class NeuronWindow(Frame):
    DISPLAY_SIZE = 448

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, bd=0, **kw)
        self.pack(fill=BOTH, expand=1)

        # remove window border and put it on top
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True)

        # exit on escape key press
        self.bind_all("<Escape>", self.exit)

        self.canvas = Canvas(self, bg='black', height=self.DISPLAY_SIZE,
                             width=self.DISPLAY_SIZE, highlightthickness=0)
        self.canvas.pack(fill=BOTH)

        # show controls window
        self.controls_window = ControlsWindow(self.master, neuron=self)

    def swap_screen(self):
        # get [width, height, left, top] of window
        rect = [int(i) for i in self.master.winfo_geometry().replace('x', '+').split('+')]
        rect[2] = self.master.winfo_screenwidth() - rect[2]
        # set [width, height, left, top] of window
        self.master.geometry("{}x{}+{}+{}".format(*rect))

    def exit(self, *_, **__):
        if hasattr(self, '_exit'):
            return
        setattr(self, '_exit', True)
        print('exit')
        self.master.quit()


def main():
    root = Tk()
    neuron = NeuronWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
