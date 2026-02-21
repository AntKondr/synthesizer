from typing import Final, Iterable, Iterator


_STEP: Final[float] = 1.0


def _iter(self) -> Iterator[float]:
    return self


def _defaultNext(self) -> float:
    if self.curr < self.stop:
        r: float = self.curr
        self.curr += _STEP
        return r
    raise StopIteration


class _1Arg:
    __slots__ = ("curr", "stop")
    __iter__ = _iter
    __next__ = _defaultNext

    def __init__(self, stop: float, /) -> None:
        self.curr: float = 0.0
        self.stop: float = stop


class _2Arg:
    __slots__ = ("curr", "stop")
    __iter__ = _iter
    __next__ = _defaultNext

    def __init__(self, start: float, stop: float, /) -> None:
        self.curr: float = start
        self.stop: float = stop


class _3ArgPos:
    __slots__ = ("curr", "stop", "step")
    __iter__ = _iter

    def __init__(self, start: float, stop: float, step: float, /) -> None:
        self.curr: float = start
        self.stop: float = stop
        self.step: float = step

    def __next__(self) -> float:
        if self.curr < self.stop:
            r: float = self.curr
            self.curr += self.step
            return r
        raise StopIteration


class _3ArgNeg:
    __slots__ = ("curr", "stop", "step")
    __iter__ = _iter

    def __init__(self, start: float, stop: float, step: float, /) -> None:
        self.curr: float = start
        self.stop: float = stop
        self.step: float = step

    def __next__(self) -> float:
        if self.curr > self.stop:
            r: float = self.curr
            self.curr += self.step
            return r
        raise StopIteration


def frange(*a: float) -> Iterable[float]:
    if (c := len(a)) == 1:
        return _1Arg(*a)
    if c == 2:
        return _2Arg(*a)
    if c == 3:
        if a[2] > 0.0:
            return _3ArgPos(*a)
        if a[2] < 0.0:
            return _3ArgNeg(*a)
        raise ValueError("frange() arg step must not be zero")
    raise TypeError("frange() expected from 1 to 3 args")
