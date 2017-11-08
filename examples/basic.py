"""
DO NOT CHANGE THE IMPORT
"""
from jockey import *

# creates an instance of the Application
app = Application(title='Sample Jockey Application', subtitle=__version__, save_path='save.csv')


def setup():
    """
    This is the test setup code.  Any code entered here should be intended to execute one time
    at application instantiation.  As such, you should only set power supplies, daqs, etc, into
    their initial state.  Since we are not manipulating the GUI, hardware manipulations should
    not pass the 'app' argument within this function

    :return: None
    """
    write_daq(device='Dev1', output='ao/0', voltage=0)  # set an initial condition

    app.add_input_label('Some custom text!')  # this is how you might add custom labeling to the inputs
    app.add_input_label('test v1.2')  # this is how you might add custom labeling to the inputs

    app.add_user_inputs('serial number')  # this is how you would add user input values

    app.add_input_label('add more text if you want')  # this is how you might add custom labeling to the inputs


def test():
    """
    This is the main body of the test and should contain all of the executable code.  All manipulations
    within this body should pass the 'app' parameter in order to be properly added to the test queue.

    :return: None
    """
    write_daq(device='Dev1', output='ao/0', voltage=1.25, app=app)
    wait(0.5, app=app)
    read_daq(device='Dev1', input='ai/0', max_value=2, app=app)
    read_daq(device='Dev1', input='port0/line2', pass_if=True, save=True, save_column_header='port0/line2', app=app)
    read_daq(device='Dev1', input='port0/line4', pass_if=False, save=True, save_column_header='port0/line4', app=app)


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
