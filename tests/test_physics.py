import numpy as np
from gedm_mc.kinematics import max_recoil_energy_ev, minimum_speed_m_s
from gedm_mc.response import gaussian_response_matrix, apply_response
from gedm_mc.statistics import asimov_significance

def test_recoil_inverse_kinematics():
    mchi=10.0; mge=67.7; v=220e3
    e=max_recoil_energy_ev(mchi,mge,v)
    vmin=minimum_speed_m_s(e,mchi,mge)
    assert np.isclose(vmin,v,rtol=1e-12)

def test_response_conserves_counts():
    grid=np.linspace(0,100,101)
    r=gaussian_response_matrix(grid,grid,5)
    x=np.ones(grid.size)
    assert np.isclose(apply_response(x,r).sum(),x.sum())

def test_significance_positive():
    assert asimov_significance([5,3],[10,10])>0
