import sys
sys.path.insert(0, "..")    #look for "chemparse" module in the directory ".." in the first place
import pytest, chemparse, os
print(f"{os.path.basename(__file__)}:\nLoading module {chemparse.__file__}")
from typing import Tuple, Dict, List

species:List[Tuple[str,Dict[str,int]]] = [
    ("CH3",{"C":1, "H":3}),
    ("Ga(CH3)3",{"Ga":1,"C":3, "H":9}),
    ("In(CH3)3",{"In":1,"C":3, "H":9}),
    ("Al(CH3)2NH2",{"Al":1,"C":2,"H":8,"N":1}),
    ("CH3NHHNCH3", {"C":2, "H":8, "N":2}),
    ("(CH3)2NH(HN)3CH3", {"C":3, "H":13, "N":4}),
    ("BaKBi1O3",{'Ba': 1, 'K': 1, 'Bi': 1, 'O': 3}),
    ("Al(Succ)+",{'+': 1, 'Al': 1, 'Succ': 1}),

    ("((CH3)2)3",{'C': 6, 'H': 18}),
    ("(((CH3)2)3)4",{'C': 24, 'H': 72}),
    ("(Al(Ga2O)5)3",{'Al': 3, 'O': 15, 'Ga': 30}),
    ("((CH3)2)3NH3",{'C': 6, 'N': 1, 'H': 21}),
    ("(Al(Ga2O3)5)3((CH3)2)3NH3",{'O': 45, 'Al': 3, 'H': 21, 'N': 1, 'C': 6, 'Ga': 30}),
    ("(Al(Ga2O3)5)3NH3((CH3)2)3",{'O': 45, 'Al': 3, 'H': 21, 'N': 1, 'C': 6, 'Ga': 30}),
    ("K4[Fe(SCN)6]",{'S': 6, 'K': 4, 'N': 6, 'C': 6, "Fe":1}),
    ("K4[Fe(SCN)6]2",{'S': 12, 'K': 4, 'N': 12, 'C': 12, "Fe":2}),
]

def test_chemparse(formula:str, expected:Dict[str,int]):
    assert chemparse.parse_formula(formula) == expected

def pytest_generate_tests (metafunc:pytest.Metafunc):
    metafunc.parametrize("formula,expected", species)