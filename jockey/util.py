class TestSequence:
    def __init__(self, sequence: list=None, args: list=None):
        if sequence is not None and args is not None:
            if len(sequence) != len(args):
                raise ValueError('the test sequence and args lists must be of the same length')

        self.sequence = sequence if sequence is not None else list()

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
    # direct callback injection at initialization
    callbacks = [lambda: print('1'), lambda: print('2'), lambda: print('3')]
    ts = TestSequence(callbacks)
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
