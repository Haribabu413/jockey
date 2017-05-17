import jockey.hardware


def write_daq(output, voltage=None, state=None, save=False, save_column_header=None, override=False, app=None):
    callback = jockey.hardware.write_daq
    args = (output, voltage, state, save, save_column_header, override)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)


def read_daq(input, num_of_points=1, sample_rate=1000,
             min_value=None, max_value=None, pass_if=None,
             save=False, save_column_header=None,
             app=None):
    callback = jockey.hardware.read_daq
    args = (input, num_of_points, sample_rate,
            min_value, max_value, pass_if,
            save, save_column_header)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)
