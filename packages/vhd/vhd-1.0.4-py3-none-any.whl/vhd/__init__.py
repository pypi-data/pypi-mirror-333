from .vhd import create_fixed_vhd,read_vhd_footer
__version__ = "1.0.4"
__author__ = "Zhong Yang"

def test():
    print("__int__")
    return 1


def create(filename, size_mb):
    return create_fixed_vhd(filename, size_mb)

def read(filename):
    return read_vhd_footer(filename)

