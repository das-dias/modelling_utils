__name__ = "SAR assisted Pipeline ADC's Temperature-Insensitive Residue Amplifier Modelling"
__version__ = '0.1.0'
__author__ = "Diogo André"
__date__ = "2022-05-05"
__annotations__ = "Residue Amplifier Modelling Scripts and other Analog IC shenanigans"
from .utils import *
from .read import *
from .write import *
from .device import *
from .amplifier import *

def verbose_info():
    print(f"{__name__}")
    print(f"Version:        {__version__} ({__date__})")
    print(f"Author:         {__author__}")
    print(f"Description:    {__annotations__}")
verbose_info()    