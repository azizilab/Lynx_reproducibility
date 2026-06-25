# `results/` — cached model outputs (placeholder)

Placeholder directory. The `Benchmark.ipynb` notebooks read **cached** artifacts from
here so figures can be regenerated without re-running any model. The files are
gitignored (large `.h5ad`/`.npy`); obtain them from the project's results release or
regenerate with the scripts below. Override the location with:

```bash
export LYNX_RESULTS_DIR=/path/to/results
```

All paths resolve from `RESULTS_DIR` (see `../paths.py`).

## Artifact → producer map

LYNX outputs (`scripts/<app>/run_Lynx*.py`):

| Artifact | Producer |
|---|---|
| `results/breast/LYNX_xenium_cci2.h5ad` | `scripts/breast/run_Lynx.py` |
| `results/liver/LYNX_xenium_6_0512.h5ad`, `LYNX_desi_6_0512.npy`, `LYNX_t*.npy` | `scripts/liver/run_Lynx.py` |
| `results/liver_3d/LYNX_NIH_F5_section_*_{xenium,desi}.h5ad`, `pseudotime_3d*.npy`, `zone_3d*.npy` | `scripts/liver/run_Lynx_3D.ipynb` |
| `results/thymus/lynx_rna_6_Mouse_Thymus1.h5ad`, `lynx_*_Mouse_Thymus1.npy` | `scripts/thymus/run_Lynx.py` |
| `results/liver/ab_validation.h5ad` | `scripts/liver/simulate_gradient.py` |

Competitor outputs (`scripts/benchmarks/<app>/`):

| Artifact pattern | Producer |
|---|---|
| `results/<app>/GASTON_*` | `run_GASTON.py` |
| `results/<app>/Novae_*` | `run_Novae.py` |
| `results/<app>/SIMVI_*`, `simvi_model.pt` | `run_SIMVI.py` |
| `results/<app>/SpaceFlow_*` | `run_SpaceFlow.py` |
| `results/<app>/SpatialGlue_*` | `run_SpatialGlue.py` |
| `results/<app>/SpatialMETA_embedding.npy` | `run_SpatialMETA.py` |
| `results/thymus/scvi_*.npy`, `totalvi_*.npy` | `run_scVIs.py` / `run_others.py` |
| `results/<app>/ablation/*` | `benchmarks/ablation/<app>_ablation.py` |
| `results/<app>/runtime.txt` | appended by several benchmark scripts |

> Note: original `CORAL_*` / `Coral_*` artifacts are **not** regenerated here — Coral
> was excluded from this repo.
