import tkinter as tk


class Application(tk.Frame):
    def __init__(self, parent, title: (tuple, str)=None):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.header_frame = HeaderFrame(self, title=title)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky='news')

        self.input_frame = InputLabelFrame(self)
        self.input_frame.grid(row=1, column=0, sticky='news')

        self.output_frame = OutputLabelFrame(self)
        self.output_frame.grid(row=1, column=1, sticky='news')

    def add_input_label(self, text, index: int=None):
        self.input_frame.add_label(text, index)

    def add_output_label(self, text, index: int=None):
        self.output_frame.add_label(text, index)


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


class InputLabelFrame(UserLabelFrame):
    def __init__(self, parent, start_command=None, abort_command=None):
        self.parent = parent
        UserLabelFrame.__init__(self, self.parent, text='Input')

        self.abort_button = tk.Button(self, text='Abort', command=abort_command)
        self.add_widget(self.abort_button)

        self.start_button = tk.Button(self, text='Start', command=start_command)
        self.add_widget(self.start_button)

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


class OutputLabelFrame(UserLabelFrame):
    def __init__(self, parent):
        self.parent = parent
        UserLabelFrame.__init__(self, self.parent, text='Output')


if __name__ == '__main__':
    root = tk.Tk()

    app = Application(root, title=('Application', 'v0.0.1'))
    app.grid()

    for i in range(3):
        app.add_input_label(text='input {}------------'.format(i))

    for i in range(4):
        app.add_output_label(text='output {}'.format(i))

    app.add_output_label('inserted output', 1)

    root.mainloop()
