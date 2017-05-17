import tkinter as tk
from jockey.gui import HeaderFrame, InputLabelFrame, OutputLabelFrame
from jockey.util import TestSequence


class Application:
    def __init__(self, title: (tuple, str)=None):
        self.root = tk.Tk()

        # allow the GUI to stretch
        root_rows = 2
        root_columns = 2

        for x in range(root_columns):
            tk.Grid.columnconfigure(self.root, x, weight=1)

        for y in range(root_rows):
            tk.Grid.rowconfigure(self.root, y, weight=1)

        self.test_sequence = TestSequence()

        # create the base GUI frame elements
        self.header_frame = HeaderFrame(self.root, title=title)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky='news')

        self.input_frame = InputLabelFrame(self.root)
        self.input_frame.grid(row=1, column=0, sticky='news')

        self.output_frame = OutputLabelFrame(self.root)
        self.output_frame.grid(row=1, column=1, sticky='news')

        # application NEVER comes out of this !!!
        self.root.mainloop()

    def sleep(self, time, callback):
        print('sleeping for {}ms'.format(time))
        self.root.after(time, callback)

    def add_input_label(self, text, index: int=None):
        self.input_frame.add_label(text, index)

    def add_output_label(self, text, index: int=None):
        self.output_frame.add_label(text, index)

if __name__ == '__main__':
    Application(title=('Application', 'v0.0.1'))
