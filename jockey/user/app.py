import tkinter as tk
from jockey.gui import HeaderFrame, InputLabelFrame, OutputLabelFrame
from jockey.util import TestSequence


class Application:
    def __init__(self, title: (tuple, str)=None,
                 setup_callback=None, test_callback=None, teardown_callback=None):
        # initialize the test sequences
        self.test_sequence = TestSequence()

        # executing these should register the tests with the test sequences
        setup_callback()
        test_callback()
        teardown_callback()

        # start the GUI
        self.root = tk.Tk()

        # allow the GUI to stretch
        tk.Grid.columnconfigure(self.root, 0, weight=1)
        tk.Grid.columnconfigure(self.root, 1, weight=1)
        tk.Grid.rowconfigure(self.root, 0, weight=1)
        tk.Grid.rowconfigure(self.root, 1, weight=1)

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
