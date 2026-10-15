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


def test_single_game_rejects_invalid_before_render(tmp_path, capsys, monkeypatch):
    from game_infographic_generator.rendering import single_game
    def unexpected(*args):
        raise AssertionError('Rendering must not run')
    monkeypatch.setattr(single_game, 'render_single_game', unexpected)
    metadata = tmp_path / 'bad.json'
    metadata.write_text('{"title": 42}')
    output = tmp_path / 'output.png'
    assert main(['single-game', str(metadata), str(output), '--artwork', str(tmp_path / 'art.png')]) == 1
    assert not output.exists()
    assert 'Validation failed' in capsys.readouterr().err


def test_single_game_dispatch(tmp_path, monkeypatch, capsys):
    from game_infographic_generator.rendering import single_game
    def render(metadata, output, artwork, presentation):
        assert metadata.title == 'Example'
        assert output == tmp_path / 'result.png'
        assert artwork == tmp_path / 'art.png'
        return 1200, 1600
    monkeypatch.setattr(single_game, 'render_single_game', render)
    source = tmp_path / 'input.json'
    source.write_text('{"title":"Example"}')
    assert main(['single-game', str(source), str(tmp_path / 'result.png'), '--artwork', str(tmp_path / 'art.png')]) == 0
    assert '1200 x 1600' in capsys.readouterr().out


def test_single_game_default_without_artwork(tmp_path, monkeypatch):
    from game_infographic_generator.rendering import single_game
    def render(metadata, output, artwork, presentation):
        assert artwork is None and presentation is None
        return 1200, 1600
    monkeypatch.setattr(single_game, 'render_single_game', render)
    source = tmp_path / 'input.json'
    source.write_text('{"title":"Example"}')
    assert main(['single-game', str(source), str(tmp_path / 'out.png')]) == 0
