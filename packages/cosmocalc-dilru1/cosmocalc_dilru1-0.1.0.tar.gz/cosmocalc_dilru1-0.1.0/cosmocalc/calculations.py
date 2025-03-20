# cosmocalc/calculations.py

import math

def hubble_parameter(H0, z, omega_m, omega_lambda):
    """
    Calculates the Hubble parameter at redshift z.
    
    H0: Hubble constant today (km/s/Mpc)
    z: Redshift
    omega_m: Matter density parameter
    omega_lambda: Dark energy density parameter
    """
    omega_k = 1.0 - omega_m - omega_lambda
    return H0 * math.sqrt(omega_m * (1 + z)**3 + omega_k * (1 + z)**2 + omega_lambda)
