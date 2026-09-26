# GeDarkMatter-LowEnergyMC

Lightweight Monte Carlo tools for studying low-energy recoil signals in germanium detectors.

## Scope
The first release provides:
- sampling from user-defined recoil spectra,
- Gaussian detector-energy smearing,
- threshold and efficiency handling,
- binned expected/observed spectra,
- reproducible random-number control.

This is **not** a replacement for Geant4 or a complete dark-matter rate calculator. It is intended as a transparent low-energy analysis layer that can later ingest physically calibrated recoil spectra.

## Quick start
```bash
python -m pip install -e .
python examples/toy_recoil_mc.py
pytest
```

## Scientific principle
Signal generation and detector response are kept separate so that a validated scattering-rate model can be swapped in without changing the detector pipeline.

## Status
Early research software using toy spectra only.

## License
MIT.
