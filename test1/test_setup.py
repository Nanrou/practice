
from distutils.core import setup
import py2exe

setup(
    
    windows=["calculate_flow.py"],
    data_files = [("icos",['icos/cat.ico',]),]

    )