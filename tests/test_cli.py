from game_infographic_generator.cli import main


def test_cli_prints_readiness_message(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out == "Game Infographic Agent ready\n"
    assert captured.err == ""
