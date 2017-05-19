"""
DO NOT CHANGE THE IMPORT
"""
from jockey import *

app = Application(title=('Jockey Application', 'v0.0.0'), save_path='save.csv')


def setup():
    """
    This is the test setup code.  Any code entered here should be intended to execute one time
    at application instantiation.  As such, you should only set power supplies, daqs, etc, into
    their initial state.  Since we are not manipulating the GUI, hardware manipulations should
    not pass the 'app' argument within this function

    :return: None
    """
    write_daq(device='Dev1', output='ao/0', voltage=0)


def test():
    """
    This is the main body of the test and should contain all of the executable code.  All manipulations
    within this body should pass the 'app' parameter in order to be properly added to the test queue.

    :return: None
    """
    write_daq(device='Dev1', output='ao/0', voltage=1.25, app=app)
    read_daq(device='Dev1', input='ai/0', max_value=1, app=app)
    read_daq(device='Dev1', input='port0/line1', pass_if=True, save_column_header='port0/line1', app=app)


def teardown():
    """
    This block will execute at the end of the test regardless of pass/fail state or errors.  Use it to
    turn off power supplies or perform other tasks that should occur regardless of pass/fail status of the test.

    :return: None
    """
    write_daq(device='Dev1', output='ao/0', voltage=0)


def custom_function():
    """
    You can create your own custom functions and execute them as part of the test sequence

    :return:
    """
    pass

'''
---------------------------
DO NOT MESS BELOW THIS LINE
'''
if __name__ == '__main__':
    app.register_tests(setup, test, teardown)
    app.run()
