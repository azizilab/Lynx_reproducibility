# LYNX — Reproducibility

Analysis code and notebooks reproducing the figures in the **LYNX**
manuscript.

This repo deliberately holds **only** the scripts, notebooks, and instructions. The LYNX
 model is installed from the pinned source [`azizilab/Lynx`](https://github.com/azizilab/Lynx) repo.

## Structure

```
.
├── paths.py            # central DATA_DIR / RESULTS_DIR / FIGURES_DIR (env-overridable)
├── data/               # placeholder — see data/README.md
├── results/            # placeholder — see results/README.md
├── figures/            # outputs land here (figures/compiled/ for paper figures)
└── scripts/
    ├── breast/  liver/  thymus/    # per-app: annotation.py, run_Lynx*.py,
    │                                #          downstream.py, Benchmark.ipynb (+ liver 3D nbs)
    └── benchmarks/                  # competitor methods — see scripts/benchmarks/README.md
```

Each application's `Benchmark.ipynb` (plus liver application's `run_Lynx_3D.ipynb`) includde brief instructions with a
**"How to reproduce"** section listing the upstream scripts needed.

## Setup

LYNX and most benchmarking packages were implemented / tested **Python 3.9.5** (w/ exception from `spatialglue_env` with **Python 3.8**). 
— see [scripts/benchmarks/README.md](scripts/benchmarks/README.md). Conda is the preferred
track for the main env:

```bash
conda env create -f environment.yml && conda activate lynx

# Install the pinned LYNX implementation (EDITABLE — see note below)
git clone https://github.com/azizilab/Lynx.git
cd Lynx && git checkout 7090ff6 && pip install -e . && cd ..
pip install scFates==1.0.8 --no-deps                       # stale pins; out-of-resolver
pip install torch-sparse==0.6.18 torch-scatter==2.1.2 torch-geometric==2.6.1 \
    -f https://data.pyg.org/whl/torch-2.3.1+cu121.html      # match torch + CUDA

# Pull rendered notebook outputs
git lfs install && git lfs pull
```

`pip` fallback: see `requirements.txt`.

> **Dev shortcut:** if a `Lynx` checkout sits beside this repo (e.g. `../IMS`),
> `pip install -e ../IMS` installs LYNX from it instead of cloning.

## Reproduce

1. Populate `data/` (see [data/README.md](data/README.md)) — or `export LYNX_DATA_DIR=…`.
2. Obtain cached `results/` (see [results/README.md](results/README.md)) — or regenerate
   with the per-app scripts.
3. Open `scripts/<app>/Benchmark.ipynb` and run top-to-bottom. With cached `results/`,
   no model re-training is needed.

Full pipeline per application (run from `scripts/<app>/`):

```bash
python annotation.py     # prepare / annotate inputs   -> data/
python run_Lynx.py       # train LYNX                   -> results/<app>/
python downstream.py     # trajectory / zonation / CCI  -> figures/
# then open Benchmark.ipynb for baseline comparison + figure compilation
```

Each baseline method being benchmarked run in their own per-method venvs — see [scripts/benchmarks/README.md](scripts/benchmarks/README.md).

## Paths

Scripts / notebooks don't save results with hard-coded relative paths; they import roots from `paths.py`:

| Variable | Default | Override |
|---|---|---|
| `DATA_DIR` | `./data` | `LYNX_DATA_DIR` |
| `RESULTS_DIR` | `./results` | `LYNX_RESULTS_DIR` |
| `FIGURES_DIR` | `./figures` | `LYNX_FIGURES_DIR` |
| `FINAL_FIGURES_DIR` | `./figures/compiled` | `LYNX_FINAL_FIGURES_DIR` |

## Extra Notes

- Notebooks are stored via **Git LFS** with outputs intact (`git lfs pull` to fetch).
  LFS-tracked notebooks do **not** render in the GitHub web preview — view them locally.
- Save/load paths were normalized to the table above, fixing inconsistencies in the
  original benchmark scripts (e.g. liver GASTON wrote to both `../results/...` and
  `../../results/...`).
