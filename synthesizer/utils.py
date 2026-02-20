from typing import Final, Iterable, Iterator, overload


_STEP: Final[float] = 1.0


class _1Arg:
    __slots__ = ("curr", "stop")

    def __init__(self, stop: float, /) -> None:
        self.curr: float = 0.0
        self.stop: float = stop

    def __iter__(self) -> Iterator[float]:
        return self

    def __next__(self) -> float:
        if self.curr < self.stop:
            r: float = self.curr
            self.curr += _STEP
            return r
        raise StopIteration


class _2Arg:
    __slots__ = ("curr", "stop")

    def __init__(self, start: float, stop: float, /) -> None:
        self.curr: float = start
        self.stop: float = stop

    def __iter__(self) -> Iterator[float]:
        return self

    def __next__(self) -> float:
        if self.curr < self.stop:
            r: float = self.curr
            self.curr += _STEP
            return r
        raise StopIteration


class _3Arg:
    __slots__ = ("curr", "stop", "step")

    def __init__(self, start: float, stop: float, step: float, /) -> None:
        self.curr: float = start
        self.stop: float = stop
        self.step: float = step

    def __iter__(self) -> Iterator[float]:
        return self

    def __next__(self) -> float:
        if self.curr < self.stop:
            r: float = self.curr
            self.curr += self.step
            return r
        raise StopIteration


@overload
def frange(stop: float, /) -> Iterable[float]: ...
@overload
def frange(start: float, stop: float, /) -> Iterable[float]: ...
@overload
def frange(start: float, stop: float, step: float, /) -> Iterable[float]: ...


def frange(*a: float) -> Iterable[float]:
    if (c := len(a)) == 1:
        return _1Arg(*a)
    if c == 2:
        return _2Arg(*a)
    if c == 3:
        return _3Arg(*a)
    raise TypeError
