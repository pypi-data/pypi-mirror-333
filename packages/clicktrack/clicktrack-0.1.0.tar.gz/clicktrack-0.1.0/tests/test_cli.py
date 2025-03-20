from contextlib import suppress

from clicktrack.cli import main


def test_cli_help(capsys):
    with suppress(SystemExit):
        main(['-h'])
    output = capsys.readouterr().out
    assert 'click track' in output
