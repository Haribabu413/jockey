import logging

from jockey.user.app import Application
from jockey.user.hardware import write_daq, read_daq
from jockey.user.software import add_input_label, add_entry, wait

from jockey.version import __version__

__all__ = ['__version__', 'Application', 'write_daq', 'read_daq', 'add_input_label', 'add_entry', 'wait']

logger = logging.getLogger('jockey')
logging.basicConfig(level=logging.DEBUG)
