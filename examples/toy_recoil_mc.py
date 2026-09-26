import numpy as np
from gedm_mc.core import sample_exponential_recoils, smear_energy, apply_threshold

e=sample_exponential_recoils(100000,80.0,rng=7)
e=smear_energy(e,10.0,rng=8)
kept=apply_threshold(e,40.0)
print(f"generated={len(e)} accepted={len(kept)} acceptance={len(kept)/len(e):.3f}")
print("median accepted energy [eV] =",np.median(kept))
