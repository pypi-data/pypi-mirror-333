import os
import sys
from apex.core.calculator.lib.vasp_utils import *
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def setUpModule():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))


def write_poscar(conf):
    ret_poscar_bcc = '''Mo2                                     
   1.0000000000000000     
     3.1623672675177916   -0.0000000000000000   -0.0000000000000000
    -0.0000000000000000    3.1623672675177916   -0.0000000000000000
     0.0000000000000000    0.0000000000000000    3.1623672675177916
   Mo
     2
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.5000000000000000  0.5000000000000000  0.5000000000000000

  0.00000000E+00  0.00000000E+00  0.00000000E+00
  0.00000000E+00  0.00000000E+00  0.00000000E+00
  '''

    ret_poscar_fcc = '''Mo4                                     
   1.0000000000000000     
     4.0038866454866655   -0.0000000000000000   -0.0000000000000000
    -0.0000000000000000    4.0038866454866655   -0.0000000000000000
     0.0000000000000000    0.0000000000000000    4.0038866454866655
   Mo
     4
Direct
  0.0000000000000000  0.0000000000000000  0.0000000000000000
  0.0000000000000000  0.5000000000000000  0.5000000000000000
  0.5000000000000000  0.0000000000000000  0.5000000000000000
  0.5000000000000000  0.5000000000000000  0.0000000000000000

  0.00000000E+00  0.00000000E+00  0.00000000E+00
  0.00000000E+00  0.00000000E+00  0.00000000E+00
  0.00000000E+00  0.00000000E+00  0.00000000E+00
  0.00000000E+00  0.00000000E+00  0.00000000E+00
    '''

    with open("POSCAR", "a") as f:
        if conf == 'bcc':
            f.write(ret_poscar_bcc)
        elif conf == 'fcc':
            f.write(ret_poscar_fcc)
