# How to develop on this project

icon_uxarray welcomes contributions from the community.

**You need PYTHON3!**

## install for developing

```bash
# Clone the repository
git git@github.com:jcanton/icon_uxarray.git
cd icon_uxarray

# Create a virtual environment
make virtualenv

# Activate the virtual environment and make sure that 'wheel' is installed
source .venv/bin/activate
pip install --upgrade wheel

# Install all the packages and dependencies
make install

# Finally, check that everything works
make test
```