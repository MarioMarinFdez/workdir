import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.utilidades import conectar

def test_conectar_devuelve_true():
    assert conectar() == True
