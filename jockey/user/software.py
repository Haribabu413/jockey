

def wait(wait_time, app=None):
    callback = app.wait
    args = (wait_time,)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)
