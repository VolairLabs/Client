## k4modev
import traceback



import warnings
# Suppress the deprecation warning from the cryptography module.
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import cryptography


try:
    from .core import Volair
    from .core import start_location
    from .core import HASHES
    from .core import Volair_Serial

except:
    pass

from .remote import localimport
from .remote import Volair_On_Prem, Tiger, Tiger_Admin, VolairOnPrem
from .remote import no_exception
from .remote import requires
from .remote import encrypt
from .remote import decrypt
from .remote import Volair_serializer
from .remote import interface


open_databases = {}

__version__ = '0.34.3'  # fmt: skip
