import numpy as np

def poisson_log_likelihood(observed, expected):
    n=np.asarray(observed,float)
    mu=np.asarray(expected,float)
    if n.shape!=mu.shape or np.any(n<0) or np.any(mu<=0):
        raise ValueError("invalid Poisson inputs")
    return float(np.sum(n*np.log(mu)-mu))

def asimov_significance(signal, background):
    """Approximate discovery significance for known background."""
    s=np.asarray(signal,float)
    b=np.asarray(background,float)
    if s.shape!=b.shape or np.any(s<0) or np.any(b<=0):
        raise ValueError("invalid signal/background")
    q=2*np.sum((s+b)*np.log1p(s/b)-s)
    return float(np.sqrt(max(q,0.0)))

def expected_counts_from_rate(rate_per_kg_day_ev, exposure_kg_day, bin_width_ev):
    r=np.asarray(rate_per_kg_day_ev,float)
    if exposure_kg_day<0 or bin_width_ev<=0: raise ValueError("invalid exposure/bin width")
    return r*exposure_kg_day*bin_width_ev
