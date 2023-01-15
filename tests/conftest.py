import shutil
import uuid
from pathlib import Path

import pytest

from . import DATA_DIR

TEST_FILENAME = "empty_db.kdbx"


@pytest.fixture
def keepass_file(tmp_path) -> Path:
    """'Create' an empty KeePass file in a temp directory."""
    source = DATA_DIR / TEST_FILENAME
    dest_filename = uuid.uuid4().hex + ".kdbx"
    dest = tmp_path / dest_filename

    shutil.copy(source, dest)

    return dest
