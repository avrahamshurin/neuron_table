from tkinter import *
from slide import Slide


class NeuronWindow(Frame):

    NEURON_IMG_PATH = r'..\res\neuron\neuron_{}_{}.png'
    GRAPH_IMG_PATH = r'..\res\graph\graph_{}_{}.png'
    SLIDES = [['Desire:', 4], ['Fear:', 3]]
    PADS = {'padx': 5, 'pady': 5}
    NEURON_SIZE = 448

    def load_images(self):
        try:
            slides = [self.slides[i].value.get() for i in range(len(self.SLIDES))]
            self.neuron_image = PhotoImage(file=self.NEURON_IMG_PATH.format(*slides))
            self.graph_image = PhotoImage(file=self.GRAPH_IMG_PATH.format(*slides))
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

        self.decide_button = Button(self, text='Decide!', command=self.load_images)
        self.decide_button.pack(in_=self.controls_frame, fill=BOTH, **self.PADS)

        self.quit_btn = Button(self, text='Quit', bg='red', command=self.master.destroy)
        self.quit_btn.pack(in_=self, fill=BOTH, **self.PADS)


def main():
    root = Tk()
    neuron = NeuronWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
