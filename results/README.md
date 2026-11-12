# `results/` — cached model outputs (placeholder)

Placeholder directory. The `Benchmark.ipynb` notebooks read **cached** artifacts from
here so figures can be regenerated without re-running LYNX / baselines. The files are
gitignored; obtain them from the project's results release or
regenerate with the scripts below. Override the location with:

```bash
export LYNX_RESULTS_DIR=/path/to/results
```

All paths resolve from `RESULTS_DIR` (see `../paths.py`).

## Naming convention

Method-output files follow `<METHOD>_<tissue>_<sampletype>[_<descriptor>].<ext>`, where
`<tissue>` is `breast` / `liver` / `thymus` and `<sampletype>` is the modality
(`xenium` for breast & liver, `rna` for thymus; `desi` / `protein` where applicable).
Version / parameter tokens (`_6`, `_0512`, `_50`, `_10`, `_20`, …) were removed. The
primary LYNX result per application is the bare `LYNX_<tissue>_<sampletype>` file.

## LYNX outputs

| Artifact | Producer |
|---|---|
| `results/breast/LYNX_breast_xenium.h5ad` (+ `_cci`, `_stromal_states`) | `scripts/breast/run_Lynx.py` |
| `results/liver/LYNX_liver_xenium.h5ad`, `LYNX_liver_desi.npy`, `LYNX_liver_pseudotime.npy` | `scripts/liver/run_Lynx.py` |
| `results/liver_3d/LYNX_liver_{SAMPLE_ID}_{section}_{xenium,desi}.h5ad` (joint run; `_seedN`: replicate runs, `_sectionwise`, `_heldout`: section-wise and held-out runs), `LYNX_liver_{SAMPLE_ID}_{neighbour_counts,joint_vs_sectionwise}.csv` | `scripts/liver/run_Lynx_3D.ipynb` |
| `results/liver_3d/LYNX_liver_{SAMPLE_ID}_{registration_error,slice_registration}.csv` | `scripts/liver/alignment_3D.ipynb` |
| `results/thymus/LYNX_thymus_rna.h5ad`, `LYNX_thymus_rna.npy` | `scripts/thymus/run_Lynx.py` |
| `results/liver/ab_validation.h5ad` (antibody ground truth) | `scripts/liver/simulate_gradient.py` |

## Baseline outputs (`scripts/benchmarks/<app>/`)

`<st>` = `xenium` (breast/liver) or `rna` (thymus).

| Artifact pattern | Producer |
|---|---|
| `results/<app>/GASTON_<app>_<st>_{isodepth,seg}.npy` | `run_GASTON.py` |
| `results/<app>/Novae_<app>_<st>_{latent,seg,zero_shot_latent}.npy` | `run_Novae.py` |
| `results/<app>/SIMVI_<app>_<st>_{z,s}.npy`, `SIMVI_<app>_model.pt` | `run_SIMVI.py` |
| `results/<app>/SpaceFlow_<app>_<st>_{pseudotime,seg}.csv` | `run_SpaceFlow.py` |
| `results/<app>/SpatialGlue_<app>_<st>_{embedding,cluster}.npy` | `run_SpatialGlue.py` |
| `results/<app>/SpatialMETA_<app>_<st>_embedding.npy` | `run_SpatialMETA.py` |
| `results/<app>/scVI_<app>_<st>.npy`, `TotalVI_<app>_<st>.npy` | `run_scVIs.py` (liver & thymus) |
| `results/<app>/{RandomU,SpatialVGAE}_<app>_<st>_z.npy` | `ablation/<app>_ablation.py` |
| `results/<app>/runtime.txt` | appended by several benchmark scripts |

> A few baseline scripts (`run_SpatialGlue.py`, `run_scVIs.py`) keep their training
> `np.save(...)` commented out and reload the cached `.npy` — uncomment those lines to
> regenerate the artifact from scratch.
