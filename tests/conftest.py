import os
import sys
import shutil
import pytest
from tests.test_base import ICON_GRID_FNAME


# each test runs on cwd to its temp dir
@pytest.fixture(autouse=True)
def go_to_tmpdir(request):
    # Get the fixture dynamically by its name.
    tmpdir = request.getfixturevalue("tmpdir")
    print("trying to copy stuff")
    shutil.copy(os.path.join("tests", ICON_GRID_FNAME), tmpdir)
    # ensure local test created packages can be imported
    sys.path.insert(0, str(tmpdir))
    # Chdir only for the duration of the test.
    with tmpdir.as_cwd():
        yield
