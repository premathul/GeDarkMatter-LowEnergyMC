import numpy as np
from gedm_mc.core import sample_exponential_recoils, apply_threshold, efficiency_logistic

def test_reproducible():
    a=sample_exponential_recoils(5,10,rng=1)
    b=sample_exponential_recoils(5,10,rng=1)
    assert np.allclose(a,b)

def test_threshold():
    assert np.all(apply_threshold([1,2,3],2)>=2)

def test_efficiency_midpoint():
    assert np.isclose(efficiency_logistic([50],50,5)[0],0.5)
