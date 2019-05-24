# import tkinter
from tkinter import *


class Slide(LabelFrame):

    RADIO_BUTTONS_TEXT = ['Small', 'Medium', 'Big', 'Large']
    PADS = {'padx': 5, 'pady': 5}

    def __init__(self, master=None, size=len(RADIO_BUTTONS_TEXT), command=None, cnf={}, **kw):
        LabelFrame.__init__(self, master=master, cnf=cnf, **kw)

        self.value = IntVar()
        self.scrollbar = Scale(master, showvalue=0, to=size-1, variable=self.value,
                               command=command)
        self.scrollbar.pack(in_=self, side=LEFT, fill=Y, **self.PADS)

        self.radio_frame = Frame(master)
        self.radio_frame.pack(in_=self, side=LEFT)

        self.radio_buttons = []
        for i in range(size):
            radio_button = Radiobutton(master, text=self.RADIO_BUTTONS_TEXT[i],
                                       variable=self.value, value=i, command=command)
            radio_button.pack(in_=self.radio_frame, side=TOP, anchor=W)
            self.radio_buttons.append(radio_button)
