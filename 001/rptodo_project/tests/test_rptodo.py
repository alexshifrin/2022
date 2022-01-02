# tests/test_rptodo.py
import json

import pytest
from typer.testing import CliRunner

from rptodo import (
    DB_READ_ERROR,
    SUCCESS,
    __app_name__,
    __version__,
    cli,
    rptodo,
)

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    todo = [{"Description": "Get some milk", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file