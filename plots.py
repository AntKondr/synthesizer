from matplotlib import pyplot
from synthesizer.signals.generators import Wave, Phase, SinGen, SawGen, TriGen
from synthesizer.signals.func import summWaves, amplitudeModulation, invertWave, fade
from synthesizer.notes import NOTES
from synthesizer.config import CONFIG


nrows = 3


w1 = Wave.generate(SinGen, 180.0, 0.01, 1.0, Phase(0))
w2 = Wave.generate(SinGen, 1800.0, 0.01, 0.6, Phase(0))
w3 = Wave.generate(SinGen, 360.0, 0.01)
# inv = invertSignal(info)
# tr = generateSinSignal(800.0, 0.05, 0.2)
# mod = ampMod(info, tr)
pyplot.subplot(nrows, 1, 1)
pyplot.plot(w1.arr)

# pyplot.subplot(nrows, 1, 2)
pyplot.plot(w2.arr)

pyplot.subplot(nrows, 1, 2)
pyplot.plot(summWaves(w1, w2).arr)

pyplot.subplot(nrows, 1, 3)
pyplot.plot(fade(w3).arr)
# pyplot.subplot(3, 1, 3)
# pyplot.plot(inv)
# pyplot.plot(tr)
# pyplot.plot(mod)
pyplot.show()
