python_requirements(source="pyproject.toml")
pants_requirements(name="pants", resolve="pants-uv-lifecycle-plugin")

# Generates File target for each file in the sources field - useful if you want to treat all targets uniformly
files(
    name="pyproject_toml_files",
    sources=["**/pyproject.toml"],
    description="Files target representing all pyproject.toml files",
    tags=["pyproject-toml-files"],
)

# Generates File target for each file in the sources field - useful if you want to treat all targets uniformly
files(
    name="feature_files",
    sources=["**/*.feature"],
    description="Files target representing all behave *.feature files",
    tags=["feature-files"],
)
