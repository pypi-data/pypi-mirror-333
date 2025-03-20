# Release Process

This document describes how to release a new version of the wagtail-block-exchange package.

## Pre-Release Checklist

1. Ensure all tests pass
2. Update the version number in:
   - `setup.py`
   - `package.json`
3. Update the CHANGELOG.md file
4. Make sure the README.md is up to date

## Building the Package

The package includes pre-built JavaScript files, so you don't need to rely on end users having npm installed. The easiest way to build the package is to use the included build script:

```bash
# Run the build script which handles everything
python build_package.py
```

This script will:

1. Clean up previous build directories
2. Build the JavaScript files using npm (if available)
3. Copy the built files to the right locations
4. Build both source and wheel distributions
5. Verify that the JavaScript files are included in the distributions

If you prefer to do these steps manually, here's the process:

```bash
# 1. Install JavaScript dependencies
npm install

# 2. Build the JavaScript bundle
npm run build

# 3. Install Python build tools if not already installed
pip install --upgrade build twine wheel

# 4. Build the Python package (this will include the pre-built JS)
python -m build

# 5. Test the package distribution
twine check dist/*

# 6. Upload to TestPyPI (optional)
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 7. Upload to PyPI
twine upload dist/*
```

## Post-Release Steps

1. Create a new tag for the release:

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Create a GitHub release with the same version number

## Troubleshooting

If the JavaScript files are not included in the package, check:

1. The MANIFEST.in file includes the correct paths
2. The JavaScript files are built before creating the package
3. The directory structure matches what's expected
4. Try running the `build_package.py` script, which includes additional checks
