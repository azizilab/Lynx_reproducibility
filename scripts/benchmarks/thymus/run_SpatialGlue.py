# %%
import os
import gc
import sys
import time

import numpy as np
import pandas as pd
import scanpy as sc
import torch

import SpatialGlue
from SpatialGlue.preprocess import clr_normalize_each_cell, pca, fix_seed
from SpatialGlue.preprocess import construct_neighbor_graph
from SpatialGlue.SpatialGlue_pyG import Train_SpatialGlue

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
# NOTE: competitor imports below assume the original liver3d checkout layout /
# the method's venv (see benchmarks/README.md); not re-run in this repo.
# -----------------------------------------------------------------------------
import IO
%load_ext autoreload
%autoreload 2

# %%
# Load dataset
data_path = DATA_DIR + '/thymus/'
sample_id = 'Mouse_Thymus1'

adata_rna = sc.read_h5ad(os.path.join(data_path, sample_id, 'adata_rna.h5'))
sc.pp.normalize_total(adata_rna, target_sum=1e4)
sc.pp.log1p(adata_rna)
adata_protein = sc.read_h5ad(os.path.join(data_path, sample_id, 'adata_protein.h5'))
adata_protein.var_names_make_unique()

# %%
# Train SpatialGlue model
data_type = 'Stereo-CITE-seq'
device = torch.device('cpu')
fix_seed(42)

n_pc_comps = min(adata_rna.shape[1], adata_protein.shape[1])
adata_rna.obsm['feat'] = pca(adata_rna, n_comps=n_pc_comps)
adata_protein.obsm['feat'] = pca(adata_protein, n_comps=n_pc_comps)

data = construct_neighbor_graph(adata_rna, adata_protein, datatype=data_type)
model = Train_SpatialGlue(data, datatype=data_type, device=device)
output = model.train()

# %%
adata_rna.obsm['SpatialGlue'] = np.load(RESULTS_DIR + '/thymus/SpatialGlue_embedding.npy')

# %% 
# Post-hoc clustering on latent embedding
from SpatialGlue.utils import clustering
tool = 'mclust'
clustering(
    adata_rna, key='SpatialGlue', add_key='SpatialGlue', 
    n_clusters=4, method=tool, use_pca=True
)

# %%
adata_rna.obs['SpatialGlue'].value_counts()

# %%
sc.pl.spatial(
    img_key=None,
    adata=adata_rna,
    color='SpatialGlue',
    size=100
)

# %%
# np.save(RESULTS_DIR + '/thymus/SpatialGlue_embedding.npy', output['SpatialGlue'])
np.save(RESULTS_DIR + '/thymus/SpatialGlue_cluster.npy', adata_rna.obs['SpatialGlue'].values)


