import tkinter as tk
import os
import datetime
import tk_tools


class HeaderFrame(tk.Frame):
    def __init__(self, parent, title: (tuple, str)=None):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        if title is not None:
            if isinstance(title, str):
                self.title = tk.Label(self, text=title, font=("Helvetica", 18))
                self.title.pack(expand=True)
            elif isinstance(title, tuple):
                self.title = tk.Label(self, text=title[0], font=("Helvetica", 18))
                self.title.pack(expand=True)
                self.subtitle = tk.Label(self, text=title[1], font=("Helvetica", 12))
                self.subtitle.pack(expand=True)

        # todo: implement logo


class UserLabelFrame(tk.LabelFrame):
    def __init__(self, parent, text):
        self.parent = parent
        tk.LabelFrame.__init__(self, self.parent, text=text)

        self.widgets = list()

    def add_widget(self, widget: tk.Widget, index: int=None):
        if index is None:
            self.widgets.append(widget)
        else:
            self.widgets.insert(index, widget)

        for widget in self.widgets:
            widget.pack_forget()
            widget.pack(fill='x')

    def add_label(self, text, index: int=None):
        label = tk.Label(self, text=text)
        self.add_widget(label, index=index)

    def add_button(self, text, command=None, index: int=None):
        button = tk.Button(self, text=text, command=command)
        self.add_widget(button, index)

    def clear(self):
        for widget in self.widgets:
            widget.pack_forget()
            widget.destroy()

        self.widgets = list()


class InputLabelFrame(UserLabelFrame):
    def __init__(self, parent, start_command=None, abort_command=None, entries: list=None):
        self.parent = parent
        UserLabelFrame.__init__(self, self.parent, text='Input')

        btn_font = ('Courier New', 14, 'bold')
        self.abort_button = tk.Button(self, text='Abort', command=abort_command, foreground='red', font=btn_font)
        self.add_widget(self.abort_button)

        self.start_button = tk.Button(self, text='Start', command=start_command, foreground='green', font=btn_font)
        self.add_widget(self.start_button)

        if entries is not None:
            self.inputs = tk_tools.KeyValueEntry(self, keys=entries)
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

        for widget in self.widgets:
            widget.pack_forget()
            widget.pack(fill='x')

    def enable(self):
        self.start_button['state'] = 'normal'

    def disable(self):
        self.start_button['state'] = 'disabled'

    def add_entries(self, entries):
        if self.inputs is not None:
            print('warning: there is already one instance of key: value entries in the input frame')
            return

        self.inputs = tk_tools.KeyValueEntry(self, keys=entries)
        self.add_widget(self.inputs)

    def get_user_inputs(self):
        return self.inputs.get() if self.inputs is not None else None

    def clear_entries(self):
        self.inputs.reset()


class OutputLabelFrame(UserLabelFrame):
    def __init__(self, parent):
        self.parent = parent
        UserLabelFrame.__init__(self, self.parent, text='Output')

    def create_table(self, headers=None):
        table = tk_tools.LabelGrid(self, 2, headers=headers)
        self.add_widget(table)

    def add_to_table(self, label, value):
        table = None
        for e in self.widgets:
            if isinstance(e, tk_tools.LabelGrid):
                table = e
                break

        if table is not None:
            table.add_row([label, value])

    def clear(self):
        for widget in self.widgets:
            if not isinstance(widget, tk_tools.LabelGrid):
                widget.pack_forget()
                widget.destroy()
            else:
                widget.clear()

        self.widgets = [w for w in self.widgets if isinstance(w, tk_tools.LabelGrid)]


class StatusBar(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.executing_label = tk.Label(self, text='Idle', font='Ariel 10 bold')
        self.executing_label.pack(side='left', expand=True, fill=tk.X)

        self.status_label = tk.Label(self, text='Idle', font='Ariel 12 bold')
        self.status_label.pack(side='left', expand=True, fill=tk.X)

        self.datetime_label = tk.Label(self, text='-', font='Ariel 10 bold')
        self.datetime_label.pack(side='left', expand=True, fill=tk.X)

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
        dt_str = datetime.datetime.strftime(dt, '%Y-%m-%d %H:%M')
        self.datetime_label['text'] = dt_str

        return dt_str

if __name__ == '__main__':
    root = tk.Tk()

    ilf = StatusBar(root)
    ilf.grid()

    root.mainloop()
