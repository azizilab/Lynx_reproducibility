# %%
import os
import gc
import sys
import time

import numpy as np
import pandas as pd
import scanpy as sc
import squidpy as sq
import torch

from pytorch_lightning.utilities.seed import seed_everything

# %%
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from IPython.display import display

sns.set_context('paper')
rcParams.update({'font.family': 'Liberation Sans'})
rcParams.update({'font.size': 12})
rcParams.update({'figure.dpi': 180})
rcParams.update({'savefig.dpi': 300})

import warnings
warnings.filterwarnings('ignore')
%matplotlib inline

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
# NOTE: competitor imports below assume the original liver3d checkout layout /
# the method's venv (see benchmarks/README.md); not re-run in this repo.
# -----------------------------------------------------------------------------
import IO, plot, trajectory
from simvi.model import SimVI

# %%
%load_ext autoreload
%autoreload 2

# %%
# Load dataset
data_path = DATA_DIR + '/thymus/'
sample_ids = sorted([
    f for f in os.listdir(data_path)
    if os.path.isdir(os.path.join(data_path, f))
])

sample_id = sample_ids[0]
adata_rna = sc.read_h5ad(os.path.join(data_path, sample_id, 'adata_rna.h5'))

# %%
# Dataset specs
k = 8
adata = adata_rna.copy()
SimVI.setup_anndata(adata)
edge_index = SimVI.extract_edge_index(adata, n_neighbors=k)

# %%
# Training & Inference
seed_everything(42)

model = SimVI(
    adata, kl_weight=1, kl_gatweight=0.01, lam_mi=1000, 
    permutation_rate=0.5, n_spatial=20, n_intrinsic=20
)
train_loss, val_loss = model.train(edge_index, max_epochs=200, batch_size=500, use_gpu=True, mae_epochs=25)

# %%
adata.obsm['simvi_z'] = model.get_latent_representation(edge_index, representation_kind='intrinsic', give_mean=True)
adata.obsm['simvi_s'] = model.get_latent_representation(edge_index, representation_kind='interaction', give_mean=True)

# %%
# %%
# Save model & latent variables
model.save(RESULTS_DIR + "/thymus/simvi_model.pt")
np.save(RESULTS_DIR + '/thymus/SIMVI_rna_z20.npy', adata.obsm['simvi_z'])
np.save(RESULTS_DIR + '/thymus/SIMVI_rna_s20.npy', adata.obsm['simvi_s'])
