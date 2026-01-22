import wave
from numpy import int16
import pyaudio as pa
from synthesizer.signals.generators import Wave, Phase, SinGen, SawGen, TriGen
from synthesizer.signals.func import summWaves, amplitudeModulation, invertWave
from synthesizer.trackBuilder.builder import TrackItem, TrackBuilder
from synthesizer.notes import NOTES
from synthesizer.config import CONFIG


# vol: float = 0.4
# phase: Phase = Phase(0)

# tb: TrackBuilder = TrackBuilder()
# tb.addItems(
#     TrackItem(0.0, Wave.generate(SinGen, NOTES["la3"], 0.8, vol, phase, CONFIG.sampleRateF)),

#     TrackItem(2.0, Wave.generate(SinGen, NOTES["do4"], 0.2, vol, phase, CONFIG.sampleRateF)),
#     TrackItem(2.25, Wave.generate(SinGen, NOTES["do4"], 0.2, vol, phase, CONFIG.sampleRateF)),
#     TrackItem(2.5, Wave.generate(SinGen, NOTES["do4"], 0.2, vol, phase, CONFIG.sampleRateF)),

#     TrackItem(3.0, Wave.generate(SinGen, NOTES["fa3"], 0.4, vol, phase, CONFIG.sampleRateF)),
#     TrackItem(3.5, Wave.generate(SinGen, NOTES["so3"], 0.4, vol, phase, CONFIG.sampleRateF))
# )

# with wave.open("out.wav", "wb") as wavfile:
#     wavfile.setnchannels(1)
#     wavfile.setsampwidth(CONFIG.sampleWidth)
#     wavfile.setframerate(CONFIG.sampleRateF)
#     audio_data = (tb.build() * 32767).astype(int16)
#     wavfile.writeframes(audio_data.tobytes())


tb: TrackBuilder = TrackBuilder()
# la do fa so
tb.addItems(
    TrackItem(
        0.0, summWaves(Wave.generate(SawGen, NOTES["la1"], 2.0), Wave.generate(SawGen, NOTES["la1"] * 2.0, 2.0))
    ),
    TrackItem(
        2.5, summWaves(Wave.generate(SawGen, NOTES["do2"], 2.0), Wave.generate(SawGen, NOTES["do2"] * 2, 2.0))
    ),
    TrackItem(
        5.0, summWaves(Wave.generate(SawGen, NOTES["fa1"], 2.0), Wave.generate(SawGen, NOTES["fa1"] * 2, 2.0))
    ),
    TrackItem(
        7.5, summWaves(Wave.generate(SawGen, NOTES["so1"], 2.0), Wave.generate(SinGen, NOTES["so1"], 2.0))
    )
)
with wave.open("out.wav", "wb") as wavfile:
    wavfile.setnchannels(1)
    wavfile.setsampwidth(CONFIG.sampleWidth)
    wavfile.setframerate(CONFIG.sampleRateF)
    audio_data = (tb.build() * 32767).astype(int16)
    wavfile.writeframes(audio_data.tobytes())

# p = pa.PyAudio()
# stream = p.open(
#     rate=CONFIG.sampleRate,
#     channels=1,
#     format=p.get_format_from_width(CONFIG.sampleWidth),
#     output=True
# )
try:
    # info1 = Wave.generate(TriGen, 300.0, 0.02, 1.0, Phase(0))
    # info2 = SawGen(250.0, 0.3)
    # info = summSignals(info1, info2)
    # inv = invertSignal(info)
    # tr = generateSinSignal(800.0, 0.05, 0.2)

    # audio_data = (tb.build() * 32767).astype(int16)
    # stream.write(audio_data.tobytes())
    pass

except Exception as e:
    print(e)
finally:
    # # останавливаем устройство
    # stream.stop_stream()
    # # завершаем работу PyAudio
    # stream.close()
    # p.terminate()
    pass
