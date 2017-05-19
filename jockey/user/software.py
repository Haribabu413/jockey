

def add_input_label(text, app):
    app.add_input_label(text)


def add_entry(key, value, app):
    app.add_entry(key, value)


def wait(wait_time, app=None):
    callback = app.wait
    args = (wait_time,)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)

