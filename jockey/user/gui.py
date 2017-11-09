import tkinter as tk
import datetime
import logging
import tk_tools

from jockey.images import btn_start, btn_abort

logger = logging.getLogger(__name__)


class HeaderFrame(tk.Frame):
    def __init__(self, parent, title: str=None, subtitle: str=None):
        self.parent = parent
        super().__init__(self.parent)

        if title is not None:
            self.title = tk.Label(self, text=title, font=("Helvetica", 18))
            self.title.grid(sticky='ew')

        if subtitle is not None:
            self.subtitle = tk.Label(self, text=subtitle, font=("Helvetica", 12))
            self.subtitle.grid(sticky='ew')

        # todo: implement logo


class UserLabelFrame(tk.LabelFrame):
    def __init__(self, parent, text):
        self.parent = parent
        super().__init__(self.parent, text=text)

        self.widgets = list()

    def add_widget(self, widget: tk.Widget, index: int=None):
        if index is None:
            logger.debug('adding widget {}'.format(widget))
            self.widgets.append(widget)
        else:
            logger.debug('adding widget {} at index {}'.format(widget, index))
            self.widgets.insert(index, widget)

        for i, widget in enumerate(self.widgets):
            widget.grid_forget()
            widget.grid(row=i, sticky='ew')

    def add_label(self, text, index: int=None):
        label = tk.Label(self, text=text)
        self.add_widget(label, index=index)

    def add_button(self, text, command=None, index: int=None):
        button = tk.Button(self, text=text, command=command)
        self.add_widget(button, index)

    def clear(self):
        for widget in self.widgets:
            widget.grid_forget()
            widget.destroy()

        self.widgets = list()


class InputLabelFrame(UserLabelFrame):
    def __init__(self, parent, start_command=None, abort_command=None, entries: list=None):
        self.parent = parent
        super().__init__(self.parent, text='User Inputs')

        self.start_command = start_command

        # create the images and image items for the buttons
        self.abort_image = tk.PhotoImage(data=btn_abort).subsample(2)
        self.start_image = tk.PhotoImage(data=btn_start).subsample(2)

        # create the buttons
        self.abort_button = tk.Button(self, image=self.abort_image, command=abort_command)
        self.add_widget(self.abort_button)

        self.start_button = tk.Button(self, image=self.start_image, command=self.start_command)
        self.add_widget(self.start_button)

        if entries is not None:
            self.inputs = tk_tools.KeyValueEntry(self, keys=entries, on_change_callback=self.start_command)
            self.add_widget(self.inputs)

        else:
            self.inputs = None

    def add_widget(self, widget: tk.Widget, index: int=None):
        # modify the index so that the start and abort
        # buttons are always at the end of the list
        if index is None:
            self.widgets.insert(-2, widget)
        else:
            self.widgets.insert(index, widget)

        for i, widget in enumerate(self.widgets):
            widget.grid_forget()
            widget.grid(row=i, sticky='ew')

    def enable(self):
        self.start_button['state'] = 'normal'

    def disable(self):
        self.start_button['state'] = 'disabled'

    def add_entries(self, entries):
        if self.inputs is not None:
            print('warning: there is already one instance of key: value entries in the input frame')
            return

        self.inputs = tk_tools.KeyValueEntry(self, keys=entries, on_change_callback=self.start_command)
        self.add_widget(self.inputs)

    def get_user_inputs(self):
        return self.inputs.get() if self.inputs is not None else None

    def clear_entries(self):
        self.inputs.reset()


class OutputLabelFrame(UserLabelFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent, text='Test Outputs')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.led = tk_tools.Led(self)
        self.led.to_green()
        self.led.grid(row=1, column=0, sticky='s')

    def create_table(self, headers=None):
        table = tk_tools.LabelGrid(self, 3, headers=headers)
        self.add_widget(table)

    def add_to_table(self, label, value, status):
        table = None
        for e in self.widgets:
            if isinstance(e, tk_tools.LabelGrid):
                table = e
                break

        if table is not None:
            table.add_row([label, value, status])

    def clear(self):
        self.led.to_yellow(True)

        for widget in self.widgets:
            if not isinstance(widget, tk_tools.LabelGrid):
                widget.grid_forget()
                widget.destroy()
            else:
                widget.clear()

        self.widgets = [w for w in self.widgets if isinstance(w, tk_tools.LabelGrid)]

    def to_pass(self):
        self.led.to_green(True)

    def to_fail(self):
        self.led.to_red(True)


class StatusBar(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.executing_label = tk.Label(self, text='Idle', font='Ariel 10 bold', relief=tk.SUNKEN)
        self.executing_label.grid(row=0, column=0, sticky='news')

        self.status_label = tk.Label(self, text='Idle', font='Ariel 12 bold', relief=tk.SUNKEN)
        self.status_label.grid(row=0, column=1, sticky='news')

        self.datetime_label = tk.Label(self, text='-', font='Ariel 10 bold', relief=tk.SUNKEN)
        self.datetime_label.grid(row=0, column=2, sticky='news')

        self.default_fg_color = self.status_label.cget('foreground')
        self.default_bg_color = self.status_label.cget('background')

    def executing(self, text: str):
        self.executing_label['text'] = text

    def status(self, text: str):
        if text.lower() in ['fail', 'f']:
            self.status_label['foreground'] = 'red'
            self.status_label['background'] = self.default_bg_color

        elif text.lower() in ['pass', 'p']:
            self.status_label['foreground'] = 'green'
            self.status_label['background'] = self.default_bg_color

        elif text.lower() in ['pending', 'testing', 'test']:
            self.status_label['foreground'] = 'black'
            self.status_label['background'] = 'yellow'

        else:
            self.status_label['foreground'] = self.default_fg_color
            self.status_label['background'] = self.default_bg_color

        self.status_label['text'] = text

    def datetime(self):
        dt = datetime.datetime.now()
        dt_str = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
        self.datetime_label['text'] = dt_str

        return dt_str


if __name__ == '__main__':
    root = tk.Tk()

    ilf = StatusBar(root)
    ilf.grid()

    root.mainloop()
