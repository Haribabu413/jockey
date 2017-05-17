

# these are the tests that are intended to be re-defined by the user
def _user_test_setup():
    print('warning: setup undefined by user')


def _user_test_test():
    print('warning: setup undefined by user')


def _user_test_teardown():
    print('warning: setup undefined by user')


def register_test(setup_callback=None, test_callback=None, teardown_callback=None):
    global _user_test_setup, _user_test_test, _user_test_teardown

    if setup_callback is not None:
        _user_test_setup = setup_callback

    if test_callback is not None:
        _user_test_test = test_callback

    if teardown_callback is not None:
        _user_test_teardown = teardown_callback


def start_runner():
    _user_test_setup()
    _user_test_test()
    _user_test_teardown()

