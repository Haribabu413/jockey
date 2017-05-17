import subdue
import time


def write_daq_ao(voltage, output, save=False, save_column_header=None, override=False):
    print('writing to daq {}: {}'.format(output, voltage))
    time.sleep(1.0)
