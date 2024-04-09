# How to develop on this project

icon_uxarray welcomes contributions from the community.

**You need PYTHON >= 3.10!**

## install for developing

```bash
# Clone the repository
git git@github.com:jcanton/icon_uxarray.git
cd icon_uxarray

# Create a virtual environment
# This step already installs all the packages and dependencies
make virtualenv

# Activate the virtual environment
source .venv/bin/activate

# Finally, check that everything works
make test
```