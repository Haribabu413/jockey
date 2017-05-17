import jockey.hardware


def write_daq_ao(voltage, output, save=False, save_column_header=None, override=False, app=None):
    callback = jockey.hardware.write_daq_ao
    args = (voltage, output, save, save_column_header, override)

    if app is None:
        callback(*args)
    else:
        app.add_test(callback, args)
