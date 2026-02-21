from typing import Final, Self, Any
from argparse import ArgumentParser
from pathlib import Path
from json import load


# sampling rate (samples amount (length samples array) for 1 second)
_DEFAULT_SAMPLE_RATE: Final[int] = 44100
_SAMPLE_RATES: Final[tuple[int, ...]] = (
    8000,           # 8000 Hz: telephony, voice calls (adequate for speech)
    16000,          # 16000 Hz: VoIP, video conferencing (better voice quality)
    11025, 22050,   # 11025 Hz / 22050 Hz: low-quality PCM, audio analysis
    44100,          # 44100 Hz: standard for audio CDs, MP3s, general music
    48000,          # 48000 Hz: standard for digital video, DVD, Blu-ray, streaming
    88200, 96000,   # 88200 Hz / 96000 Hz: high-resolution audio, professional recording, mastering (Blu-ray)
    176400, 192000  # 176400 Hz / 192000 Hz: high-resolution/audiophile formats, professional studio recording (DVD-Audio, Blu-ray)
)

# глубина, бит (signed)
_DEFAULT_BIT_DEPTH: Final[int] = 16
_BIT_DEPTHS: Final[tuple[int, ...]] = (8, 16, 24, 32)

# buffer size for samples
_DEFAULT_BUFF_SIZE: Final[int] = 512

_DEFAULT_CONFIG_PATH: Final[Path] = Path(__file__).parent.parent / "config.json"


class _Config:
    __slots__ = ("_confFile", "sampleRate", "sampleRateF", "sampleTime", "bitDepth", "buffSize", "sampleWidth", "maxAmplitude", "minAmplitude")

    def __init__(self, confFile: Path) -> None:
        self._confFile: Final[Path] = confFile

    def initialize(self) -> Self:
        with open(self._confFile, "tr", -1, "utf_8") as f:
            conf: dict[str, Any] = load(f)

        # sampling rate
        if (v := conf.get("SAMPLE_RATE", _DEFAULT_SAMPLE_RATE)) not in _SAMPLE_RATES:
            raise ValueError(f"Invalid sample rate -> {v}")
        self.sampleRate: int = v
        self.sampleRateF: float = float(v)

        # time between two samples
        self.sampleTime: float = 1.0 / self.sampleRateF

        # bit depth
        if (v := conf.get("BIT_DEPTH", _DEFAULT_BIT_DEPTH)) not in _BIT_DEPTHS:
            raise ValueError(f"Invalid bit depth -> {v}")
        self.bitDepth: int = v

        # buffer size for samples
        self.buffSize: int = int(conf.get("BUFF_SIZE", _DEFAULT_BUFF_SIZE))

        # ----- calculated fields ------------------------------------
        # bytes amount into depth
        self.sampleWidth: int = self.bitDepth // 8

        # bound values ​​of amplitude for a given bit depth
        self.maxAmplitude: float = float((2 ** (self.bitDepth - 1)) - 1)
        self.minAmplitude: float = (self.maxAmplitude + 1.0) * -1.0
        return self


_argp: ArgumentParser = ArgumentParser()
_argp.add_argument("-c", "--config", metavar="", help="config file path")
_args = _argp.parse_args()

CONFIG: Final[_Config] = _Config(Path(_args.config) if _args.config else _DEFAULT_CONFIG_PATH).initialize()
