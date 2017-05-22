from subdue import daqmx
from jockey.util import apply_limits


def _parse_daq_string(daq_string):
    elements = daq_string.split('/')

    if 'Dev' in elements[0]:
        daq = elements.pop(0)
    else:
        daq = None

    port = elements.pop(0)
    pin = elements.pop(0)

    return daq, port, pin


def _get_daq_hardware(device=None, serial_number=None, model=None):
    if device is not None or serial_number is not None or model is not None:
        if device is not None:
            daq = daqmx.NIDAQmx(device_name=device)
        elif serial_number is not None:
            daq = daqmx.NIDAQmx(serial_number=serial_number)
        elif model is not None:
            raise NotImplementedError('the DAQ cannot be currently allocated based on a model number')
    else:
        searcher = daqmx.NIDAQmxSearch()
        device_name = searcher.list_devices()[0]
        daq = daqmx.NIDAQmx(device_name=device_name)

    return daq


def _append_limits(result_dict, min_value, max_value, pass_if):
    if min_value is not None:
        result_dict['min_value'] = min_value

    if max_value is not None:
        result_dict['min_value'] = max_value

    if pass_if is not None:
        result_dict['min_value'] = pass_if


def write_daq(output, device=None, serial_number=None, model=None,
              voltage=None, state=None,
              save=False, save_column_header=None):
    print('writing to {}: {}/{}'.format(device, output, voltage, state))

    daq_str, port_str, pin_str = _parse_daq_string(output)
    daq = _get_daq_hardware(device, serial_number, model)
    line = port_str + pin_str

    result = {'save': save, 'save_column_header': save_column_header, 'device': output}
    if 'ao' in line:
        daq.analog_out(line, voltage)
        result['value'] = voltage

    elif 'port' in line and 'line' in line:
        daq.digital_out_line(port_str, pin_str, state)
        result['value'] = state
    else:
        raise ValueError('incorrect "output" parameter')

    return result


def read_daq(input, device=None, serial_number=None, model=None,
             num_of_points=1, sample_rate=1000,
             min_value=None, max_value=None, pass_if=None,
             save=False, save_column_header=None):

    daq_str, port_str, pin_str = _parse_daq_string(input)

    daq = _get_daq_hardware(device, serial_number, model)
    line = port_str + pin_str

    result = {'save': save, 'save_column_header': save_column_header, 'device': input}
    _append_limits(result, min_value, max_value, pass_if)

    if 'ai' in line:
        samples = daq.sample_analog_in(line, sample_count=num_of_points, rate=sample_rate)
        avg = sum(samples) / len(samples)
        value = round(avg, 2)

        result['value'] = value
        result['pass'] = apply_limits(result['value'], min_value, max_value, pass_if)

    elif 'port' in line and 'line' in line:
        value = daq.digital_in_line(port_str, pin_str)
        result['value'] = value
        result['pass'] = apply_limits(result['value'], min_value, max_value, pass_if)

    else:
        raise ValueError('incorrect "input" parameter')

    return result

