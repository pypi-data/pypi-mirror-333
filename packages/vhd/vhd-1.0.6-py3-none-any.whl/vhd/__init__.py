from .vhd import _create_fixed_vhd,_read_vhd_footer
__version__ = "1.0.6"
__author__ = "钟阳"

def test():
    print("__int__")
    return 1


def create(filename, size_mb):
    return _create_fixed_vhd(filename, size_mb)

def read(filename):
    return _read_vhd_footer(filename)

