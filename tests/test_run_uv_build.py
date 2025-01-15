from pants.testutil.pants_integration_test import run_pants, setup_tmpdir
from pathlib import Path
import os


def test_uv_build() -> None:
    # Define the mock project structure
    sources = {
        "pyproject.toml": """
            [project]
            name = "test-project"
            version = "0.1.0"
    
            dependencies = ["numpy>=1.9"]
            """,
        "BUILD": "files(name='pyproject_toml_files', sources=['pyproject.toml'])",
    }

    # This is a limitation of the current implementation.
    # See https://github.com/pantsbuild/pants/issues/12760.
    build_root_marker = Path.cwd().joinpath("BUILDROOT")
    build_root_marker.touch()

    plugin_path = os.getenv("PANTS_UV_PLUGIN_PATH")
    assert plugin_path is not None, "PANTS_UV_PLUGIN_PATH is not set in the environment"

    # Create temporary directory with the mock project structure
    with setup_tmpdir(sources) as tmpdir:
        # Run the `uv-build` Pants goal
        result = run_pants(
            [
                f"--pythonpath={plugin_path}",
                "--backend-packages=['pants.backend.python','pants_uv_lifecycle_plugin']",
                "uv-build",
            ]
        )

        result.assert_success("`pants uv-build` failed to run.")

        test_project_dist = Path(tmpdir) / "dist"

        # Assert that the `dist` directory exists and is a directory
        assert test_project_dist.exists() and (
            test_project_dist.is_dir(),
            "dist directory not created!",
        )

        # Check for the presence of `.tar.gz` and `.whl` files
        dist_files = list(test_project_dist.glob("*"))
        tar_gz_files = [
            file
            for file in dist_files
            if file.suffix == ".gz" and file.name.endswith(".tar.gz")
        ]
        whl_files = [file for file in dist_files if file.suffix == ".whl"]

        assert tar_gz_files, f"No .tar.gz files found in {test_project_dist}!"
        assert whl_files, f"No .whl files found in {test_project_dist}!"

        build_root_marker.unlink()


def test_uv_missing_target() -> None:
    # Define the mock project structure
    sources = {
        "pyproject.toml": """
            [project]
            version = "0.1.0"

            dependencies = ["numpy>=1.9"]
            """,
        "BUILD": "",
    }

    build_root_marker = Path.cwd().joinpath("BUILDROOT")
    build_root_marker.touch()

    plugin_path = os.getenv("PANTS_UV_PLUGIN_PATH")
    assert plugin_path is not None, "PANTS_UV_PLUGIN_PATH is not set in the environment"

    # Create temporary directory with the mock project structure
    with setup_tmpdir(sources) as tmpdir:
        # Run the `uv-build` Pants goal
        result = run_pants(
            [
                f"--pythonpath={plugin_path}",
                "--backend-packages=['pants.backend.python','pants_uv_lifecycle_plugin']",
                "uv-build",
            ]
        )

        result.assert_failure("`pants uv-build` did not fail as expected.")

        test_project_dist = Path(tmpdir) / "dist"

        # Assert that the `dist` directory does not exist
        assert not test_project_dist.exists(), "dist directory was created in error."

        build_root_marker.unlink()
