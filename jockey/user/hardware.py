"""
Used to provide the scripting hardware interface for the
user.  Each of the functions within this are intended to
be utilized within the user script.
"""

import jockey.hardware


def write_daq(output, device=None, serial_number=None, model=None,
              voltage=None, state=None,
              save=False, save_column_header=None, app=None):

    callback = jockey.hardware.write_daq
    args = (output, device, serial_number, model, voltage, state, save, save_column_header)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)


def read_daq(input, device=None, serial_number=None, model=None,
             num_of_points=1, sample_rate=1000,
             min_value=None, max_value=None, pass_if=None,
             save=False, save_column_header=None,
             app=None):
    callback = jockey.hardware.read_daq
    args = (input, device, serial_number, model,
            num_of_points, sample_rate,
            min_value, max_value, pass_if,
            save, save_column_header)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)
