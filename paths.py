"""Central path configuration for the LYNX reproducibility repo.

All scripts and notebooks anchor their inputs/outputs to the four roots below
instead of hard-coding relative paths. Each root defaults to a sibling of this
file (the repo root) and can be overridden with an environment variable, e.g.::

    export LYNX_DATA_DIR=/mnt/big_disk/lynx_data

``data/`` and ``results/`` are gitignored placeholders — see their READMEs for
how to populate them. ``figures/`` holds downstream PDFs/SVGs;
``FINAL_FIGURES_DIR`` is where the notebooks write the compiled paper figures
(in the original repo this pointed *outside* the tree, at ``../LYNX_method/figures``).
"""

import os

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.environ.get("LYNX_DATA_DIR", os.path.join(REPO_ROOT, "data"))
RESULTS_DIR = os.environ.get("LYNX_RESULTS_DIR", os.path.join(REPO_ROOT, "results"))
FIGURES_DIR = os.environ.get("LYNX_FIGURES_DIR", os.path.join(REPO_ROOT, "figures"))

# Compiled paper figures (notebook "Compile figure" sections). Defaults to a
# subdir of FIGURES_DIR; override to restore the original external location.
FINAL_FIGURES_DIR = os.environ.get(
    "LYNX_FINAL_FIGURES_DIR", os.path.join(FIGURES_DIR, "compiled")
)

__all__ = ["REPO_ROOT", "DATA_DIR", "RESULTS_DIR", "FIGURES_DIR", "FINAL_FIGURES_DIR"]
