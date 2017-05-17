import tkinter as tk


class Application(tk.Frame):
    def __init__(self, parent, title: (tuple, str)=None):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.header_frame = HeaderFrame(self, title=title)
        self.header_frame.grid(row=0, column=0, columnspan=2)

        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=1, column=0)

        self.input_frame = OutputFrame(self)
        self.input_frame.grid(row=1, column=1)


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


class InputFrame(tk.LabelFrame):
    def __init__(self, parent):
        self.parent = parent
        tk.LabelFrame.__init__(self, self.parent, text='Input')

        self.label = tk.Label(self, text='some text')
        self.label.grid()


class OutputFrame(tk.LabelFrame):
    def __init__(self, parent):
        self.parent = parent
        tk.LabelFrame.__init__(self, self.parent, text='Output')

        self.label = tk.Label(self, text='some text')
        self.label.grid()

if __name__ == '__main__':
    root = tk.Tk()

    Application(root, title=('Application', 'v0.0.1')).grid()

    root.mainloop()
