# Dynamically retrieve version from setuptools-scm
try:
    from ._version import version as __version__
except ModuleNotFoundError:
    __version__ = "dev"  # Fallback for development mode

# Print a message when the package is imported
print(f"📖 scia {__version__} - For Documentation, visit: xxx")


from .data import create_scd
from .fill_missing import fill_missing
from .filter import subset_scd
from .io import read_scd, write_scd
from .ird import ird
from .pand import pand
from .pem import pem
from .pet import pet
from .plm import plm
from .pnd import pnd
from .preprocess import prepare_scd
from .recombine import recombine_phases
from .select import select_cases
from .smd import smd
from .summary import summary_scd
from .tau_u import tau_u
from .utils import revise_names
from .autocorr import autocorr
from .corrected_tau import corrected_tau
from .nap import nap
from .overlap import overlap
from .select import select_cases


