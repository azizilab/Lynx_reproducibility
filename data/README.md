# `data/` — input datasets (placeholder)

This directory is a **placeholder**. 

```bash
export LYNX_DATA_DIR=/path/to/your/data   # overrides the default ./data
```

All scripts/notebooks resolve inputs from `DATA_DIR` (see `../paths.py`).

## Expected layout

```
data/
├── breast/
│   ├── <sample_id>/
│   │   ├── experiment.xenium          # Xenium run metadata
│   │   ├── Xenium_annot.csv           # cell-type annotations ('Cluster')
│   │   └── morphology / H&E image
│   └── dcis_fov/                      # produced by breast/annotation.py
│       ├── cell_feature_matrix.h5     # Xenium expression (DCIS FOV)
│       ├── he.tif / he_hires.tif      # cropped H&E
│       └── he_patches_norm.h5ad       # normalized H&E patches
│
├── xenium/                            # liver Xenium (per-sample subdirs:
│   └── <sample_id>/                   #   morphology_focus/, morphology_mip.ome.tif, reseg_masks.npy)
├── desi/                              # liver DESI (metabolomics)
├── integrated/
│   ├── antibody/                      # liver antibody-stain ground truth
│   └── anchors/                       # cross-modal integration anchors
│
└── thymus/
    └── <sample_id>/                   # e.g. Mouse_Thymus1
        └── adata_rna.h5  / adata_protein.h5  # processed (written by annotation.py)
```

## Sources

These datasets accompany the LYNX manuscript. Obtain them from the project's data
release / repository (contact the Azizi Lab / see the manuscript data-availability
statement) and place them under the layout above. The per-application
`annotation.py` scripts handle preprocessing steps for the input data.
