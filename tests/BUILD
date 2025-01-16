# This target sets the metadata for all the Python test files in this directory.
python_tests(name="pants-uv-lifecycle-plugin-tests")

# Temporary fix to resolve warning when running `pants test ::`. This is an existing issue and is being tracked at https://github.com/pantsbuild/pants/issues/21382
python_requirement(
    requirements=["pytest<7.1.0,>=6.2.4"], resolve="pants-uv-lifecycle-plugin"
)
