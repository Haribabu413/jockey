import tkinter as tk
from jockey.gui import HeaderFrame, InputLabelFrame, OutputLabelFrame
from jockey.util import TestSequence


class Application:
    def __init__(self, title: (tuple, str), save_path: str):
        # initialize the test sequences
        self.test_sequence = TestSequence()
        self.teardown = None
        self.save_path = save_path

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

        self.input_frame = InputLabelFrame(self.root, start_command=self.start_btn_pressed)
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

    def start_btn_pressed(self):
        self.input_frame.disable()
        self.clear_output()

        # allow time for the button to disable before beginning the test sequence
        self.root.after(150, self.run_test)

    def run_test(self):
        result = self.test_sequence.run_test()
        if result.get('save_column_header') is not None:
            self.add_output_label(result.get('save_column_header'))
            self.add_output_label(result.get('value'))
        # todo: display results in output

        # continue adding the next test sequence for
        # as long as the test is not completed
        if not self.test_sequence.complete:
            self.root.after(100, self.run_test)
        else:
            self.teardown()
            self.process_results(self.test_sequence.results)
            self.test_sequence.reset()
            self.input_frame.enable()

    def process_results(self, results):
        pass

    def add_input_label(self, text, index: int=None):
        self.input_frame.add_label(text, index)

    def add_output_label(self, text, index: int=None):
        self.output_frame.add_label(text, index)

    def clear_output(self):
        self.output_frame.clear()

if __name__ == '__main__':
    Application(title=('Application', 'v0.0.1'))
