# SPDX-FileCopyrightText: 2025-present Ramiro Gómez <code@ramiro.org>
#
# SPDX-License-Identifier: MIT
from midiutil import MIDIFile  # type: ignore


def create(beats, tempo, time_signature):
    beats_per_bar, beat_unit = map(int, time_signature.split('/'))

    # Create MIDI file with 1 track
    midi = MIDIFile(1)

    # Track settings
    track = 0
    channel = 9  # Channel 10 (zero-based) is traditionally used for percussion
    time = 0

    midi.addTempo(track, time, tempo)

    # Woodblock sounds, use higher pitch for first beat of a bar
    high_woodblock = 76
    low_woodblock = 77

    volume = 100

    # Calculate the duration of each beat in terms of quarter notes
    beat_duration = 4 / beat_unit

    # Create clicks
    for beat in range(beats):
        # Use high woodblock for first beat of a bar, low woodblock for others
        pitch = high_woodblock if (beat % beats_per_bar) == 0 else low_woodblock
        midi.addNote(track, channel, pitch, time + beat * beat_duration, 0.1, volume)

    # Write MIDI file
    ts_slug = time_signature.replace('/', '-')
    filename = f'{beats}-beats-{ts_slug}-meter-{tempo}-bpm.mid'
    with open(filename, 'wb') as output:
        midi.writeFile(output)
