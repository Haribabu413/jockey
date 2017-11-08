"""
The functions within this file are intended
for use within the user script and each will
generally perform some action that is noticable
by a user from the GUI
"""
from jockey.user.app import Application


def add_input_label(text, app: Application):
    """
    Adds a label and entry into the user input portion of the application.

    :param text: the text of the input field and the key under which the data is saved
    :param app: an instance of the user application
    :return:
    """
    app.add_input_label(text)


def wait(wait_time: (int, float), app: Application):
    """
    Adds a wait step between two steps

    :param wait_time:
    :param app:
    :return:
    """
    callback = app.wait
    args = (wait_time,)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)

