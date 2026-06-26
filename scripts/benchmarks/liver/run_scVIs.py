# Benchmark with scVI & TotalVI (liver)
#
# Adapted from scripts/benchmarks/thymus/run_scVIs.py for the liver application:
# scVI is trained on the Xenium gene panel; TotalVI uses Xenium (RNA) + DESI as its
# two modalities (DESI intensities are rescaled like the thymus protein modality).
# Produces the artifacts the liver Benchmark.ipynb loads:
#   results/liver/scVI_liver_xenium.npy
#   results/liver/TotalVI_liver_xenium.npy
# Runs in the main LYNX env (`env/`, where scvi-tools is installed); not re-run in this repo.

# %%
import os
import gc
import sys

import numpy as np
import pandas as pd
import scanpy as sc
import squidpy as sq

import torch

# %%
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

sns.set_context('paper')
rcParams.update({'font.family': 'Liberation Sans'})
rcParams.update({'font.size': 12})
rcParams.update({'figure.dpi': 180})
rcParams.update({'savefig.dpi': 300})

# %%
sys.path.append('../../')
sys.path.append('../../models/')
sys.path.append('../../util')

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
# Competitor imports assume the method's venv / original layout (benchmarks/README.md).
# -----------------------------------------------------------------------------

import IO, plot, utils, trajectory

# %%
# Load dataset (Xenium + DESI), matching the other liver benchmark scripts
xenium_path = DATA_DIR + '/xenium/'
desi_path = DATA_DIR + '/desi/'
sample_id = 'NIH_F5_proseg'

adata_xenium = IO.load_xenium(os.path.join(xenium_path, sample_id), load_img=True)
adata_desi = sc.read_h5ad(os.path.join(desi_path, sample_id + '.h5'))
adata_xenium, adata_desi = IO.filter_cells(adata_xenium, adata_desi, by='map')

# %%
# -------------
#  (1). scVI
# -------------
import scvi
scvi.settings.seed = 42

adata_rna = adata_xenium.copy()
scvi.model.SCVI.setup_anndata(adata_rna)
model = scvi.model.SCVI(adata_rna, n_layers=2, gene_likelihood="nb")
model.train()

# Retrieve & save latent representation
latent = model.get_latent_representation()
np.save(RESULTS_DIR + '/liver/scVI_liver_xenium.npy', latent)
adata_rna.obsm['X_scvi'] = latent

# %%
# ----------------
#  (2). TotalVI  (Xenium RNA + DESI as the second modality)
# ----------------
import mudata as md

adata_desi.X = (adata_desi.X - adata_desi.X.min()) / (adata_desi.X.max() - adata_desi.X.min())
adata_desi.X = (255 * adata_desi.X).astype(np.uint8)
mdata = md.MuData({'rna': adata_xenium, 'protein': adata_desi})

scvi.model.TOTALVI.setup_mudata(
    mdata,
    rna_layer=None,
    protein_layer=None,
    modalities={
        "rna_layer": "rna",
        "protein_layer": "protein",
    },
)

model = scvi.model.TOTALVI(mdata)  # n_latent defaults to 20
model.train()

# Retrieve & save joint latent representation
adata_xenium.obsm['X_totalvi'] = model.get_latent_representation()['rna']
np.save(RESULTS_DIR + '/liver/TotalVI_liver_xenium.npy', adata_xenium.obsm['X_totalvi'])
