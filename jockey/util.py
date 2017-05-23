import logging

logger = logging.getLogger('jockey.util')


def apply_limits(value, min_value: float=None, max_value: float=None, pass_if: (bool, str, int)=None):
    if min_value:
        if value < min_value:
            logger.warning('value of {} is less than the required minimum {}'.format(value, min_value))
            return False

    if max_value:
        if value > max_value:
            logger.warning('value of {} is greater than the required maximum {}'.format(value, max_value))
            return False

    if pass_if:
        if value != pass_if:
            logger.warning('value of {} is not the required value of {}'.format(value, pass_if))
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
        logger.debug('adding test "{}({}) to sequence"'.format(test, args))
        self.sequence.append(test)
        self.args.append(args)

    def run_test(self):
        logger.debug('executing sequence {} of {}'.format(self.sequence_index, len(self.sequence)))
        try:
            test_function = self.sequence[self.sequence_index]
            test_args = self.args[self.sequence_index]
        except IndexError:
            logger.warning('test reset required')
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
        logger.info('test sequence reset')
        self.sequence_index = 0
        self.results = list()


def save(data: dict, file_path: str, delimiter='\t'):
    logger.info('saving data point {} to {} using the "{}" delimiter'.format(data, file_path, delimiter))

    header = delimiter.join(data.keys()) + '\n'

    # determine if the header is present and - if not - then print a new header in the file
    header_present = False
    try:
        with open(file_path, 'r') as f:
            if header in f.read():
                header_present = True
    except FileNotFoundError:
        pass

    # append the data to the data file
    with open(file_path, 'a') as f:
        if not header_present:
            logger.debug('proper column headers not found, creating')
            f.write(header)
        else:
            logger.debug('found correct column headers')

        logger.debug('writing data point: {}'.format(data))
        data = delimiter.join([str(v) for _, v in data.items()]) + '\n'
        f.write(data)


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
