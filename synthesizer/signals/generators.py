from typing import Final, Self
from numpy import linspace, resize, abs, sin, pi, float64
from numpy.typing import NDArray
from ..config import F_DEFAULT_SAMPLE_RATE


# pi / 2 = 90  degree
# pi     = 180 degree
# 2 * pi = 360 degree (full circuit)
_2PI: Final[float] = pi * 2.0
_1DEGREE: Final[float] = pi / 180.0
MAX_ANGLE: Final[float] = 360.0


class Phase:
    # фаза
    __slots__ = ("angle", "_rad", "_norm")

    def __init__(self, angle: float = 0.0) -> None:
        # angle is: 0 -> 360
        self.angle: float = self._angleNormalize(angle)
        self._rad: float | None = None
        self._norm: float | None = None

    @staticmethod
    def _angleNormalize(angle: float) -> float:
        return angle % MAX_ANGLE

    @property
    def rad(self) -> float:
        # radian is: 0.0 -> 2pi
        if self._rad is None:
            self._rad = self.angle * _1DEGREE
        return self._rad

    @property
    def norm(self) -> float:
        # normalized form is: 0.0 -> 1.0
        if self._norm is None:
            self._norm = self.rad / _2PI
        return self._norm


def _periodDuration(freq: float) -> float:
    # длительность одного периода, секунд
    return 1.0 / freq


def _samplesPerPeriod(freq: float, sampleRate: float) -> int:
    # количество сэмплов в одном периоде
    return round(sampleRate / freq)


def samplesTotal(duration: float, sampleRate: float) -> int:
    # количество сэмплов всего
    return round(duration * sampleRate)


def _periodsAmt(duration: float, freq: float) -> int:
    # количество периодов всего
    return round(duration * freq)


class SinGen:
    __slots__ = ("arr", "dur", "vol", "samplesAmt")

    def __init__(
        self,
        freq: float,
        volume: float = 1.0,
        phase: Phase = Phase(),
        sampleRate: float = F_DEFAULT_SAMPLE_RATE
    ) -> None:
        # Генерируем один период сигнала
        samplesAmt: int = _samplesPerPeriod(freq, sampleRate)
        t: NDArray[float64]
        if phase.angle:
            t = linspace(phase.rad, _2PI + phase.rad, samplesAmt, False, dtype=float64)
        else:
            t = linspace(0.0, _2PI, samplesAmt, False, dtype=float64)
        sin(t, t)
        if volume != 1.0:
            t *= volume
        self.arr: NDArray[float64] = t
        self.dur: float = _periodDuration(freq)
        self.vol: float = volume
        self.samplesAmt: int = samplesAmt

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> NDArray[float64]:
        return self.arr


class SawGen:
    __slots__ = ("arr", "dur", "samplesAmt")

    def __init__(
        self,
        freq: float,
        volume: float = 1.0,
        phase: Phase = Phase(),
        sampleRate: float = F_DEFAULT_SAMPLE_RATE
    ) -> None:
        samplesAmt: int = _samplesPerPeriod(freq, sampleRate)
        t: NDArray[float64]
        if phase.angle:
            t = linspace(phase.norm, 1.0 + phase.norm, samplesAmt, False, dtype=float64)
            t %= 1.0
            t *= 2.0
            t -= 1.0
        else:
            t = linspace(-1.0, 1.0, samplesAmt, False, dtype=float64)
        if volume != 1.0:
            t *= volume
        self.arr: NDArray[float64] = t
        self.dur: float = _periodDuration(freq)
        self.samplesAmt: int = samplesAmt

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> NDArray[float64]:
        return self.arr


class TriGen:
    __slots__ = ("arr", "dur", "samplesAmt")

    def __init__(
        self,
        freq: float,
        volume: float = 1.0,
        phase: Phase = Phase(),
        sampleRate: float = F_DEFAULT_SAMPLE_RATE
    ) -> None:
        samplesAmt: int = _samplesPerPeriod(freq, sampleRate)
        t: NDArray[float64]
        if phase.angle:
            t = linspace(phase.norm, 1.0 + phase.norm, samplesAmt, False, dtype=float64)
            t %= 1.0
            t -= 0.5
            abs(t, t)
            t *= 4.0
            t -= 1.0
        else:
            t = linspace(-1.0, 1.0, samplesAmt, False, dtype=float64)
            abs(t, t)
            t *= 2.0
            t -= 1.0
        if volume != 1.0:
            t *= volume
        self.arr: NDArray[float64] = t
        self.dur: float = _periodDuration(freq)
        self.samplesAmt: int = samplesAmt

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> NDArray[float64]:
        return self.arr


class Wave:
    __slots__ = ("duration", "arr", "samplesAmt", "volume")

    def __init__(self, duration: float, arr: NDArray[float64], samplesAmt: int, volume: float) -> None:
        self.duration: float = duration
        self.arr: NDArray[float64] = arr
        self.samplesAmt: int = samplesAmt
        self.volume: float = volume

    @classmethod
    def generate(
        cls,
        gClass: type[SinGen | SawGen | TriGen],
        freq: float,
        duration: float,
        volume: float = 1.0,
        phase: Phase = Phase(),
        sampleRate: float = F_DEFAULT_SAMPLE_RATE
    ) -> Self:
        samplesAmt: int = samplesTotal(duration, sampleRate)
        return cls(
            duration,
            resize(
                gClass(freq, volume, phase, sampleRate).arr,
                samplesAmt
            ),
            samplesAmt,
            volume
        )
