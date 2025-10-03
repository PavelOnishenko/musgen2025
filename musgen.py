import random

import mido
from mido import MidiFile, MidiTrack, Message
from uuid import uuid4

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

channel = 9
KICK, SNARE, HIHAT = 36, 38, 42
BASE_VELOCITY = 80
KICK_VELOCITY = round(BASE_VELOCITY * 1.3)

STEPS_PER_BEAT = 4

ticks_per_beat = mid.ticks_per_beat
note_len = ticks_per_beat // STEPS_PER_BEAT


def tick(notes):
    if notes:
        for n in notes:
            velocity = KICK_VELOCITY if n == KICK else BASE_VELOCITY
            track.append(Message('note_on', note=n, velocity=velocity, time=0, channel=channel))
        for i, n in enumerate(notes):
            track.append(Message('note_off', note=n, velocity=0,
                                 time=note_len if i == 0 else 0,
                                 channel=channel))
    else:
        track.append(Message('note_on', note=0, velocity=0, time=note_len, channel=channel))


def generate_basic_bar(steps_per_beat=STEPS_PER_BEAT):
    """Return a bar using the structured groove pattern."""
    steps_per_bar = steps_per_beat * 4
    bar = []
    for step in range(steps_per_bar):
        events = []
        beat_position = step % steps_per_bar
        beat_index = beat_position // steps_per_beat
        step_in_beat = beat_position % steps_per_beat
        hihat_chance = 1.0 if step_in_beat == 0 else 0.85
        if random.random() < hihat_chance:
            events.append(HIHAT)
        if beat_index == 0 and step_in_beat == 0:
            events.append(KICK)
        else:
            if beat_index == 2 and step_in_beat == 0 and random.random() < 0.8:
                events.append(KICK)
            elif step_in_beat in (0, 2) and random.random() < 0.25:
                events.append(KICK)
        if beat_index in (1, 3) and step_in_beat == 0:
            events.append(SNARE)
        elif beat_index == 1 and step_in_beat == 2 and random.random() < 0.2:
            events.append(SNARE)
        bar.append(events)
    return bar


def generate_chaos_bar(steps_per_beat=STEPS_PER_BEAT):
    """Return a bar with randomized hit counts and placements."""
    steps_per_bar = steps_per_beat * 4
    bar = [[] for _ in range(steps_per_bar)]

    def place_random_hits(note, count):
        if count <= 0:
            return
        count = min(count, steps_per_bar)
        indices = random.sample(range(steps_per_bar), count)
        for idx in indices:
            bar[idx].append(note)

    kick_hits = random.randint(0, steps_per_beat)
    snare_hits = random.randint(0, steps_per_beat)
    hihat_hits = random.randint(steps_per_beat, steps_per_bar)

    place_random_hits(KICK, kick_hits)
    place_random_hits(SNARE, snare_hits)
    place_random_hits(HIHAT, hihat_hits)

    return bar


def generate_sequence(bars=4, steps_per_beat=STEPS_PER_BEAT):
    """Generate a drum sequence selecting a mode per bar."""
    modes = (generate_basic_bar, generate_chaos_bar)
    sequence = []
    for _ in range(bars):
        generator = random.choice(modes)
        sequence.extend(generator(steps_per_beat=steps_per_beat))
    return sequence


sequence = generate_sequence()

for events in sequence:
    tick(events)

file_name = f"drums_{uuid4().hex}.mid"
mid.save(file_name)
print(f"✅ Сохранено: {file_name}")
