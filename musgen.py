import mido
from mido import MidiFile, MidiTrack, Message

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

channel = 9 
KICK, SNARE, HIHAT = 36, 38, 42

ticks_per_beat = mid.ticks_per_beat
quarter = ticks_per_beat
eighth = ticks_per_beat // 2

# 4 такта по 4/4
for bar in range(4):
    for beat in range(4):
        if beat in [0, 2]:  # кик на 1 и 3
            track.append(Message('note_on', note=KICK, velocity=100, time=0, channel=channel))
            track.append(Message('note_off', note=KICK, velocity=0, time=0, channel=channel))

        if beat in [1, 3]:  # снейр на 2 и 4
            track.append(Message('note_on', note=SNARE, velocity=100, time=0, channel=channel))
            track.append(Message('note_off', note=SNARE, velocity=0, time=0, channel=channel))

        # хай-хэт восьмыми (два удара на долю)
        # первый — вместе с киком/снейром
        track.append(Message('note_on', note=HIHAT, velocity=70, time=0, channel=channel))
        track.append(Message('note_off', note=HIHAT, velocity=0, time=eighth, channel=channel))

        # второй — через восьмую
        track.append(Message('note_on', note=HIHAT, velocity=60, time=0, channel=channel))
        track.append(Message('note_off', note=HIHAT, velocity=0, time=eighth, channel=channel))

mid.save("drums_groove.mid")
print("✅ Сохранено: drums_groove.mid")
