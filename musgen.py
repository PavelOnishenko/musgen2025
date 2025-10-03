import random

import mido
from mido import MidiFile, MidiTrack, Message
from uuid import uuid4

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

channel = 9
KICK, SNARE, HIHAT = 36, 38, 42

STEPS_PER_BEAT = 4

ticks_per_beat = mid.ticks_per_beat
note_len = ticks_per_beat // STEPS_PER_BEAT

def tick(notes):
    if notes:
        for n in notes:
            track.append(Message('note_on', note=n, velocity=80, time=0, channel=channel))
        for i, n in enumerate(notes):
            track.append(Message('note_off', note=n, velocity=0,
                                 time=note_len if i == 0 else 0,
                                 channel=channel))
    else:
        track.append(Message('note_on', note=0, velocity=0, time=note_len, channel=channel))


def generate_basic_sequence(bars=4, steps_per_beat=STEPS_PER_BEAT):
    """Generate a simple but varied drum sequence.

    The pattern aims for a straightforward 4/4 groove with a steady hi-hat,
    kicks on the downbeats, and snares on beats two and four. Randomness is
    introduced to create variation while keeping the groove coherent.
    """

    steps_per_bar = steps_per_beat * 4
    total_steps = bars * steps_per_bar
    sequence = []

    for step in range(total_steps):
        events = []
        beat_position = step % steps_per_bar
        beat_index = beat_position // steps_per_beat  # 0-3 within the bar
        step_in_beat = beat_position % steps_per_beat

        # Hi-hat keeps time on almost every subdivision to anchor the groove.
        hihat_chance = 1.0 if step_in_beat == 0 else 0.85
        if random.random() < hihat_chance:
            events.append(HIHAT)

        # Solid kick on beat one of every bar.
        if beat_index == 0 and step_in_beat == 0:
            events.append(KICK)
        else:
            # Additional kicks on beat three and off-beats with some randomness.
            if beat_index == 2 and step_in_beat == 0 and random.random() < 0.8:
                events.append(KICK)
            elif step_in_beat in (0, 2) and random.random() < 0.25:
                events.append(KICK)

        # Snare backbeat on beats two and four, with occasional extra hits.
        if beat_index in (1, 3) and step_in_beat == 0:
            events.append(SNARE)
        elif beat_index == 1 and step_in_beat == 2 and random.random() < 0.2:
            events.append(SNARE)

        sequence.append(events)

    return sequence


sequence = generate_basic_sequence()

for events in sequence:
    tick(events)

file_name = f"drums_{uuid4().hex}.mid"
mid.save(file_name)
print(f"✅ Сохранено: {file_name}")