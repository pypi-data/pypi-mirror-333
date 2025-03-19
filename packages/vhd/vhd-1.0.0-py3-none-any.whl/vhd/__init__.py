from .vhd import create_fixed_vhd
__version__ = "1.0.0"
__author__ = "Zhong Yang"

def test():
    print("__int__")
    return 1


def create(filename, size_mb):
    create_fixed_vhd(filename, size_mb)