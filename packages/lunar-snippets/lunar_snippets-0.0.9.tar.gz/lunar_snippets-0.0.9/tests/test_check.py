import json
from pathlib import Path
import pytest
from src.lunar_snippets import Check


class TestCheck():
    @pytest.fixture(autouse=True)
    def setup_lunar_bundle(self, monkeypatch):
        monkeypatch.setenv(
            'LUNAR_BUNDLE_PATH',
            str(Path(__file__).parent / "sample.json")
        )
        yield

    def test_description_check(self, capsys):
        with Check("test", "description") as f:
            f.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert result["description"] == "description"

    def test_description_not_in_check(self, capsys):
        with Check("test") as f:
            f.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert "description" not in result

    def test_paths_in_check(self, capsys):
        with Check("test") as f:
            v = f.get(".const_false")
            f.assert_false(v)
            f.assert_true(".const_true")

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert result["paths"] == [".const_false", ".const_true"]

    def test_paths_not_in_check(self, capsys):
        with Check("test") as f:
            f.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)

        assert "paths" not in result

    def test_simple_value_check(self, capsys):
        with Check("test") as f:
            f.assert_true(True)

        captured = capsys.readouterr()
        result = json.loads(captured.out)["assertions"][0]

        assert result["op"] == "true"
        assert result["args"] == [True]
        assert result["ok"] is True
        assert "failure_message" not in result

    def test_simple_path_check(self, capsys):
        with Check("test") as f:
            f.assert_true(".const_true")

        captured = capsys.readouterr()
        result = json.loads(captured.out)["assertions"][0]

        assert result["op"] == "true"
        assert result["args"] == [True]
        assert result["ok"] is True
        assert "failure_message" not in result

    def test_multiple_assertions_in_check(self, capsys):
        with Check("test") as f:
            f.assert_true(True)
            f.assert_true(".const_true")

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["ok"] for result in results)

    def test_all_value_assertions_in_check(self, capsys):
        with Check("test") as f:
            f.assert_true(True)
            f.assert_false(False)
            f.assert_equals(1, 1)
            f.assert_greater(2, 1)
            f.assert_greater_or_equal(2, 1)
            f.assert_greater_or_equal(1, 1)
            f.assert_less(1, 2)
            f.assert_less_or_equal(1, 1)
            f.assert_contains("hello", "e")
            f.assert_match("hello", ".*ell.*")

        captured = capsys.readouterr()
        results = json.loads(captured.out)["assertions"]
        assert all(result["ok"] for result in results)
