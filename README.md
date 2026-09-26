# GeDarkMatter-LowEnergyMC

GeDarkMatter-LowEnergyMC is a research-oriented Monte Carlo and statistical-analysis framework for studying low-energy signals in germanium dark-matter detectors. The project is designed to separate the underlying particle-physics recoil model from detector response and statistical interpretation. This modular approach is useful because uncertainties in the predicted signal, the detector resolution, the trigger threshold, the selection efficiency, and the background model arise from physically different sources and should not be hidden inside one monolithic simulation.

Germanium detectors are especially important in low-background physics because they can combine low energy thresholds with excellent energy resolution and mature detector technology. For light dark matter, low-mass weakly interacting particles, or other exotic energy-deposition mechanisms, the most informative events can appear close to threshold. In that regime, detector effects that would be secondary at high energy can become central to the interpretation. A modest change in resolution or trigger efficiency can noticeably modify the predicted observed spectrum. The purpose of this repository is to provide a transparent framework in which those effects can be studied, validated, and eventually combined with more sophisticated dark-matter interaction models.

The current implementation includes a simple toy recoil generator, elastic two-body scattering kinematics, detector smearing, hard thresholding, logistic efficiency, matrix-based detector response, binned counting, Poisson likelihood calculations, Asimov significance, and rate-to-count conversion. These pieces form the basic analysis chain needed to transform an idealized recoil spectrum into a detector-level prediction.

For a dark-matter particle of mass (m_chi) scattering elastically from a nucleus of mass (m_N), the reduced mass is

[
mu_{chi N}=
rac{m_chi m_N}{m_chi+m_N}.
]

For an incident speed (v), the maximum recoil energy in an elastic collision is

[
E_{R,max}=
rac{2mu_{chi N}^2v^2}{m_N}.
]

Conversely, the minimum incident speed required to produce a recoil energy (E_R) is

[
v_{min}=
sqrt{
rac{m_NE_R}
{2mu_{chi N}^2}
}.
]

These relations are implemented explicitly so that the user can examine the kinematic scale of a proposed interaction before introducing a full astrophysical velocity distribution.

The current Monte Carlo includes a toy exponential recoil distribution,

[
rac{dR}{dE}propto e^{-E/E_0}.
]

This model is not intended to represent a complete dark-matter prediction. Its role is to provide a controlled input spectrum that makes it possible to validate the downstream detector and statistical machinery. A physically calibrated differential rate can later replace the toy spectrum without changing the detector-response layer.

Detector energy resolution is modeled initially by Gaussian smearing,

[
E_{mathrm{meas}}
sim
mathcal N(E_{mathrm{true}},sigma_E).
]

The package supports both event-level smearing and response-matrix calculations. In a binned analysis, the detector response can be represented as

[
N_i^{mathrm{meas}}
=
sum_j
R_{ij}N_j^{mathrm{true}},
]

where (R_{ij}) gives the probability that an event originating in true-energy bin (j) is reconstructed in measured-energy bin (i). The current response implementation is normalized so that total counts are conserved before efficiency losses are applied.

A logistic efficiency model is included as a generic smooth threshold,

[
epsilon(E)=
rac{1}{
1+exp[-(E-E_{50})/w]
}.
]

Here (E_{50}) is the energy at which efficiency reaches 50%, and (w) controls the turn-on width. This is useful for testing analysis logic, but a real experimental analysis should use a measured efficiency curve obtained from calibration or detector characterization. The repository also supports a hard threshold for cases where a simple cut is intentionally being studied. Hard thresholds and smooth efficiency curves represent different assumptions and should not be used interchangeably without explanation.

The statistical layer begins with a Poisson likelihood. For observed counts (n_i) and expected counts (mu_i), the log likelihood, up to additive constants independent of the model parameters, is

[
lnmathcal L
=
sum_i
left(
n_ilnmu_i-mu_i
ight).
]

The repository also implements the Asimov significance for a known background model,

[
Z_A=
sqrt{
2sum_i
left[
(s_i+b_i)
lnleft(1+rac{s_i}{b_i}ight)
-s_i
ight]
}.
]

This quantity is useful for estimating expected sensitivity under idealized conditions, but it is not a replacement for a complete experimental limit-setting procedure with nuisance parameters, systematic uncertainties, and coverage studies.

The package includes explicit conversion from differential rate to expected counts. If the rate is expressed in events per kilogram per day per electronvolt, the expected number of events in a bin of width (Delta E) for exposure (mathcal E) is

[
N=
rac{dR}{dE}
mathcal E
Delta E.
]

Making this conversion explicit is important because unit mistakes in exposure or energy binning can easily produce large normalization errors.

The repository is organized into several small modules. The `core.py` module contains the initial Monte Carlo recoil sampling, smearing, threshold, and efficiency utilities. The `kinematics.py` module implements elastic scattering kinematics. The `response.py` module builds and applies detector-response matrices. The `statistics.py` module contains Poisson and Asimov calculations. Example scripts demonstrate toy Monte Carlo generation and recoil kinematics, while the automated tests verify reproducibility, kinematic inversion, response normalization, and statistical behavior.

Installation can be performed with

```bash
git clone https://github.com/premathul/GeDarkMatter-LowEnergyMC.git
cd GeDarkMatter-LowEnergyMC
python -m pip install -e .
```

For development and testing,

```bash
python -m pip install -e .[dev]
pytest -q
```

A basic toy Monte Carlo can be run with

```python
from gedm_mc.core import (
    sample_exponential_recoils,
    smear_energy,
    apply_threshold,
)

E = sample_exponential_recoils(
    n=100000,
    scale_ev=80.0,
    rng=7,
)

E_meas = smear_energy(
    E,
    sigma_ev=10.0,
    rng=8,
)

accepted = apply_threshold(
    E_meas,
    threshold_ev=40.0,
)
```

Explicit random seeds are used here so that the result can be reproduced exactly.

The current code should be regarded as a low-energy analysis foundation rather than a complete dark-matter event generator. It does not yet include the Standard Halo Model, Earth-frame velocity distributions, nuclear form factors, isotope-dependent scattering, spin-independent cross-section normalization, spin-dependent interactions, dark-photon absorption, crystal electronic structure, Migdal processes, quenching, phonon transport, cosmogenic activation, or detailed radioactive backgrounds.

The next physics milestone is to implement a standard spin-independent nuclear recoil model for germanium. That requires combining the halo velocity distribution, nuclear reduced mass, cross-section normalization, isotope composition, and a nuclear form factor such as the Helm form factor. Once that calculation is validated against independent references, the toy exponential spectrum can remain as a testing utility while the physical recoil model becomes the primary signal generator.

A second development stage will focus on detector physics near threshold. For germanium detectors, this may include ionization yield, electron-equivalent versus nuclear-recoil-equivalent energy, Fano fluctuations, energy-dependent resolution, charge-production statistics, trigger efficiency, and multiple measured channels. The architecture is intentionally designed so that these response effects remain separate from the underlying particle model.

A third development stage will add backgrounds and statistical inference. Real rare-event analyses depend critically on the background model, and therefore future versions should support flat continua, lines, cosmogenic components, neutron templates, and nuisance parameters. Profile likelihoods, upper limits, expected sensitivity bands, toy-Monte-Carlo coverage tests, and systematic uncertainty propagation are natural future additions.

The long-term workflow is

[
	ext{interaction model}
ightarrow
rac{dR}{dE}
ightarrow
	ext{true spectrum}
ightarrow
R(E_{mathrm{meas}},E_{mathrm{true}})
ightarrow
epsilon(E)
ightarrow
	ext{background model}
ightarrow
mathcal L
ightarrow
	ext{sensitivity or inference}.
]

The key design principle is that each stage should remain replaceable and testable. A detector physicist should be able to modify the response model without rewriting the dark-matter kinematics, while a phenomenologist should be able to replace the signal model without modifying the detector analysis.

Reproducibility is especially important in low-count experiments. A quantitative result should record the dark-matter mass, interaction model, nuclear assumptions, velocity model, recoil normalization, detector resolution, threshold, efficiency, exposure, energy binning, random seed, statistical method, and Git commit. Small differences in any of these inputs can produce meaningful changes near threshold.

The repository is currently appropriate for method development, detector-response studies, educational Monte Carlo work, and prototyping of low-energy analyses. It should not be used to claim an experimental exclusion limit or discovery sensitivity without independently validating the physical recoil model, detector calibration, background model, and statistical procedure.

## Contact

**Athul Prem**

For questions, scientific discussion, collaboration, or suggestions related to this project, please contact Athul Prem through the GitHub account associated with the repository.
