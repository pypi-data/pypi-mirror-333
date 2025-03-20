# fsl_sub_plugin_slurm release history

## 1.6.6

* Fix enumeration of and validation of accounts

## 1.6.5

* GPU class selection refactored
* Additional tests
* Detection and handling of constraints in --extra_args
* Fix handling of job name when none provided
* Refactor log location handling
* Change to requesting memory via --mem to avoid issues with SMT systems
* Add additional environment variable, FSLSUB_NORAMLIMIT, to allow user to temporarily disable notifying SLURM of RAM requirements

## 1.6.4

* Multiple fixes for GPU class selection when not using constraints

## 1.6.3

* Add option/environment variable to enable nested queuing of tasks - principally of use when using Open OnDemand desktop environments

## 1.6.2

* Fix array limit application

## 1.6.1

* Fix job submission if empty list provided as job dependencies

## 1.6.0

* Refactor job dependency processing to simplify testing
* Modified default job hold type to be 'afterany', the sbatch default for a dependency
* Added new configuration option and environment variable to control whether 'afterany' or 'afterok' is used.
* Added ability to specify a complex job hold in the -j argument

## 1.5.2

* Keep the job launch script (when requested to) on error
* Improve documentation of keep_jobscript

## 1.5.1

* Add license file
* Change to release status

## 1.5.0

* Fix specification of constraints
* Add mem-per-gpu and cpus-per-gpu support

## 1.4.4

* Resolve issue with saving the job script where the location of temporary files is on a different file system to the current working directory.

## 1.4.3

* Resolve issues with multi-thread/slot job submission and the setting of ntasks.
* Improve clarity of example configuration, especially with respect to possible GPU configuration

## 1.4.2

* Documentation changes for migration to conda-based FSL.

## 1.4.1

* Improve handling of job scripts (--usescript command line option)
* Resolve issues in job submission when keep_jobscript not turned on

## 1.4.0

* Implement scheduler argument pass-through
* Prevent re-loading of modules if environment passing has been configured
* Ensure coprocessor environment module is loaded if specified

## 1.3.8

* Implement documented (but not-implemented) export_vars configuration option

## 1.3.7

* Support environment variables that have an '=' in their value

## 1.3.6

* Changes to tests for latest fsl_sub version

## 1.3.5

* Fixed array task wrapper generation

## 1.3.4

* Fixed queue capture when queue has infinite duration
* Fixed tests to take into account --chdir is now always set
* Fixed typo in --dependency option

## 1.3.3

* Documentation clean up
* Changed options for SLURM GPU constraints
* Add support for auto-configuring partitions

## 1.3.2

* First public release
* Add support for comma and space in exported environment variables

## Pre-1.3.2

Pre-release versions
