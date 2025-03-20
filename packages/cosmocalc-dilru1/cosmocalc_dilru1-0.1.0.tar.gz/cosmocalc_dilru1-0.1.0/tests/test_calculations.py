# tests/test_calculations.py

import pytest
from cosmocalc.calculations import hubble_parameter

def test_hubble_parameter():
    H0 = 70  # km/s/Mpc
    z = 1
    omega_m = 0.3
    omega_lambda = 0.7
    
    expected = 70 * ((0.3 * (1 + 1)**3 + 0.7)**0.5)
    assert hubble_parameter(H0, z, omega_m, omega_lambda) == pytest.approx(expected)
