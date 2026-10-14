from game_infographic_generator.cli import main


def test_cli_prints_readiness_message(capsys):
    main([])
    captured = capsys.readouterr()
    assert captured.out == "Game Infographic Agent ready\n"
    assert captured.err == ""


def test_validate_fixture(capsys):
    from pathlib import Path

    fixture = Path(__file__).parent / "fixtures" / "game_metadata.json"
    assert main(["validate", str(fixture)]) == 0
    assert "Valid game metadata:" in capsys.readouterr().out


def test_invalid_inputs(tmp_path, capsys):
    for content in ('{', '{"title": 42}', '{"title": "Game", "extra": 1}'):
        path = tmp_path / "invalid.json"
        path.write_text(content)
        assert main(["validate", str(path)]) == 1
        captured = capsys.readouterr()
        assert "Validation failed:" in captured.err
        assert captured.out == ""


def test_missing_file(tmp_path, capsys):
    assert main(["validate", str(tmp_path / "missing.json")]) == 1
    assert "Validation failed:" in capsys.readouterr().err


def test_module_exit_status(tmp_path):
    import os
    from pathlib import Path
    import subprocess
    import sys

    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1] / "src"))
    result = subprocess.run(
        [sys.executable, "-m", "game_infographic_generator", "validate",
         str(tmp_path / "missing.json")],
        capture_output=True, text=True, env=env,
    )
    assert result.returncode == 1
    assert "Validation failed:" in result.stderr
