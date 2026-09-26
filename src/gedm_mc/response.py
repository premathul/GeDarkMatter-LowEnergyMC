import numpy as np

def gaussian_response_matrix(true_centers_ev, measured_centers_ev, sigma_ev):
    """Column-normalized detector smearing matrix P(E_meas | E_true)."""
    if sigma_ev<=0: raise ValueError("sigma_ev must be positive")
    t=np.asarray(true_centers_ev,float)
    m=np.asarray(measured_centers_ev,float)
    z=(m[:,None]-t[None,:])/sigma_ev
    r=np.exp(-0.5*z*z)
    norm=r.sum(axis=0,keepdims=True)
    norm[norm==0]=1
    return r/norm

def apply_response(expected_true_counts, response_matrix):
    x=np.asarray(expected_true_counts,float)
    r=np.asarray(response_matrix,float)
    if r.shape[1]!=x.size: raise ValueError("response dimension mismatch")
    return r@x

def apply_efficiency(expected_counts, efficiency):
    x=np.asarray(expected_counts,float)
    e=np.asarray(efficiency,float)
    if x.shape!=e.shape: raise ValueError("shape mismatch")
    if np.any((e<0)|(e>1)): raise ValueError("efficiency must be in [0,1]")
    return x*e
