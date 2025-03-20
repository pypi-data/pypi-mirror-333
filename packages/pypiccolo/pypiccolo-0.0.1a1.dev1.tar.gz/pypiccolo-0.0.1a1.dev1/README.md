# PyPiccolo Placeholder Package

## Build

```
python3 -m venv build_env
source build_env/bin/activate
pip install --upgrade pip
pip install build
python -m build
```

### Inspect distributions

#### Source distribution

```
cd dist
tar -xvf *.tar.gz
```

#### Binary distribution

```
cd dist
unzip *.whl
```

### Tear down build and build environment

```
deactivate
rm -rf dist src/pypiccolo.egg-info build_env
```

## Push

### Manual publication

TODO

### Automated publication (via `.pypirc`)

```
mkdir -p path/to/registries/testpypi
touch path/to/registries/testpypi/.pypirc
chmod 600 path/to/registries/testpypi/.pypirc
```

```
echo "\
[distutils]\n\
  index-servers = testpypi\n\
" >> path/to/registries/testpypi/.pypirc

echo "\
[testpypi]\n\
  username = __token__\n\
  password = ${TOKEN}\n\
" >> path/to/registries/testpypi/.pypirc
```

```
python3 -m venv push_env
source push_env/bin/activate
pip install --upgrade pip
pip install twine
HOME=path/to/registries/testpypi twine upload --repository=testpypi dist/*
deactivate
rm -rf push_env
```

### Automated publication (via CI/CD)

TODO

### Note

- Unfortunately, public Python version identifiers are not fully compatible with semantic versioning identifiers (see https://packaging.python.org/en/latest/specifications/version-specifiers/), although they are compatible with the `X.Y.Z` notation of semantic versioning for major/minor/patch version numbers, and there exists an analogous notion of release candidates.


## Pull

```
python3 -m venv pull_env
source pull_env/bin/activate
pip install --upgrade pip
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pypiccolo==0.0.1a1.dev1
deactivate
rm -rf pull_env
```

## Setuptools usage

### Notes on package discovery, package data, and runtime configuration

- Setuptools offers a variety of means of discovering and/or specifying packages and modules to be included in the distribution (https://setuptools.pypa.io/en/latest/userguide/package_discovery.html). While setuptools offers means of implicitly discovering package layout (flat- vs. src-layout), and of explicitly specifying packages to be included, the means chosen by the present project is to explicitly specify package layout (i.e. using `package-dir` to specify src-layout), while not explicitly specifying packages to be included (i.e. not using `package`, in order to retain flexibility).

- Setuptools also offers several means of specifying data files to be included/excluded from the distribution (https://setuptools.pypa.io/en/latest/userguide/datafiles.html). Crucially, data files are meant to be read-only; it is recommended that shared and/or writable data files be installed outside the package directory in an appropriate location.

- Source distributions also include a number of files by default, including files matching `test[s]/test*.py`, license files (unless otherwise specified via `license-files`), `pyproject.toml`, files matching `setup.{cfg,py}`, README files, and `MANIFEST.in`, unless otherwise specified by `MANIFEST.in` (https://setuptools.pypa.io/en/latest/userguide/miscellaneous.html); however, binary distributions do not. Crucially, binary distributions cannot depend on tests in `test[s]/test*.py`.

### Miscellaneous notes

- All of the `[project]` table entries of the `pyproject.toml` are standardized, with the exception of `license`. The PEP 639 standard defines new `[project]` table entries `license` (corresponding to a valid SPDX license expression) and `license-files` (corresponding to a list of license file glob paths). As `setuptools` is yet to support this standard, the legacy declaration is used instead; it is of the form `license = { text = "MIT License" }` or `license = { file = "LICENSE" }`. Note that other license files will still be included in the metadata, and hence both the source and binary distributions, unless the `license-files` entry of the `[tool.setuptools]` table is also used. It is expected that once `setuptools` adds support for PEP 639 that the `license-files` entry of the `[tools.setuptools]` table will be deprecated (or at least redundant).

- Depending on the versions of Python, `build`, and `setuptools` that are employed, it may be necessary to include a boilerplate `setup.py` file consisting of `from setuptools import setup; setup();` for backwards compatibility.

## References

### Tutorials

- https://packaging.python.org/en/latest/tutorials/packaging-projects/

### Guides

- https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
- https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#platform-wheels
- https://packaging.python.org/en/latest/guides/packaging-binary-extensions/
- https://packaging.python.org/en/latest/guides/using-testpypi/
- https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
- https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html

### Specifications

- https://packaging.python.org/en/latest/specifications/version-specifiers/
- https://packaging.python.org/en/latest/specifications/pyproject-toml/
- https://packaging.python.org/en/latest/specifications/pypirc/
- https://pypi.org/classifiers/

### Examples

- https://github.com/pypa/sampleproject
