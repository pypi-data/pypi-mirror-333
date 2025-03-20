#!/usr/bin/env python
import argparse

import clicktrack


def main(args=None) -> None:
    """Create click track in MIDI format."""

    parser = argparse.ArgumentParser(description='Generate a MIDI click track')
    parser.add_argument('--beats', '-b', type=int, default=4, help='Number of beats in the click track')
    parser.add_argument('--tempo', '-t', type=int, default=60, help='Tempo in beats per minute')
    parser.add_argument('--time-signature', '-ts', type=str, default='4/4', help='Time signature')
    argv = parser.parse_args(args)

    clicktrack.create(argv.beats, argv.tempo, argv.time_signature)


if __name__ == '__main__':
    main()
