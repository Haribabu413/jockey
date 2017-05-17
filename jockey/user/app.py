import tkinter as tk
from jockey.gui import HeaderFrame, InputLabelFrame, OutputLabelFrame
from jockey.util import TestSequence


class Application:
    def __init__(self, title: (tuple, str)=None):
        # initialize the test sequences
        self.test_sequence = TestSequence()
        self.teardown = None

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

        self.input_frame = InputLabelFrame(self.root, start_command=self.run_test)
        self.input_frame.grid(row=1, column=0, sticky='news')

        self.output_frame = OutputLabelFrame(self.root)
        self.output_frame.grid(row=1, column=1, sticky='news')

    def __del__(self):
        if self.teardown is not None:
            self.teardown()

    def register_tests(self, setup_callback=None, test_callback=None, teardown_callback=None):
        # executing these should register the tests with the test sequences
        setup_callback()
        test_callback()
        self.teardown = teardown_callback

    def run(self):
        # application NEVER comes out of this !!!
        self.root.mainloop()

    def add_test(self, callback, args):
        self.test_sequence.add_test(callback, args)

    def run_test(self):
        if self.test_sequence.ready:
            self.test_sequence.reset()

        self.test_sequence.run_test()

        # continue adding the next test sequence for
        # as long as the test is not completed
        if not self.test_sequence.complete:
            self.root.after(100, self.run_test)
        else:
            self.teardown()
            self.test_sequence.reset()

    def add_input_label(self, text, index: int=None):
        self.input_frame.add_label(text, index)

    def add_output_label(self, text, index: int=None):
        self.output_frame.add_label(text, index)

if __name__ == '__main__':
    Application(title=('Application', 'v0.0.1'))
