# Building from Source

## Python/PIP

To build a wheel you need to install wheel into your Python build environment

    pip install wheel setuptools

fsl\_sub\_plugin\_slurm is only compatible with python 3 so you will be building a Pure Python Wheel

    python -m build

## Conda Build

The fsl\_sub\_plugin\_slurm conda recipe is hosted in a separate repository at https://git.fmrib.ox.ac.uk/fsl/conda/fsl-sub-plugin-slurm. Conda packages for new releases (denoted as tags on the gitlab repository) are automatically built and published to the FSL conda channel at https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public/.

To build a Conda package by hand for the current fsl\_sub\_plugin\_slurm release (denoted by the `version` field specified in the recipe `meta.yaml` file):

    git clone https://git.fmrib.ox.ac.uk/fsl/conda/fsl-sub-plugin-slurm
    cd fsl-sub-plugin-slurm
    conda build

Refer to the [FSL conda documentation](https://git.fmrib.ox.ac.uk/fsl/conda/docs/-/blob/master/building_fsl_conda_packages.md) for more information on FSL conda packages.
