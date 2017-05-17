"""
DO NOT CHANGE THE IMPORT
"""
from jockey import *


def setup():
    """
    This is the test setup code and should only contain instances of 'add_user_data'

    :return: None
    """
    print('setup')


def test():
    """
    This is the main body of the test and should contain all of the executable code.

    :return: None
    """
    print('test')


def teardown():
    """
    This block will execute at the end of the test regardless of pass/fail state or errors.  Use it to
    turn off power supplies or perform other tasks that should occur regardless of pass/fail status of the test.

    :return: None
    """
    print('teardown')

'''
---------------------------
DO NOT MESS BELOW THIS LINE
'''
if __name__ == '__main__':
    register_test(setup, test, teardown)
    start_runner()


