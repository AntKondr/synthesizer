from numpy import zeros, float64
from numpy.typing import NDArray
from ..signals.generators import Wave, samplesForDuration
from ..config import CONFIG


class TrackItem:
    __slots__ = ("timeOffset", "wave")

    def __init__(self, timeOffset: float, wave: Wave) -> None:
        self.timeOffset: float = timeOffset
        self.wave: Wave = wave


class TrackBuilder:
    __slots__ = ("items",)

    def __init__(self) -> None:
        self.items: list[TrackItem] = []

    def addItems(self, *items: TrackItem) -> None:
        self.items.extend(items)

    def build(self) -> NDArray[float64]:
        mostItem: TrackItem = max(self.items, key=lambda i: i.timeOffset + i.wave.duration)
        totalDuration: float = mostItem.timeOffset + mostItem.wave.duration
        samplesAmt: int = samplesForDuration(totalDuration, CONFIG.sampleRateF)
        masterBuffer: NDArray[float64] = zeros(samplesAmt, float64)
        for item in self.items:
            idx: int = round(item.timeOffset * CONFIG.sampleRateF)
            masterBuffer[idx:idx + item.wave.samplesAmt] += item.wave.arr
        return masterBuffer
