

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


class TestSequence:

    def __init__(self, sequence: list=None, args: list=None):
        self.sequence = sequence

        if args is None:
            self.args = [None] * len(self.sequence)  # fill args with 'None' of same length as sequence
        else:
            self.args = args

        self.sequence_index = 0

    def add_test(self, test, args: tuple=None):
        self.sequence.append(test)
        self.args.append(args)

    def run_test(self):
        test_function = self.sequence[self.sequence_index]
        test_args = self.args[self.sequence_index]

        if test_args is not None:
            results = test_function(*test_args)
        else:
            results = test_function()

        self.sequence_index += 1

        if self.sequence_index >= len(self.sequence):
            raise IndexError

        return results

    def run_sequence(self):
        results = list()

        while True:
            try:
                result = self.run_test()
                results.append(result)
            except IndexError:
                break

        return results

if __name__ == '__main__':
    callbacks = [lambda: print('1'), lambda: print('2'), lambda: print('3')]

    ts = TestSequence(callbacks)
    ts.run_sequence()

    callbacks = [print, print, print]
    args = ['4', '5', '6']

    ts = TestSequence(callbacks, args)
    ts.run_sequence()
