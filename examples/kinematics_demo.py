from gedm_mc.kinematics import max_recoil_energy_ev

m_ge=67.7
for mchi in (0.5,1,5,10,100):
    e=max_recoil_energy_ev(mchi,m_ge,220e3)
    print(f"m_chi={mchi:6.1f} GeV -> E_R,max={e:9.3f} eV at 220 km/s")
