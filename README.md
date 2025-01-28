# pants-uv-lifecycle-plugin

This repository contains plugins to integrate the following `uv` commands into Pantsbuild lifecycle goals. 

## Dependencies
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Pants](https://www.pantsbuild.org/stable/docs/getting-started/installing-pants)

# Run Plugin
To run a plugin, run `pants <name-of-goal>`. 

## Run Tests
To run the tests within this repo, from the project root, run `pants uv-run-behave`. 

## Publish Plugin
Currently this is done by running `pants uv-build` and `pants uv-publish --uv-publish-url https://test.pypi.org/legacy/` within the CI build. 

## Install the Published Plugin
To install the published plugin, add the following to the project's `pants.toml` file.

```
[GLOBAL]
backend_packages = ["pants_uv_lifecycle_plugin"]
plugins = ["pants-uv-lifecycle-plugin==<version>"]
```
## Current Available Plugins
- `uv-sync`: Runs `uv sync` across all modules containing a `pyproject.toml` file within a Pants project. 
- `uv-build`: Runs `uv build` across all modules containing a `pyproject.toml` file within a Pants project. 
- `uv-run-behave`: Runs `uv run behave` across all modules containing `"**/*.feature"` files within a `**/tests/features"` directory within a Pants project. (Note: anytime you run `uv run`, it will create the virtual environment if it doesn't already exist and update the module's `uv.lock` file.)
- `uv-publish`: Runs `uv publish` for each module in a Pants project that contains a `pyproject.toml`, assuming the required build artifacts are already present in those directories. Can be run using the `--uv-publish-url`, `--uv-publish-token`, and `--uv-publish-ignore-dirs` Pants Options. All options can be configured via command-line flags, environment variables, or config files. Reference the [Pants Options documentation](https://www.pantsbuild.org/stable/docs/using-pants/key-concepts/options#options-precedence) for more information on how to use Options.


## Tests 
To test the plugins within a sample project, run the following commands from the root project directory.
```
pants uv-run-behave # the example-project contains a set of simple unit tests
```
