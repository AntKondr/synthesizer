from numpy import float64, linspace
from numpy.typing import NDArray
from .generators import Wave
from ..config import CONFIG


# def mix_period_to_master(master_buffer, period_array, volume=1.0):
#     # Максимально эффективно подмешивает период в мастер-буфер
#     n_master = len(master_buffer)
#     n_period = len(period_array)
#     # Чтобы не умножать на volume внутри цикла
#     # подготовим временную копию одного маленького периода
#     # (Это единственная маленькая аллокация)
#     temp_period = period_array * volume
#     # Итерируемся по мастер-буферу с шагом в один период
#     for i in range(0, n_master, n_period):
#         # Рассчитываем, сколько семплов влезет (для последнего кусочка)
#         chunk_size = min(n_period, n_master - i)
#         # In-place сложение. NumPy делает это на уровне C-инструкций
#         master_buffer[i : i + chunk_size] += temp_period[:chunk_size]


def _keyWave(wave: Wave) -> int:
    return wave.samplesAmt


def summWaves(*w: Wave) -> Wave:
    # TODO компенсировать амплитуду
    grW: Wave = max(w, key=_keyWave)
    for wave in w:
        grW.arr[0:wave.samplesAmt] += wave.arr
    return grW


def amplitudeModulation(infoSig: list[int], trSig: list[int]) -> list[int]:
    dele: int = (int(CONFIG.maxAmplitude) // 2) - 9800
    newFrame: list[int] = []
    for v1, v2 in zip(infoSig, trSig):
        newFrame.append((v1 * v2) // dele)
    return newFrame


def invertWave(w: Wave) -> Wave:
    w.arr *= -1.0
    return w


def fade(w: Wave) -> Wave:
    # TODO размер фейда
    nSamples: int = w.samplesAmt // 3
    w.arr[:nSamples] *= linspace(0.0, 1.0, nSamples)
    w.arr[-nSamples:] *= linspace(1.0, 0.0, nSamples)
    return w
