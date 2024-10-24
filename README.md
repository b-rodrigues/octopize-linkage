# octopize-linkage

## Setup
Dependencies are managed with poetry and nix. Installation steps are given below:

### poetry

```bash
poetry lock
poetry install
```

### nix

A `default.nix` is provided at the root of the project. Build the environment using:

```bash
nix-build
```

Drop into an interactive shell using:

```bash
nix-shell
```

From this shell, you can start your IDE which should then have access to the packages.

## Run use cases

Use case scripts are available to run all steps in one go and see how the whole pipeline can be executed.

```bash
poetry run python run_use_case_pra.py
```

or, if you’re using nix:

```bash
nix-shell --run 'python run_use_case_pra.py'
```

## Run tests 

```bash
poetry run pytest <test_feature.py>
```

## Run anonymization with avatar

Generation of anonymous synthetic data can be done with the solution avatar, provided a license to the avatar solution is in place. 

```bash
poetry run python anonymize_pra.py
```


## Planned linkage steps

1. Evaluate linkage potential
Identify common/shared variables between two datasets and evaluate their correlation with the other variables in both datasets
    - if low correlations: impossible to perform linkage (user ned to find a way to get more common variables to "help" linkage)
    - Note: it is important to have correlation with variables in **both** datasets
    - For experiments, this can be evaluated on original data
(If there are many shared variables, find the optimum set of variables to use for linkage (if fewer = better))
    
2. Perform linkage
    - several strategies available
    - need to find the more robust one(s), able to work well on a wide range of datasets

3. Evaluate linkage
    - linkage metrics should be made available
    - metrics will mainly be used in development stage because it may be difficult to assess a good linkage if we cannot get access to both original datasets to get the "ground truth" informations (pairing, correlations etc...).
    - Can we think of linkage metrics computed **without** original datasets ?
    - Comparison of `original_full_df` and `linked(avatar_split_1_df, avatar_split_2_df)`
    - E.g. of metrics:
        - Correlations between variables in data1 (x-axis) and variables in data2 (y-axis) - difference between original "ground truth" correlations and correlations on linked data

4. Correlate pre and post linkage metrics
    - Objective: find out if pre-linkage metrics can predict post-linkage metrics because in practice, we will not be able to run post-linkage metrics.

