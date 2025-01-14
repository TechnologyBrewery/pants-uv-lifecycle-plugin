from pants.testutil.pants_integration_test import run_pants, setup_tmpdir
from pathlib import Path
import os

def test_uv_run() -> None:
    # Define the mock project structure
    sources = {
        "test-project/pyproject.toml":
        """
        [project]
        name = "test-project"
        version = "0.1.0"

        dependencies = ["numpy>=1.9"]
        """,
    }

    # This is a limitation of the current implementation.
    # See https://github.com/pantsbuild/pants/issues/12760.
    build_root_marker = Path.cwd().joinpath("BUILDROOT")
    build_root_marker.touch()

    plugin_path = os.getenv("PANTS_UV_PLUGIN_PATH")
    assert plugin_path is not None, "PANTS_UV_PLUGIN_PATH is not set in the environment"

    # Create temporary directory with the mock project structure
    with setup_tmpdir(sources) as tmpdir:

        # Run the `uv-sync` Pants goal
        result = run_pants(
            [
                f"--pythonpath={plugin_path}",
                "--backend-packages=['pants.backend.python','pants_uv_lifecycle_plugin']",
                 "uv-sync",
             ]
        )

        # Verify that the command was successful
        result.assert_success('`uv-sync` failed to run.')

        test_project_venv = Path(tmpdir) / "test-project/.venv"

        # Assert that the `.venv` directory exists and is a directory
        assert test_project_venv.exists() and (test_project_venv.is_dir(), "test-project/.venv directory not created!")

        test_project_uv_lock_file = Path(tmpdir) / "test-project/uv.lock"

        # Assert that the `uv.lock` file exists
        assert test_project_uv_lock_file.exists(), "test-project/uv.lock file was not created!"

        build_root_marker.unlink()

def test_uv_run_missing_project_name() -> None:
    # Define the mock project structure
    sources = {
        "test-project/pyproject.toml":
        """
        [project]
        version = "0.1.0"

        dependencies = ["numpy>=1.9"]
        """,
    }

    # This is a limitation of the current implementation.
    # See https://github.com/pantsbuild/pants/issues/12760.
    build_root_marker = Path.cwd().joinpath("BUILDROOT")
    build_root_marker.touch()

    plugin_path = os.getenv("PANTS_UV_PLUGIN_PATH")
    assert plugin_path is not None, "PANTS_UV_PLUGIN_PATH is not set in the environment"

    # Create temporary directory with the mock project structure
    with setup_tmpdir(sources) as tmpdir:

        # Run the `uv-sync` Pants goal
        result = run_pants(
            [
                f"--pythonpath={plugin_path}",
                "--backend-packages=['pants.backend.python','pants_uv_lifecycle_plugin']",
                 "uv-sync",
             ]
        )

        result.assert_failure("`pants uv-sync` did not fail, but it should have failed.")

        build_root_marker.unlink()

def test_uv_run_missing_project_version() -> None:
    # Define the mock project structure
    sources = {
        "test-project/pyproject.toml":
        """
        [project]
        name = "test-project"

        dependencies = ["numpy>=1.9"]
        """,
    }

    # This is a limitation of the current implementation.
    # See https://github.com/pantsbuild/pants/issues/12760.
    build_root_marker = Path.cwd().joinpath("BUILDROOT")
    build_root_marker.touch()

    plugin_path = os.getenv("PANTS_UV_PLUGIN_PATH")
    assert plugin_path is not None, "PANTS_UV_PLUGIN_PATH is not set in the environment"

    # Create temporary directory with the mock project structure
    with setup_tmpdir(sources) as tmpdir:

        # Run the `uv-sync` Pants goal
        result = run_pants(
            [
                f"--pythonpath={plugin_path}",
                "--backend-packages=['pants.backend.python','pants_uv_lifecycle_plugin']",
                 "uv-sync",
             ]
        )

        result.assert_failure("`pants uv-sync` did not fail, but it should have failed.")

        build_root_marker.unlink()

