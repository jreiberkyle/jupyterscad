# Contributing

Thank you for your interest in contributing to Jupyter SCAD! This
document explains how to contribute successfully.

## Workflows

### Development

#### Development Branch

Implementation of new features will be tracked in the `main` branch, while bug
fixes and doc changes for the latest release will be tracked in the maintenance
branch, called `maint-RELEASE_VERSION`. All work will be performed in a
new development branch starting with the appropriate base branch and merged
back into that branch.

For new features:

```console
git checkout main
git pull
git checkout -b new-branch-name
```

For example, for bug fixes and doc changes to release version 1.1:

```console
git checkout maint-1.1
git pull
git checkout -b new-branch-name
```

#### Branch Naming

Please use the following naming convention for development branchs:

`{up to 3-word summary of topic, separated by a dash)-{ticket number}`


#### Changelog

Add the changes to the Unreleased section of `CHANGELOG.md`. Instructions for
doing so are given at the top of `CHANGELOG.md`.

### Pull Requests

NOTE: Make sure to set the appropriate base branch for PRs. See Development Branch above for appriopriate branch.

Prior to review, the PR must pass Continuous Integration (CI) checks.

To minimize the feedback loop, we have configured Nox so that it can be used to run all of the CI checks on the local machine. See the [Development Tools](#development-tools) section for information on running CI checks locally with Nox.


## <a name="development-tools"></a>Development Tools

This repository uses [Nox](https://nox.thea.codes/) to automate development.

Install Nox in your local dev environment:

```console
    $ pip install nox
```

To run nox with the default sessions (same checks as CI) type "nox".

```console
    $ nox
```

If no changes have been made to the Nox environment since it was last run,
speed up the run by reusing the environment:

```console
    $ nox -r
```

If only one test is desired, specify it with `-s` and if only one python version
is desired, specify it with `-p`. To only run tests on python 3.10:

```console
$ nox -s tests -p 3.10
```

The configuration for Nox is given in `noxfile.py`. See the Nox link above for
advanced usage.
