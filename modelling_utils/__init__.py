__version__ = '0.2.1'
__author__ = "Diogo André"
__date__ = "2022-05-05"
__annotations__ = "Utility functions and data structure for Analog Integrated Circuit Modelling"
from .utils import *
from .read import *
from .write import *
from .data import *

def verbose_info():
    print(f"{__name__}")
    print(f"Version:        {__version__} ({__date__})")
    print(f"Author:         {__author__}")
    print(f"Description:    {__annotations__}")