import numpy as np

C_M_S = 299792458.0
EV_PER_GEV = 1e9

def reduced_mass_gev(m_chi_gev, m_nucleus_gev):
    if m_chi_gev<=0 or m_nucleus_gev<=0:
        raise ValueError("masses must be positive")
    return m_chi_gev*m_nucleus_gev/(m_chi_gev+m_nucleus_gev)

def max_recoil_energy_ev(m_chi_gev, m_nucleus_gev, speed_m_s):
    """Elastic two-body maximum nuclear recoil energy."""
    if speed_m_s<0:
        raise ValueError("speed must be nonnegative")
    mu=reduced_mass_gev(m_chi_gev,m_nucleus_gev)
    beta=speed_m_s/C_M_S
    return 2*mu**2*beta**2/m_nucleus_gev*EV_PER_GEV

def minimum_speed_m_s(recoil_ev, m_chi_gev, m_nucleus_gev):
    """Minimum incident speed for an elastic recoil of energy E_R."""
    er=np.asarray(recoil_ev,float)/EV_PER_GEV
    if np.any(er<0): raise ValueError("recoil energy must be nonnegative")
    mu=reduced_mass_gev(m_chi_gev,m_nucleus_gev)
    beta=np.sqrt(m_nucleus_gev*er/(2*mu**2))
    return beta*C_M_S
