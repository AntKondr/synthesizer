from typing import Iterator


class FloatRange:
    __slots__ = ()

    def __init__(self, start: float, stop: float, step: float, /) -> None:
        if start >= stop:
            raise ValueError(f"Stop ({stop}) is less or equal than start ({start})!")
        self.start: float = start
        self.stop: float = stop
        self.step: float = step
        self.curr: float = start

    def __iter__(self) -> Iterator[float]:
        return self

    def __next__(self) -> float:
        if self.curr >= self.stop:
            self.curr = self.start
            raise StopIteration
        r: float = self.curr
        self.curr += self.step
        return r
