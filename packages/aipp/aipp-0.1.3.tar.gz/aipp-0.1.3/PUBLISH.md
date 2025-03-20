# Publishing Python Packages with UV

## Setup

1. Configure `pyproject.toml` with the necessary index information:

```toml
[[tool.uv.index]]
name = "pypi"
url = "https://pypi.org/simple/"
publish-url = "https://upload.pypi.org/legacy/"

[[tool.uv.index]]
name = "testpypi"
url = "https://test.pypi.org/simple/"
publish-url = "https://test.pypi.org/legacy/"
```

2. Authentication options:

**Interactive authentication (recommended):**
When publishing, uv will prompt for credentials if not provided:
```bash
# You'll be prompted for password/token
uv publish --index testpypi --token your-token
```

## Building the Package

```bash
# Build both source distribution and wheel
uv build
```

## Publishing to TestPyPI

```bash
# Upload to TestPyPI
uv publish --index testpypi
```

## Testing the TestPyPI Package

```bash
# Create a test environment
uv venv .venv
source .venv/bin/activate

# Install your package from TestPyPI
uv pip install --index testpypi your-package-name
```

## Publishing to PyPI

```bash
# Upload to PyPI
uv publish --index pypi
```

## Notes

- Always verify your package version in `pyproject.toml` before building
- Use API tokens instead of passwords when possible
- Test your package from TestPyPI before publishing to PyPI
- Consider using keyring or netrc for more secure authentication
