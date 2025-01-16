# pants-uv-lifecycle-plugin

This repository contains plugins to integrate the following `uv` commands into Pantsbuild lifecycle goals. 

## Dependencies
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Pants](https://www.pantsbuild.org/stable/docs/getting-started/installing-pants)

# Run Plugin
To run a plugin, run `pants <name-of-goal>`. 

## Run Tests
To run the tests within this repo, from the project root, run `pants test ::`. 

## Publish Plugin
Currently this is done by running `uv build` and `uv publish --publish-url https://test.pypi.org/legacy/` within the CI build. 

## Install the Published Plugin
To install the published plugin, add the following to the project's `pants.toml` file.

```
[GLOBAL]
backend_packages = ["pants_uv_lifecycle_plugin"]
plugins = ["pants-uv-lifecycle-plugin==<version>"]
```
## Current Available Plugins
- `uv-sync`: Runs `uv sync` across all modules containing a `pyproject.toml` file within a pants project. 
