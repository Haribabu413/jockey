import tkinter as tk


class Application(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        self.label = tk.Label(self, text='some text')
        self.label.grid()

if __name__ == '__main__':
    root = tk.Tk()

    Application(root).grid()

    root.mainloop()
