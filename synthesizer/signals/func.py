from numpy import float64, linspace
from numpy.typing import NDArray
from .generators import Wave
from ..config import CONFIG


def fade(w: Wave) -> Wave:
    # TODO размер фейда
    nSamples: int = w.samplesAmt // 3
    w.arr[:nSamples] *= linspace(0.0, 1.0, nSamples)
    w.arr[-nSamples:] *= linspace(1.0, 0.0, nSamples)
    return w
