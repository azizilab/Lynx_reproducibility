# Competitor-method benchmarks

Scripts that run the methods LYNX is compared against, per application
(`breast/`, `liver/`, `thymus/`) plus `ablation/`. **These are provided for
traceability and are not re-run as part of this repo** — their outputs are
already cached under `results/<app>/` and consumed by the `Benchmark.ipynb`
notebooks in `scripts/<app>/`.

## How they run

Each method needs its own environment (different, often conflicting, pins).
`run_benchmarks.sh` selects the venv from the script name and puts the repo root
on `PYTHONPATH`:

```bash
# from scripts/benchmarks/
bash run_benchmarks.sh <app> <script> [args...]
# e.g.
bash run_benchmarks.sh liver run_GASTON.py
bash run_benchmarks.sh thymus run_SIMVI.py
```

### Method → environment mapping

Almost every baseline has its **own** environment (the pins conflict across methods).
Most live under `venvs/<name>`; the exception is **scVI / TotalVI**, which run in the
main LYNX env (`env/`, where `scvi-tools` is installed).

| Script(s)                         | Environment            | Python | Auto-selected by `run_benchmarks.sh`? |
|-----------------------------------|------------------------|--------|----------------------------------------|
| `run_GASTON.py`                   | `venvs/gaston_env`     | 3.9.5  | yes (`*GASTON*`)        |
| `run_Novae.py`                    | `venvs/novae_env`      | 3.9.5  | yes (`*Novae*`)        |
| `run_SpaceFlow.py`                | `venvs/spaceflow_env`  | 3.9.x  | yes (`*SpaceFlow*`)    |
| `run_SpatialGlue.py`              | `venvs/spatialglue_env`| **3.8.3** | yes (`*SpatialGlue*`)  |
| `run_SIMVI.py`                    | `venvs/simvi_env`      | 3.9.x  | yes (`*SIMVI*`)        |
| `run_SpatialMETA.py`              | `venvs/spatialmeta_env`| 3.9.5  | **no** — activate manually |
| `run_scVIs.py`, `run_others.py`   | main `env/` (scvi-tools)| 3.9.5 | **no** — activate manually |
| `run_spaTrack.py`                 | a `spaTrack` install    | 3.9.x | **no** — activate manually |
| `ablation/*`                      | main `env/`          | 3.9.5 | **no** |

`run_benchmarks.sh` only auto-activates the five mapped patterns above; for the rest it
runs in whatever environment is currently active, so activate the right one first (or add
a `case` entry to the script). The environments themselves are **not** included here.

### Building the environments

The baseline environments are plain `venv`s on **Python 3.9.5** (the same interpreter as
the main LYNX env), with the single exception of **SpatialGlue on Python 3.8.3** (its
upstream pins require 3.8). The original build commands were not preserved in shell
history; recreate each one from the method's upstream install instructions, following this
template:

```bash
python3.9 -m venv venvs/<name>
source venvs/<name>/bin/activate
pip install <method-package>            # per the method's upstream README
# install LYNX too if the script imports IO/util:  pip install -e <Lynx>
deactivate
```

> ⚠️ **`spatialglue_env` must be built with Python 3.8**, not 3.9 (its upstream pins
> require 3.8; the original env is Python 3.8.3):
> ```bash
> python3.8 -m venv venvs/spatialglue_env
> source venvs/spatialglue_env/bin/activate
> pip install <SpatialGlue deps>
> ```

**Note** scVI / TotalVI (`run_scVIs.py`, `run_others.py`) run in the main LYNX `env/`,
where `scvi-tools` is installed alongside LYNX.

## Imports & paths (important)

These scripts were authored to run from the original `Lynx` checkout under
`benchmarks/<app>/`. Two consequences in this repo:

- **Save/load paths were normalized** to the central `paths.py` roots(`DATA_DIR`, `RESULTS_DIR`, `FIGURES_DIR`).

