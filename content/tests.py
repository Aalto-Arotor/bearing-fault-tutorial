import numpy as np


def _analytic_signal_fft(x):
    """Compute analytic signal using FFT-domain Hilbert transform."""
    x = np.asarray(x)
    N = x.size
    Xf = np.fft.fft(x)
    h = np.zeros(N)

    if N % 2 == 0:
        h[0] = 1
        h[N // 2] = 1
        h[1:N // 2] = 2
    else:
        h[0] = 1
        h[1:(N + 1) // 2] = 2

    return np.fft.ifft(Xf * h)


def check_bpfo(bpfo_hz, n, d, D, phi, f_r, rtol=1e-4, atol=1e-8):
    """Return feedback message for BPFO calculation."""
    bpfo_expected = (n / 2) * f_r * (1 - (d / D) * np.cos(phi))

    try:
        bpfo_value = float(bpfo_hz)
    except (TypeError, ValueError):
        return "❌ BPFO_Hz must be a numeric value."

    if np.isclose(bpfo_value, bpfo_expected, rtol=rtol, atol=atol):
        return "✅ BPFO_Hz looks correct."

    return "❌ BPFO_Hz is not correct yet. Check the BPFO formula and try again."


def _check_frequency(value, expected, name, rtol=1e-4, atol=1e-8):
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return f"❌ {name} must be a numeric value."

    if np.isclose(numeric_value, expected, rtol=rtol, atol=atol):
        return f"✅ {name} looks correct."

    return f"❌ {name} is not correct yet. Check the formula and try again."


def check_all_frequencies(bpfo_hz, bpfi_hz, ftf_hz, bsf_hz, n, d, D, phi, f_r, rtol=1e-4, atol=1e-8):
    """Return feedback messages for BPFO, BPFI, FTF and BSF calculations."""
    bpfo_expected = (n / 2) * f_r * (1 - (d / D) * np.cos(phi))
    bpfi_expected = (n / 2) * f_r * (1 + (d / D) * np.cos(phi))
    ftf_expected = (f_r / 2) * (1 - (d / D) * np.cos(phi))
    bsf_expected = (D * f_r / (2 * d)) * (1 - ((d / D) * np.cos(phi)) ** 2)

    return [
        _check_frequency(bpfo_hz, bpfo_expected, "BPFO_Hz", rtol=rtol, atol=atol),
        _check_frequency(bpfi_hz, bpfi_expected, "BPFI_Hz", rtol=rtol, atol=atol),
        _check_frequency(ftf_hz, ftf_expected, "FTF_Hz", rtol=rtol, atol=atol),
        _check_frequency(bsf_hz, bsf_expected, "BSF_Hz", rtol=rtol, atol=atol),
    ]


def check_envelope_function(envelope_func, rtol=1e-4, atol=1e-8):
    """Return feedback message for the student envelope function implementation."""
    fs = 12_000.0
    duration = 0.3
    t = np.arange(0, duration, 1 / fs)

    # Deterministic mixed signal with modulation and noise-like component
    x = (
        0.8 * np.sin(2 * np.pi * 120 * t)
        + 0.4 * np.sin(2 * np.pi * 740 * t)
        + 0.2 * np.sin(2 * np.pi * 50 * t) * np.sin(2 * np.pi * 1500 * t)
        + 0.05 * np.cos(2 * np.pi * 37 * t)
    )

    try:
        result = envelope_func(x, fs)
    except Exception as exc:
        return f"❌ envelope() raised an error: {exc}"

    if not isinstance(result, tuple) or len(result) != 2:
        return "❌ envelope() must return two values: frequency vector and spectrum."

    f_student, X_student = result

    try:
        f_student = np.asarray(f_student)
        X_student = np.asarray(X_student)
    except Exception:
        return "❌ envelope() output must be array-like values."

    if f_student.ndim != 1 or X_student.ndim != 1:
        return "❌ envelope() outputs must be 1D arrays."

    if f_student.shape != X_student.shape:
        return "❌ Frequency vector and spectrum must have the same shape."

    if f_student.size != len(x) // 2:
        return "❌ Output length is incorrect. Check one-sided FFT slicing and scaling."

    if not np.all(np.isfinite(X_student)):
        return "❌ Spectrum contains non-finite values."

    # Reference implementation
    analytic_signal = _analytic_signal_fft(x)
    env = np.abs(analytic_signal)
    squared_env = env ** 2
    X_ref = np.fft.fft(squared_env)
    N = len(x)
    X_ref = np.abs(X_ref[: N // 2]) * (2 / N)
    f_ref = np.linspace(0, fs / 2, N // 2)

    if not np.allclose(f_student, f_ref, rtol=rtol, atol=atol):
        return "❌ Frequency vector is incorrect. Check how f is computed."

    if not np.allclose(X_student, X_ref, rtol=5e-3, atol=1e-8):
        return "❌ Envelope spectrum is not correct yet. Re-check Hilbert, squaring, and FFT steps."

    return "✅ envelope() looks correct."
