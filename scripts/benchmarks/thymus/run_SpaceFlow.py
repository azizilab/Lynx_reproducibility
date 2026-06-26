## ## Spatial trajectory inference via SpaceFlow

# %%
import os
import gc
import sys
import time

import numpy as np
import pandas as pd
import scanpy as sc
import squidpy as sq
import omicverse as ov

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
import IO

%load_ext autoreload
%autoreload 2

# %%
# Dataset specs
k = 8  # grid graph
data_path = DATA_DIR + '/thymus/'
outdir = FIGURES_DIR + '/'
sample_id = 'Mouse_Thymus1'

adata_rna = sc.read_h5ad(os.path.join(data_path, sample_id, 'adata_rna.h5'))

# %%
# SpaceFlow training: backbone architecture - DGI
sf_obj=ov.space.pySpaceFlow(adata_rna)
sf_obj.train(
    spatial_regularization_strength=0.1, 
    z_dim=50, lr=1e-3, epochs=1000, 
    max_patience=50, min_stop=100, 
    random_seed=42, gpu=0, 
    regularization_acceleration=True, 
    edge_subset_sz=1000000
)

# Compute & extract pSM values
sf_obj.cal_pSM(
    n_neighbors=8, resolution=1,
    max_cell_for_subsampling=5000,psm_key='pSM_spaceflow'
)

# %%
# Rotate pSM orientation if needed
# sf_obj.adata.obs['pSM_spaceflow'] = 1. - sf_obj.adata.obs['pSM_spaceflow'].values
sq.pl.spatial_scatter(
    sf_obj.adata, color='pSM_spaceflow', 
    size=100, cmap='RdBu_r', img=False
)

# %%
# Clustering on pSM
ov.utils.cluster(
    sf_obj.adata,use_rep='spaceflow',method='GMM', n_components=4
)

# %%
# Save pSM values
sf_obj.adata.obs[['pSM_spaceflow']].to_csv(RESULTS_DIR + '/thymus/SpaceFlow_thymus_rna_pseudotime.csv')
sf_obj.adata.obs[['gmm_cluster']].to_csv(RESULTS_DIR + '/thymus/SpaceFlow_thymus_rna_seg.csv')
