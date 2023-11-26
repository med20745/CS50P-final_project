import pytest
from project import interp

def test_interp():
    assert interp(0.3,'a') == "Pas capable probleme de a"
    assert interp(1.2,"a") == 'Juste capable'
