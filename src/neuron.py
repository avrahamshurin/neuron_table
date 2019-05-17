from tkinter import *
from pathlib import Path
from slide import Slide
from gif import Gif


class NeuronWindow(Frame):
    RES_PATH = Path(r'../res')
    NEURON_IMG_PATH = RES_PATH / 'neuron' / 'neuron_{}_{}.png'
    GRAPH_IMG_PATH = RES_PATH / 'graph' / 'graph_{}_{}.png'
    GIF_PATH = RES_PATH / 'gifs' / 'gif_{}_{}.gif'
    SLIDES = [['Desire:', 4], ['Fear:', 3]]
    PADS = {'padx': 5, 'pady': 5}
    NEURON_SIZE = 448

    def load_images(self):
        self.neuron_canvas.create_line(0, 0, self.NEURON_SIZE, self.NEURON_SIZE, fill='white')
        self.neuron_canvas.create_line(0, self.NEURON_SIZE, self.NEURON_SIZE, 0, fill='white')

        try:
            slides = [self.slides[i].value.get() for i in range(len(self.SLIDES))]
            # self.image = PhotoImage(file=r'res\neuron\neuron.png')
            self.neuron_image = PhotoImage(file=str(self.NEURON_IMG_PATH).format(*slides))
            self.graph_image = PhotoImage(file=str(self.GRAPH_IMG_PATH).format(*slides))
            # print(slides)
        except:
            self.neuron_canvas.create_line(0, 0, self.NEURON_SIZE, self.NEURON_SIZE, fill='white')
            self.neuron_canvas.create_line(0, self.NEURON_SIZE, self.NEURON_SIZE, 0, fill='white')
        else:
            self.neuron_canvas.create_image(0, 0, anchor=NW, image=self.neuron_image)
            self.neuron_canvas.create_image(0, 256, anchor=NW, image=self.graph_image)
        finally:
            self.neuron_canvas.pack()

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, bd=0, **kw)
        self.pack(fill=BOTH, expand=1)

        # remove window border and put it on top
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True)

        self.neuron_canvas = Canvas(self, bg='black', height=self.NEURON_SIZE, width=self.NEURON_SIZE)
        self.neuron_canvas.pack(fill=BOTH)

        self.controls_frame = LabelFrame(self, text='Controls:')
        self.controls_frame.pack(**self.PADS, side=LEFT)

        self.slides_frame = Frame(self)
        self.slides_frame.pack(in_=self.controls_frame, **self.PADS)

        self.slides = []
        for name, size in self.SLIDES:
            slide = Slide(self, size=size, text=name)
            slide.pack(in_=self.slides_frame, side=LEFT, fill=Y, **self.PADS)
            self.slides.append(slide)

        self.decide_button = Button(self, text='Decide!', command=self.button_operation)
        self.decide_button.pack(in_=self.controls_frame, fill=BOTH, **self.PADS)

        self.quit_btn = Button(self, text='Quit', bg='red', command=self.master.destroy)
        self.quit_btn.pack(in_=self, fill=BOTH, **self.PADS)

        self.gifs = []
        for i in range(self.SLIDES[0][1]):
            for j in range(self.SLIDES[1][1]):
                self.gifs.append(Gif(str(self.GIF_PATH).format(i, j)))

        self.l = Label(self.neuron_canvas, bg='black', image=self.gifs[0].frames[0])
        self.l.pack()

        # self.gif_slides = [self.slides[i].value.get() for i in range(len(self.SLIDES))]
        self.playing = False
        self.idx = 0

    def button_operation(self):
        if self.playing:
            return
        self.play()

    def play(self):
        self.playing = True
        num = self.slides[1].value.get() + self.slides[0].value.get() * self.SLIDES[1][1]
        the_gif = self.gifs[num]

        self.l.config(image=the_gif.frames[self.idx])

        self.idx += 1
        if self.idx == len(the_gif.frames):
            self.playing = False
            self.idx = 0
        else:
            self.after(the_gif.delay, self.play)


def main():
    root = Tk()
    neuron = NeuronWindow(root)
    neuron.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
