# Installation

## Requirements

fsl\_sub\_plugin\_slurm requires Python >=3.5 and fsl\_sub >=2.5.0

## Installation within FSL

FSL 6.0.6 and newer ships with fsl\_sub and the SLURM backend installed and ready to use.

FSL 6.0.5 ships with fsl\_sub pre-installed but lacking any grid backends. To install this backend use the fsl\_sub\_plugin helper script:

    $FSLDIR/bin/fsl_sub_plugin -i fsl_sub_plugin_slurm

Note that this command is only supported in FSL 6.0.5 and older - it will not work with versions of FSL newer than 6.0.5.

## Installation outside FSL

### Conda

If you are using Conda then you can install the plugin with the following (note this will automatically install fsl\_sub if required; note also that the package names are delimited with hyphens and not underscores):

    conda install -c https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public -c conda-forge fsl-sub-plugin-slurm

### Virtualenv

If you are using a virtual env, make sure the environment containing fsl\_sub is active and then use:

    pip install git+ssh://git@git.fmrib.ox.ac.uk/fsl/fsl_sub_plugin_slurm.git
