import numpy as np

def sample_exponential_recoils(n, scale_ev, rng=None):
    """Toy recoil spectrum dR/dE proportional to exp(-E/scale)."""
    if n < 0 or scale_ev <= 0:
        raise ValueError("n must be nonnegative and scale_ev positive")
    generator=np.random.default_rng(rng)
    return generator.exponential(scale_ev,int(n))

def smear_energy(energy_ev, sigma_ev, rng=None):
    """Apply Gaussian detector resolution in eV."""
    if sigma_ev < 0:
        raise ValueError("sigma_ev must be nonnegative")
    e=np.asarray(energy_ev,float)
    if sigma_ev == 0:
        return e.copy()
    generator=np.random.default_rng(rng)
    return generator.normal(e,sigma_ev)

def apply_threshold(energy_ev, threshold_ev):
    e=np.asarray(energy_ev,float)
    return e[e>=threshold_ev]

def efficiency_logistic(energy_ev, e50_ev, width_ev):
    if width_ev <= 0:
        raise ValueError("width_ev must be positive")
    e=np.asarray(energy_ev,float)
    return 1/(1+np.exp(-(e-e50_ev)/width_ev))

def histogram(energy_ev, bins_ev):
    return np.histogram(np.asarray(energy_ev,float),bins=np.asarray(bins_ev,float))
