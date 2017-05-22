import tkinter as tk
import time
import os
import logging
from collections import OrderedDict

from jockey.gui import HeaderFrame, InputLabelFrame, OutputLabelFrame, StatusBar
from jockey.util import TestSequence, save


logger = logging.getLogger()


class Application:
    def __init__(self, title: (tuple, str), save_path: str='results.txt'):
        # initialize the test sequences
        self.test_sequence = TestSequence()
        self.teardown = None
        self.save_path = save_path
        self.aborted = False

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

        self.input_frame = InputLabelFrame(self.root,
                                           start_command=self.start_btn_pressed,
                                           abort_command=self.abort_btn_pressed)
        self.input_frame.grid(row=1, column=0, sticky='news')

        self.output_frame = OutputLabelFrame(self.root)
        self.output_frame.grid(row=1, column=1, sticky='news')
        self.output_frame.create_table()

        self.status_bar = StatusBar(self.root)
        self.status_bar.grid(row=2, column=0, columnspan=2, sticky='news')

        icon_path = os.path.join(os.path.abspath(__file__), '../../img/jockey.ico')
        self.root.iconbitmap(icon_path)

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
        print('-------------')
        if not self.user_inputs_filled:
            print('user inputs not filled out')
            return

        self.status_bar.datetime()
        self.status_bar.executing('Running test sequence')
        self.status_bar.status('Pending')

        self.test_sequence.reset()
        self.input_frame.disable()
        self.output_frame.clear()
        self.aborted = False

        # allow time for the button to disable before beginning the test sequence
        self.root.after(150, self.run_test)

    def abort_btn_pressed(self):
        print('!!! ABORTED !!!')
        self.aborted = True

    def run_test(self):
        if not self.aborted:
            result = self.test_sequence.run_test()
            if result.get('save_column_header') is not None:
                status = 'pass' if result.get('pass') else 'fail'
                self.output_frame.add_to_table(result.get('save_column_header'),
                                               result.get('value'),
                                               status)
            if result.get('pass') is False:
                self.status_bar.status('Fail')

            # continue adding the next test sequence for
            # as long as the test is not completed
            if not self.test_sequence.complete:
                self.root.after(100, self.run_test)
            else:
                self.teardown()
                self.process_results()
                self.input_frame.clear_entries()
                self.test_sequence.reset()
                self.input_frame.enable()

                self.status_bar.executing('Test complete')
        else:
            self.teardown()
            self.input_frame.enable()

    def wait(self, wait_time):
        increment = 0.1
        total = 0.0
        while total < wait_time:
            time.sleep(increment)
            total += increment
            self.root.update()

            if self.aborted:
                break

        return {}

    def process_results(self):
        user_inputs = self.input_frame.get_user_inputs()
        test_results = self.test_sequence.results

        dt_str = self.status_bar.datetime()

        data = OrderedDict()
        data['datetime'] = dt_str

        # collect the user inputs and the test results into a single uniform dictionary
        header_list = [user_input for user_input in user_inputs.keys()]
        header_list.sort()
        for header in header_list:
            data[header] = user_inputs[header]

        test_passed = True
        for result in test_results:
            if result.get('save') is True:
                header = result.get('save_column_header')
                value = result.get('value')
                data[header] = value

            if result.get('pass') is False:
                test_passed = False

        if test_passed:
            self.status_bar.status('Pass')
        data['pass'] = test_passed

        save(data, self.save_path)

    def add_input_label(self, text, index: int=None):
        self.input_frame.add_label(text, index)

    def add_user_inputs(self, input_labels: list):
        self.input_frame.add_entries(input_labels)

    @property
    def user_inputs_filled(self):
        filled = True
        for key, value in self.input_frame.get_user_inputs().items():
            if value is '':
                filled = False
                break
        return filled

    def add_output_label(self, text, index: int=None):
        self.output_frame.add_label(text, index)


if __name__ == '__main__':
    Application(title=('Application', 'v0.0.1'))
