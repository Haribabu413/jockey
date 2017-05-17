"""
DO NOT CHANGE THE IMPORT
"""
from jockey import *
import time

app = Application(title=('Jockey Application', 'v0.0.0'))


def setup():
    """
    This is the test setup code.  Any code entered here should be intended to execute one time
    at application instantiation.  As such, you should only set power supplies, daqs, etc, into
    their initial state.  Since we are not manipulating the GUI, hardware manipulations should
    not pass the 'app' argument within this function

    :return: None
    """
    print('setup')


def test():
    """
    This is the main body of the test and should contain all of the executable code.  All manipulations
    within this body should pass the 'app' parameter in order to be properly added to the test queue.

    :return: None
    """
    write_daq_ao(1.25, 'ai0', app=app)


def teardown():
    """
    This block will execute at the end of the test regardless of pass/fail state or errors.  Use it to
    turn off power supplies or perform other tasks that should occur regardless of pass/fail status of the test.

    :return: None
    """
    write_daq_ao(0, 'ai0')


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
