# GeDarkMatter-LowEnergyMC

GeDarkMatter-LowEnergyMC is a lightweight Monte Carlo and statistical-analysis framework for studying **low-energy recoil signals in germanium dark-matter detectors**.

The project is designed around a modular pipeline:

[
	ext{particle model}
ightarrow
rac{dR}{dE}
ightarrow
	ext{true recoil spectrum}
ightarrow
	ext{detector response}
ightarrow
	ext{selection efficiency}
ightarrow
	ext{observed spectrum}
ightarrow
	ext{statistical inference}.
]

The present repository does not attempt to replace Geant4 or a complete dark-matter phenomenology package. Instead, it focuses on a transparent low-energy layer that can accept validated physical recoil spectra and propagate them through detector response and analysis.

---

## 1. Scientific motivation

Germanium detectors are widely used in rare-event physics because of their:

- excellent energy resolution,
- low electronic noise,
- mature crystal technology,
- low thresholds,
- sensitivity to nuclear and electronic recoils,
- long history in low-background experiments.

For light or weakly interacting dark matter, the most interesting events may appear near detector threshold.

At those energies, seemingly small assumptions about resolution, threshold, efficiency, and binning can significantly affect the predicted observed spectrum.

This repository isolates those effects so that they can be tested independently.

---

## 2. Current capabilities

The package currently provides:

- toy exponential recoil-spectrum sampling,
- elastic two-body recoil kinematics,
- reduced-mass calculation,
- maximum nuclear recoil energy,
- minimum incident speed,
- Gaussian detector smearing,
- threshold selection,
- logistic efficiency curves,
- detector response matrices,
- response application to expected spectra,
- binned histograms,
- Poisson log-likelihood,
- Asimov discovery significance,
- exposure and rate conversion.

---

## 3. Elastic recoil kinematics

For dark-matter mass (m_chi) and target-nucleus mass (m_N), the reduced mass is

[
mu_{chi N}
=
rac{m_chi m_N}{m_chi+m_N}.
]

For incident speed (v), the maximum elastic nuclear recoil energy is

[
E_{R,max}
=
rac{2mu_{chi N}^2v^2}{m_N}.
]

The minimum incident speed required to produce recoil (E_R) is

[
v_{min}
=
sqrt{
rac{m_NE_R}
{2mu_{chi N}^2}
}.
]

The code implements these relations with explicit SI/GeV/eV conversion.

---

## 4. Toy recoil generation

The initial Monte Carlo includes a simple exponential spectrum

[
rac{dR}{dE}
propto
e^{-E/E_0}.
]

This is **not** presented as a complete dark-matter recoil model.

It exists to test the detector and statistical pipeline with a controlled input distribution.

A validated physical rate model can later replace it without changing the downstream response code.

---

## 5. Detector energy resolution

Measured energy is modeled with Gaussian smearing,

[
E_{m meas}
sim
mathcal N(E_{m true},sigma_E).
]

The repository supports both event-by-event Monte Carlo smearing and matrix-based spectral response.

For discrete energy grids,

[
N_i^{m meas}
=
sum_j
R_{ij}
N_j^{m true},
]

where (R_{ij}) is the detector response matrix.

---

## 6. Detection efficiency

A logistic efficiency model is included:

[
epsilon(E)
=
rac{1}
{1+exp[-(E-E_{50})/w]}.
]

Here:

- (E_{50}) is the 50% efficiency point,
- (w) controls the turn-on width.

This is a convenient generic approximation.

Real analyses should use measured detector efficiencies.

---

## 7. Thresholding

A hard threshold can also be applied directly,

[
E_{m meas}ge E_{m th}.
]

Hard thresholds and smooth efficiency curves represent different detector assumptions and should not be confused.

---

## 8. Repository structure

```text
GeDarkMatter-LowEnergyMC/
├── README.md
├── pyproject.toml
├── examples/
│   ├── toy_recoil_mc.py
│   └── kinematics_demo.py
├── src/
│   └── gedm_mc/
│       ├── __init__.py
│       ├── core.py
│       ├── kinematics.py
│       ├── response.py
│       └── statistics.py
├── tests/
│   ├── test_core.py
│   └── test_physics.py
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 9. Installation

```bash
git clone https://github.com/premathul/GeDarkMatter-LowEnergyMC.git
cd GeDarkMatter-LowEnergyMC
python -m pip install -e .
```

Development installation:

```bash
python -m pip install -e .[dev]
pytest -q
```

---

## 10. Example: toy Monte Carlo

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

Using explicit random seeds makes this example reproducible.

---

## 11. Example: recoil kinematics

```python
from gedm_mc.kinematics import max_recoil_energy_ev

Emax = max_recoil_energy_ev(
    m_chi_gev=10.0,
    m_nucleus_gev=67.7,
    speed_m_s=220e3,
)

print(Emax)
```

This illustrates the kinematic scale for an elastic dark-matter–germanium collision.

---

## 12. Statistical layer

### Poisson likelihood

For observed bin count (n_i) and expectation (mu_i),

[
lnmathcal L
=
sum_i
left(
n_ilnmu_i-mu_i
ight)
+
	ext{constant}.
]

The factorial term is omitted when only likelihood differences are needed.

### Asimov significance

For known background (b_i) and signal (s_i),

[
Z_A
=
sqrt{
2sum_i
left[
(s_i+b_i)
lnleft(1+rac{s_i}{b_i}ight)
-s_i
ight]
}.
]

This is an approximate expected-significance metric, not a substitute for a complete experimental limit-setting framework.

---

## 13. Rate to counts

For differential rate

[
rac{dR}{dE}
]

in events/(kg day eV), exposure (mathcal E) in kg day, and bin width (Delta E),

[
N
=
rac{dR}{dE}
mathcal E
Delta E.
]

The code provides a helper for this conversion.

---

## 14. Validation

Current tests verify:

- reproducible Monte Carlo draws for fixed seeds,
- threshold selection,
- logistic efficiency midpoint,
- recoil kinematics inversion,
- detector-response normalization,
- conservation of total counts under normalized smearing,
- positivity of Asimov significance.

---

## 15. Scientific limitations

The current repository does not yet include:

- Standard Halo Model velocity integration,
- nuclear form factors,
- spin-independent cross-section normalization,
- spin-dependent interactions,
- dark-photon absorption,
- electron recoil production,
- crystal form factors,
- Migdal effect,
- quenching models,
- ionization yield,
- phonon transport,
- Geant4 detector geometry,
- cosmogenic activation,
- radioactive background simulation,
- nuisance-parameter profiling,
- confidence-limit construction.

These are future modules.

---

## 16. Planned development

### Phase I — recoil physics

- Standard Halo Model,
- Maxwellian velocity distribution,
- Earth-frame velocity,
- spin-independent nuclear recoil rate,
- Helm form factor,
- isotope mixture for natural Ge.

### Phase II — low-energy detector physics

- nuclear recoil ionization yield,
- electron-equivalent energy,
- threshold models,
- Fano fluctuations,
- energy-dependent resolution,
- multiple response channels.

### Phase III — background models

- flat continuum,
- exponential backgrounds,
- x-ray lines,
- cosmogenic isotopes,
- neutron recoil templates,
- nuisance parameters.

### Phase IV — inference

- profile likelihood,
- Asimov sensitivity,
- upper limits,
- toy-MC coverage,
- Bayesian posterior option,
- systematic uncertainty propagation.

### Phase V — experiment interface

- external recoil-spectrum import,
- calibration tables,
- detector efficiency files,
- measured background spectra,
- configuration-driven analysis.

---

## 17. Separation of signal and detector response

A major design principle is to keep

[
	ext{physics generation}
]

separate from

[
	ext{detector response}.
]

This allows the same detector model to be tested against different candidate signals.

Likewise, a single theoretical signal can be propagated through different detector assumptions.

---

## 18. Reproducibility checklist

A quantitative result should state:

- dark-matter mass,
- interaction model,
- target isotope assumptions,
- recoil-spectrum normalization,
- velocity model,
- energy resolution,
- threshold,
- efficiency,
- exposure,
- binning,
- random seed,
- statistical method,
- code commit.

---

## 19. Appropriate use

This software is suitable for:

- toy studies,
- method development,
- educational calculations,
- detector-response validation,
- sensitivity prototyping,
- cross-checking analysis logic.

It should not be used for publication-level exclusion limits without independently validating the physical rate model, detector calibration, and statistical treatment.

---

## 20. Contributing

Contributions are welcome in:

- recoil models,
- Ge detector physics,
- efficiency models,
- response matrices,
- backgrounds,
- statistical methods,
- numerical tests,
- documentation.

Physics contributions should include references and analytical or numerical benchmarks whenever possible.

---

## 21. License

MIT License.

---

## 22. Project status

**Status:** active development.

The present repository provides a transparent low-energy Monte Carlo and response-analysis foundation. The long-term objective is a modular Ge detector framework connecting dark-matter recoil physics to experimentally observable spectra and statistically reproducible sensitivity calculations.
