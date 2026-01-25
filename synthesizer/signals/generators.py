from typing import Final, Self
from abc import ABC, abstractmethod
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
    __slots__ = ("_angle", "_rad", "_norm")

    def __init__(self, angle: float = 0.0) -> None:
        # angle is: 0 -> 360
        self._angle: float = self._angleNormalize(angle)
        self._rad: float | None = None
        self._norm: float | None = None

    @staticmethod
    def _angleNormalize(angle: float) -> float:
        return angle % MAX_ANGLE

    def addAngle(self, angle: float) -> Self:
        self._angle = self._angleNormalize(self._angle + angle)
        self._rad = None
        self._norm = None
        return self

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def rad(self) -> float:
        # radian is: 0.0 -> 2pi
        if self._rad is None:
            self._rad = self._angle * _1DEGREE
        return self._rad

    @property
    def norm(self) -> float:
        # normalized form is: 0.0 -> 1.0
        if self._norm is None:
            self._norm = self.rad / _2PI
        return self._norm

    def __bool__(self) -> bool:
        return bool(self._angle)


def _periodDuration(freq: float) -> float:
    # 1 period duration, seconds
    return 1.0 / freq


def _samplesPerPeriod(freq: float, sampleRate: float) -> int:
    # samples amount in 1 period
    return round(sampleRate / freq)


def samplesForDuration(duration: float, sampleRate: float) -> int:
    # samples amount for given duration
    return round(duration * sampleRate)


def _periodsAmt(duration: float, freq: float) -> int:
    # periods amount of given frequency for given duration
    return round(duration * freq)


class PeriodGenerator(ABC):
    __slots__ = ("freq", "volume", "phase", "sampleRate", "samplesAmt", "duration")

    def __init__(
        self,
        freq: float,
        volume: float = 1.0,
        phase: Phase = Phase(),
        sampleRate: float = F_DEFAULT_SAMPLE_RATE
    ) -> None:
        self.freq: float = freq
        self.volume: float = volume
        self.phase: Phase = phase
        self.sampleRate: float = sampleRate
        self.samplesAmt: int = _samplesPerPeriod(freq, sampleRate)
        self.duration: float = _periodDuration(freq)

    # generate 1 period of wave
    @abstractmethod
    def generate(self) -> NDArray[float64]: ...


class SinGen(PeriodGenerator):
    __slots__ = ()

    def generate(self) -> NDArray[float64]:
        t: NDArray[float64]
        if self.phase:
            t = linspace(self.phase.rad, _2PI + self.phase.rad, self.samplesAmt, False, dtype=float64)
        else:
            t = linspace(0.0, _2PI, self.samplesAmt, False, dtype=float64)
        sin(t, t)
        if self.volume != 1.0:
            t *= self.volume
        return t


class SawGen(PeriodGenerator):
    __slots__ = ("flip",)

    def __init__(
        self,
        freq: float,
        volume: float = 1.0,
        phase: Phase = Phase(),
        sampleRate: float = F_DEFAULT_SAMPLE_RATE,
        flip: bool = False
    ) -> None:
        super().__init__(freq, volume, phase.addAngle(180.0), sampleRate)
        self.flip: bool = flip

    def generate(self) -> NDArray[float64]:
        t: NDArray[float64]
        if self.phase:
            t = linspace(1.0 + self.phase.norm, self.phase.norm, self.samplesAmt, False, dtype=float64) if self.flip else linspace(self.phase.norm, 1.0 + self.phase.norm, self.samplesAmt, False, dtype=float64)
            t %= 1.0
            t *= 2.0
            t -= 1.0
        else:
            t = linspace(1.0, -1.0, self.samplesAmt, False, dtype=float64) if self.flip else linspace(-1.0, 1.0, self.samplesAmt, False, dtype=float64)
        if self.volume != 1.0:
            t *= self.volume
        return t


class TriGen(PeriodGenerator):
    __slots__ = ()

    def generate(self) -> NDArray[float64]:
        t: NDArray[float64]
        if self.phase:
            t = linspace(self.phase.norm, 1.0 + self.phase.norm, self.samplesAmt, False, dtype=float64)
            t %= 1.0
            t -= 0.5
            abs(t, t)
            t *= 4.0
            t -= 1.0
        else:
            t = linspace(-1.0, 1.0, self.samplesAmt, False, dtype=float64)
            abs(t, t)
            t *= 2.0
            t -= 1.0
        if self.volume != 1.0:
            t *= self.volume
        return t


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
        gen: PeriodGenerator,
        duration: float
    ) -> Self:
        samplesAmt: int = samplesForDuration(duration, gen.sampleRate)
        return cls(
            duration,
            resize(gen.generate(), samplesAmt),
            samplesAmt,
            gen.volume
        )

    def inverted(self) -> Self:
        # returns new instance
        return type(self)(self.duration, -self.arr.copy(), self.samplesAmt, self.volume)

    def summWaves(self, *w: Self) -> Self:
        # returns new instance
        # TODO compensate amplitude
        grW: Self = max(self, *w, key=_keyMaxWave)
        grArr: NDArray[float64] = grW.arr.copy()
        if grW is not self:
            grArr[0:self.samplesAmt] += self.arr
        for wave in w:
            if grW is not wave:
                grArr[0:wave.samplesAmt] += wave.arr
        return type(self)(grW.duration, grArr, grW.samplesAmt, grW.volume)

    def amplitudeModulation(self, w: Self) -> Self:
        # TODO different lengths of arrays -> ValueError
        newArr: NDArray[float64] = self.arr.copy()
        newArr *= w.arr
        return type(self)(self.duration, newArr, self.samplesAmt, self.volume)


def _keyMaxWave(w: Wave) -> int:
    return w.samplesAmt
