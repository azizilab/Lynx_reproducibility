## Spatial trajectory inference via spaTrack

# %%
import os
import gc
import sys
import time

import numpy as np
import pandas as pd
import scanpy as sc
import squidpy as sq
import spaTrack as spt

# %%
import matplotlib.pyplot as plt
import seaborn as sns

# %%
sys.path.append('../../')
sys.path.append('../../util/')

# --- LYNX reproducibility: central paths (see repo-root paths.py) ------------
import os as _os, sys as _sys
try:
    _d = _os.path.dirname(_os.path.abspath(__file__))
except NameError:  # interactive / jupytext: __file__ undefined
    _d = _os.getcwd()
while _d != _os.path.dirname(_d) and not _os.path.exists(_os.path.join(_d, "paths.py")):
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
from paths import DATA_DIR, RESULTS_DIR, FIGURES_DIR, FINAL_FIGURES_DIR
# NOTE: competitor imports below assume the original Lynx checkout layout /
# the method's venv (see benchmarks/README.md); not re-run in this repo.
# -----------------------------------------------------------------------------
import IO, plot, trajectory

# %%
%load_ext autoreload
%autoreload 2

# %%
# Dataset specs
xenium_path = DATA_DIR + '/xenium/'
desi_path = DATA_DIR + '/desi/'
sample_id = 'NIH_F5_proseg'

adata_xenium = IO.load_xenium(os.path.join(xenium_path, sample_id), load_img=True)
adata_desi = sc.read_h5ad(os.path.join(desi_path, sample_id+'.h5'))

# Filtered Xenium data with aligned DESI for benchmarking fairness
adata, _ = IO.filter_cells(adata_xenium, adata_desi, by='map') 
adata.obs['cluster'] = adata.obs['cell_type'].copy()

print("# cells:", adata.shape)

del adata_xenium, adata_desi
gc.collect()

# %%
# Preprocessing
sc.pp.filter_genes(adata, min_cells=10)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

# %%
# spaTrack analysis
# (1). Select the starting cell-label with Cholangiocytes
start_cells=spt.set_start_cells(adata,select_way='cell_type',cell_type='Cholangiocytes + Progenitor')


# %%
# (2). Comute cell transition prob.
gc.collect()
adata.obsm['X_spatial'] = adata.obsm['spatial'].copy()
adata.obsp["trans"] = spt.get_ot_matrix(adata, data_type="spatial", alpha1=0.5, alpha2=0.5)

# %% [markdown]
# (Note): full OT isn't even feasible for ~60,000 cells
