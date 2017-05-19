
def apply_limits(value, min_value: float=None, max_value: float=None, pass_if: bool=None):
    if min_value:
        if value < min_value:
            return False

    if max_value:
        if value > max_value:
            return False

    if pass_if:
        if value != pass_if:
            return False

    return True


class TestSequence:
    def __init__(self, sequence: list=None, args: list=None):
        if sequence is not None and args is not None:
            if len(sequence) != len(args):
                raise ValueError('the test sequence and args lists must be of the same length')

        self.sequence = sequence if sequence is not None else list()
        self.results = list()

        if args is None:
            self.args = [None] * len(self.sequence)  # fill args with 'None' of same length as sequence
        else:
            self.args = args

        self.sequence_index = 0

    @property
    def ready(self):
        if self.sequence_index == 0:
            return True
        else:
            return False

    @property
    def complete(self):
        if self.sequence_index >= len(self.sequence):
            return True
        else:
            return False

    def add_test(self, test, args: tuple=None):
        self.sequence.append(test)
        self.args.append(args)

    def run_test(self):
        try:
            test_function = self.sequence[self.sequence_index]
            test_args = self.args[self.sequence_index]
        except IndexError:
            print('!!! test needs to be reset !!!')
            return None

        if test_args is not None:
            results = test_function(*test_args)
        else:
            results = test_function()
        self.results.append(results)

        self.sequence_index += 1

        return results

    def run_sequence(self):
        results = list()

        while not self.complete:
            result = self.run_test()
            results.append(result)

        return results

    def reset(self):
        self.sequence_index = 0
        self.results = list()


if __name__ == '__main__':
    # direct callback injection at initialization, run twice
    callbacks = [lambda: print('1'), lambda: print('2'), lambda: print('3')]
    ts = TestSequence(callbacks)
    ts.run_sequence()
    ts.reset()
    ts.run_sequence()

    # callbacks with args at initialization
    callbacks = [print, print, print]
    args = ['4', '5', '6']
    ts = TestSequence(callbacks, args)
    ts.run_sequence()

    # callbacks added after initialization
    ts = TestSequence()
    ts.add_test(print, ('7',))
    ts.add_test(lambda: print('8'))
    ts.add_test(print, ('9',))
    ts.run_sequence()
