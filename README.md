# pants-uv-lifecycle-plugin

This repository contains plugins to integrate the following `uv` commands into Pantsbuild lifecycle goals. 

## Dependencies
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Pants](https://www.pantsbuild.org/stable/docs/getting-started/installing-pants)

## Set Up
To initialize the repo, we ran `uv init --lib` and followed the Pantsbuild [initial configuration](https://www.pantsbuild.org/stable/docs/getting-started/initial-configuration) docs.

# Run Plugin
To run a plugin, run `pants <name-of-goal>`. 

## Run Tests
To run the tests within this repo, from the project root, run `pants test ::`. 

## Publish Plugin
Run `uv build && uv publish --publish-url https://test.pypi.org/legacy/`. Currently this is done manually. In the future, we will have plugins to handle this. Additionally, this will be performed in CI.

## Install the Published Plugin
To install the published plugin, add the following to the project's `pants.toml` file.

```
[GLOBAL]
backend_packages = ["pants_uv_lifecycle_plugin"]
plugins = ["pants-uv-lifecycle-plugin==<version>"]
```
## Current Available Plugins
- `uv-sync`: Runs `uv sync` across all modules containing a `pyproject.toml` file within a pants project. 
