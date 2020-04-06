import math
from math import pi

def deltaR(eta1, phi1, eta2, phi2):
    dphi = (phi1-phi2)
    dphi -= int(dphi / pi)*pi
    return math.sqrt((eta1-eta2)**2 + dphi**2)
