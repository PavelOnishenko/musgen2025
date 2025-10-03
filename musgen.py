import mido
from mido import MidiFile, MidiTrack, Message
from uuid import uuid4

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

channel = 9
KICK, SNARE, HIHAT = 36, 38, 42

ticks_per_beat = mid.ticks_per_beat
note_len = ticks_per_beat // 8

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

sequence = [
    [HIHAT, KICK], [], [], [],
    [HIHAT], [], [], [],
    [HIHAT, SNARE], [], [], [],
    [HIHAT], [], [], []
] * 4

for events in sequence:
    tick(events)

file_name = f"drums_{uuid4().hex}.mid"
mid.save(file_name)
print(f"✅ Сохранено: {file_name}")