from subdue import daqmx
import time


def _parse_daq_string(daq_string):
    elements = daq_string.split('/')

    if 'Dev' in elements[0]:
        daq = elements.pop(0)
    else:
        daq = None

    port = elements.pop(0)
    pin = elements.pop(0)

    return daq, port, pin


def _get_daq_hardware(daq_string):
    if daq_string is not None:
        daq = daqmx.NIDAQmx(device_name=daq_string)
    else:
        searcher = daqmx.NIDAQmxSearch()
        device_name = searcher.list_devices()[0]
        daq = daqmx.NIDAQmx(device_name=device_name)

    return daq


def write_daq(output, voltage=None, state=None,
              save=False, save_column_header=None, override=False):
    print('writing to daq {}: {}/{}'.format(output, voltage, state))

    daq_str, port_str, pin_str = _parse_daq_string(output)
    daq = _get_daq_hardware(daq_str)
    line = port_str + pin_str

    if 'ao' in line:
        daq.analog_out(line, voltage)
    elif 'port' in line and 'line' in line:
        daq.digital_out_line(port_str, pin_str, state)
    else:
        raise ValueError('incorrect "output" parameter')


def read_daq(input, num_of_points=1, sample_rate=1000,
                min_value=None, max_value=None, pass_if=None,
                save=False, save_column_header=None):

    daq_str, port_str, pin_str = _parse_daq_string(input)

    daq = _get_daq_hardware(daq_str)
    line = port_str + pin_str

    if 'ai' in line:
        return daq.sample_analog_in(line, sample_count=num_of_points, rate=sample_rate)
    elif 'port' in line and 'line' in line:
        return daq.digital_in_line(port_str, pin_str)
    else:
        raise ValueError('incorrect "input" parameter')

