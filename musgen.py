import mido
from mido import MidiFile, MidiTrack, Message

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

channel = 9  # 10-й канал для ударных
KICK, SNARE, HIHAT = 36, 38, 42

ticks_per_beat = mid.ticks_per_beat
note_len = ticks_per_beat // 8   # длительность = 1/32
eighth = ticks_per_beat // 2     # для позиционирования хэта

for bar in range(4):
    for beat in range(4):
        
        track.append(Message('note_on', note=HIHAT, velocity=70, time=0, channel=channel))
        
        if beat in [0, 2]: 
            track.append(Message('note_on', note=KICK, velocity=100, time=0, channel=channel))

        if beat in [1, 3]:
            track.append(Message('note_on', note=SNARE, velocity=100, time=0, channel=channel))
        
        track.append(Message('note_off', note=HIHAT, velocity=0, time=note_len, channel=channel))

        if beat in [0, 2]: 
            track.append(Message('note_off', note=KICK, velocity=0, time=0, channel=channel))
            
        if beat in [1, 3]:
            track.append(Message('note_off', note=SNARE, velocity=0, time=0, channel=channel))
            

        # пауза = оставшееся время до середины доли
        rest = eighth - note_len
        if rest > 0:
            track.append(Message('note_on', note=HIHAT, velocity=0, time=rest, channel=channel))  # пустышка

        # второй удар (середина доли)
        track.append(Message('note_on', note=HIHAT, velocity=60, time=0, channel=channel))
        track.append(Message('note_off', note=HIHAT, velocity=0, time=note_len, channel=channel))

        # пауза = оставшееся время до конца доли
        rest = eighth - note_len
        if rest > 0:
            track.append(Message('note_on', note=HIHAT, velocity=0, time=rest, channel=channel))  # пустышка

mid.save("drums_1_32.mid")
print("✅ Сохранено: drums_1_32.mid")
