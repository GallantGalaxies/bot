from collections.abc import Callable
from typing import Any

import numpy as np
from numpy.typing import NDArray


def noise_psd(n: int, psd: Callable = lambda: 1) -> np.ndarray:
    """Return a time series of length N with a given power spectral."""
    rng = np.random.default_rng()
    x_white = np.fft.rfft(rng.standard_normal(n))

    sound_array = psd(np.fft.rfftfreq(n))
    sound_array = sound_array / np.sqrt(np.mean(sound_array**2))
    x_shaped = x_white * sound_array
    return np.fft.irfft(x_shaped)


def psd_generator(f: Callable) -> Callable:
    """Return functions that generate power spectral densities."""
    return lambda n: noise_psd(n, f)


@psd_generator
def white_noise() -> int:
    """Return white noise."""
    return 1


@psd_generator
def blue_noise(f: int) -> int:
    """Return blue noise."""
    return np.sqrt(f)


@psd_generator
def violet_noise(f: int) -> int:
    """Return violet noise."""
    return f


@psd_generator
def brownian_noise(f: int) -> NDArray[Any, np.dtype[np.float64]]:
    """Return brownian noise."""
    return 1 / np.where(f == 0, float("inf"), f)


@psd_generator
def pink_noise(f: int) -> NDArray[Any, np.dtype[np.float64]]:
    """Return pink noise."""
    return 1 / np.where(f == 0, float("inf"), np.sqrt(f))
