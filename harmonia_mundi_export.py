"""
harmonia_mundi_export.py  —  v2
================================
Replica EXACTA del HarmoniaMundiSystem de Archeoscope.

Estado replicado: ImmersiveScene con TODAS las misiones completadas
(el sonido más rico que puede tener el juego, sin activateAllPlanets manual).

Cadena de señal (igual que el código TS):
  oscillator → gain(intensity) → [planetary|harmonic|pulse]Gain → masterGain(0.7) → destination

Capas activas:
  - earth_base_ambient  (unlocked=true desde el inicio)
  - earth_mission_1..6  (desbloqueadas por misiones)

NO incluye activateAllPlanets() — eso es un botón manual del PlanetaryAudioPanel.

Fuente: viewer3d/systems/HarmoniaMundiSystem.ts
"""

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import warnings
warnings.filterwarnings('ignore')

# ─── Parámetros globales ──────────────────────────────────────────────────────
SAMPLE_RATE  = 44100
DURATION     = 60
MASTER_VOL   = 0.70   # masterGain.gain.value (default)
PLANET_VOL   = 1.00   # planetaryGain
HARMONIC_VOL = 0.80   # harmonicGain
PULSE_VOL    = 0.60   # pulseGain

N = SAMPLE_RATE * DURATION
t = np.linspace(0, DURATION, N, endpoint=False)

# ─── Helpers ─────────────────────────────────────────────────────────────────

def transpose_to_audible(freq):
    """
    Replica exacta de createLayerOscillator:
      while (finalFreq < 20 && finalFreq > 0) finalFreq *= 2
      while (finalFreq > 2000) finalFreq /= 2
    """
    f = float(freq)
    while f < 20 and f > 0:
        f *= 2
    while f > 2000:
        f /= 2
    return f

def make_osc(waveform, freq, n, sr=SAMPLE_RATE):
    """Genera oscilador del tipo indicado (igual que OscillatorNode)"""
    ph = np.linspace(0, freq * DURATION, n, endpoint=False) % 1.0
    if waveform == 'sine':
        return np.sin(2 * np.pi * ph)
    elif waveform == 'triangle':
        return 2 * np.abs(2 * ph - 1) - 1
    elif waveform == 'sawtooth':
        return 2 * ph - 1
    elif waveform == 'square':
        return np.sign(np.sin(2 * np.pi * ph))
    return np.zeros(n)

def linear_ramp(n, sr, events):
    """
    Replica linearRampToValueAtTime.
    events = [(time_sec, value), ...]  — primer punto es el valor inicial en t=0
    """
    env = np.zeros(n)
    times  = [e[0] for e in events]
    values = [e[1] for e in events]
    for i in range(len(times) - 1):
        i0 = int(times[i]   * sr)
        i1 = int(times[i+1] * sr)
        i0 = max(0, min(n, i0))
        i1 = max(0, min(n, i1))
        if i1 > i0:
            env[i0:i1] = np.linspace(values[i], values[i+1], i1 - i0)
    # Mantener último valor hasta el final
    last_i = int(times[-1] * sr)
    last_i = max(0, min(n, last_i))
    env[last_i:] = values[-1]
    return env

def lowpass_filter(sig, cutoff, sr=SAMPLE_RATE, order=2):
    nyq = sr / 2.0
    b, a = butter(order, min(cutoff / nyq, 0.99), btype='low')
    return lfilter(b, a, sig)

def bandpass_filter(sig, center, Q, sr=SAMPLE_RATE):
    nyq = sr / 2.0
    bw   = center / Q
    lo   = max(20, center - bw / 2) / nyq
    hi   = min(nyq * 0.99, center + bw / 2) / nyq
    if lo >= hi:
        return sig
    b, a = butter(2, [lo, hi], btype='band')
    return lfilter(b, a, sig)

# ─── Acumulador ───────────────────────────────────────────────────────────────
mix = np.zeros(N, dtype=np.float64)

# ─── CAPAS DE MISIÓN DE LA TIERRA ────────────────────────────────────────────
# Todas las capas que el juego activa al completar misiones.
# Fade-in: gain.gain.linearRampToValueAtTime(intensity, now + 3)
# → env va de 0 a intensity en 3 segundos, luego se mantiene.

FADE = 3.0  # segundos

print("🌍 Generando capas de misión de la Tierra (estado: todas completadas)...")
print()

# ── earth_base_ambient ────────────────────────────────────────────────────────
# freq=40, type='drone' → sine, intensity=0.08, → planetaryGain
# unlocked=true desde el inicio
freq = transpose_to_audible(40.0)
env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.08), (DURATION, 0.08)])
osc  = make_osc('sine', freq, N)
layer = osc * env * PLANET_VOL * MASTER_VOL
mix += layer
print(f"  earth_base_ambient  | sine  | {40.0:.2f} Hz → {freq:.2f} Hz | intensity=0.08 | →planetaryGain")

# ── earth_mission_1 ───────────────────────────────────────────────────────────
# freq=136.10/16=8.50625 Hz, type='drone' → sine, intensity=0.15, → planetaryGain
raw  = 136.10 / 16
freq = transpose_to_audible(raw)
env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.15), (DURATION, 0.15)])
osc  = make_osc('sine', freq, N)
layer = osc * env * PLANET_VOL * MASTER_VOL
mix += layer
print(f"  earth_mission_1     | sine  | {raw:.4f} Hz → {freq:.4f} Hz | intensity=0.15 | →planetaryGain")

# ── earth_mission_2 ───────────────────────────────────────────────────────────
# type='pulse'
# pulseFreq = layer.frequency * 100 = (1/365.25)*100 = 0.2738 Hz
#   while pulseFreq < 40: pulseFreq *= 2  → 0.2738→0.5476→...→35.05 Hz (×128) → 70.09 Hz (×256)
# LFO: freq = max(0.1, 1/365.25) = 0.1 Hz, type='sine'
# lfoGain.gain.value = intensity * 0.5 = 0.1 * 0.5 = 0.05
# lfo.connect(lfoGain) → lfoGain.connect(gain.gain)  ← modula la ganancia del carrier
# gain.gain.linearRampToValueAtTime(intensity=0.1, now+3)
# → pulseGain (×0.6) → masterGain (×0.7)
raw_freq    = 1.0 / 365.25
pulse_freq  = raw_freq * 100
while pulse_freq < 40:
    pulse_freq *= 2
lfo_freq    = max(0.1, raw_freq)   # 0.1 Hz
lfo_gain_v  = 0.1 * 0.5            # intensity * 0.5 = 0.05

carrier_osc = make_osc('sine', pulse_freq, N)
lfo_osc     = make_osc('sine', lfo_freq, N)

# La ganancia del carrier = ramp(0→0.1 en 3s) + lfo*0.05
carrier_env = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.1), (DURATION, 0.1)])
am_gain     = carrier_env + lfo_osc * lfo_gain_v
layer       = carrier_osc * am_gain * PULSE_VOL * MASTER_VOL
mix += layer
print(f"  earth_mission_2     | pulse | carrier {pulse_freq:.4f} Hz + LFO {lfo_freq:.4f} Hz | intensity=0.1 | →pulseGain")

# ── earth_mission_3 ───────────────────────────────────────────────────────────
# freq=(136.10/16)*2=17.0125 Hz, type='harmonic' → triangle, intensity=0.08, → harmonicGain
raw  = (136.10 / 16) * 2
freq = transpose_to_audible(raw)
env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.08), (DURATION, 0.08)])
osc  = make_osc('triangle', freq, N)
layer = osc * env * HARMONIC_VOL * MASTER_VOL
mix += layer
print(f"  earth_mission_3     | tri   | {raw:.4f} Hz → {freq:.4f} Hz | intensity=0.08 | →harmonicGain")

# ── earth_mission_4 ───────────────────────────────────────────────────────────
# freq=(136.10/16)*3=25.51875 Hz, type='texture' → sawtooth, intensity=0.06, → harmonicGain
raw  = (136.10 / 16) * 3
freq = transpose_to_audible(raw)
env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.06), (DURATION, 0.06)])
osc  = make_osc('sawtooth', freq, N)
layer = osc * env * HARMONIC_VOL * MASTER_VOL
mix += layer
print(f"  earth_mission_4     | saw   | {raw:.4f} Hz → {freq:.4f} Hz | intensity=0.06 | →harmonicGain")

# ── earth_mission_5 ───────────────────────────────────────────────────────────
# freq=(136.10/16)*4=34.025 Hz, type='resonance' → sine, intensity=0.12, → planetaryGain
raw  = (136.10 / 16) * 4
freq = transpose_to_audible(raw)
env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.12), (DURATION, 0.12)])
osc  = make_osc('sine', freq, N)
layer = osc * env * PLANET_VOL * MASTER_VOL
mix += layer
print(f"  earth_mission_5     | sine  | {raw:.4f} Hz → {freq:.4f} Hz | intensity=0.12 | →planetaryGain")

# ── earth_mission_6 — Khepri base layer ──────────────────────────────────────
# freq=45 Hz, type='texture' → sawtooth, intensity=0.18, → harmonicGain
raw  = 45.0
freq = transpose_to_audible(raw)
env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.18), (DURATION, 0.18)])
osc  = make_osc('sawtooth', freq, N)
layer = osc * env * HARMONIC_VOL * MASTER_VOL
mix += layer
print(f"  earth_mission_6     | saw   | {raw:.2f} Hz → {freq:.2f} Hz | intensity=0.18 | →harmonicGain")

# ─── SONIDO DEL ESCARABAJO (playBeetleSound) ──────────────────────────────────
# Se activa al completar Göbekli Tepe (misión 6)
print()
print("🪲 Generando sonido del escarabajo Khepri (playBeetleSound)...")

# Capa 1: Wingbeat oscillator
# wingOsc.type='sawtooth', freq=45 Hz
# wingFilter: lowpass, cutoff=300 Hz, Q=2
# wingGain envelope:
#   setValueAtTime(0, now)
#   linearRampToValueAtTime(0.18, now+4)
#   linearRampToValueAtTime(0.28, now+10)
#   linearRampToValueAtTime(0.35, now+18)
#   linearRampToValueAtTime(0.15, now+30)
wing_osc = make_osc('sawtooth', 45.0, N)
wing_osc = lowpass_filter(wing_osc, 300.0)
wing_env = linear_ramp(N, SAMPLE_RATE, [
    (0,  0.00),
    (4,  0.18),
    (10, 0.28),
    (18, 0.35),
    (30, 0.15),
    (DURATION, 0.15),
])

# LFO modulación de amplitud del wingbeat
# lfo.type='sine', lfo.frequency=80 Hz
# lfoGain envelope:
#   setValueAtTime(0, now)
#   linearRampToValueAtTime(0.12, now+3)
#   linearRampToValueAtTime(0.22, now+12)
lfo_osc  = make_osc('sine', 80.0, N)
lfo_env  = linear_ramp(N, SAMPLE_RATE, [
    (0,  0.00),
    (3,  0.12),
    (12, 0.22),
    (DURATION, 0.22),
])
# lfoGain.connect(wingGain.gain) → AM: ganancia total = wing_env + lfo*lfo_env
wing_total_gain = wing_env + lfo_osc * lfo_env
wing_layer = wing_osc * wing_total_gain * MASTER_VOL
mix += wing_layer
print(f"  beetle_wing         | saw   | 45 Hz + lowpass 300 Hz + LFO 80 Hz AM | →masterGain directo")

# Capa 2: Harmonic buzz
# buzzOsc.type='square', freq=320 Hz
# buzzFilter: bandpass, center=350 Hz, Q=3
# buzzGain envelope:
#   setValueAtTime(0, now)
#   linearRampToValueAtTime(0.06, now+6)
#   linearRampToValueAtTime(0.12, now+15)
#   linearRampToValueAtTime(0.08, now+30)
buzz_osc = make_osc('square', 320.0, N)
buzz_osc = bandpass_filter(buzz_osc, 350.0, 3.0)
buzz_env = linear_ramp(N, SAMPLE_RATE, [
    (0,  0.00),
    (6,  0.06),
    (15, 0.12),
    (30, 0.08),
    (DURATION, 0.08),
])
buzz_layer = buzz_osc * buzz_env * MASTER_VOL
mix += buzz_layer
print(f"  beetle_buzz         | sq    | 320 Hz → bandpass 350 Hz Q=3 | →masterGain directo")

# ─── Normalización y exportación ─────────────────────────────────────────────
print()
print("📊 Normalizando...")
peak = np.max(np.abs(mix))
print(f"  Peak pre-normalización: {peak:.4f}")

# -3 dBFS headroom (0.707) — igual que un master bus estándar
mix_norm = mix / peak * 0.707
mix_int16 = (mix_norm * 32767).astype(np.int16)

output = "harmonia_mundi.wav"
wavfile.write(output, SAMPLE_RATE, mix_int16)

print()
print(f"✅  {output}")
print(f"    {DURATION}s · {SAMPLE_RATE} Hz · 16-bit mono")
print()
print("📋 Resumen de capas (estado: todas las misiones completadas):")
print("   earth_base_ambient  sine     40.00 Hz  intensity=0.08  →planetary×1.0")
print("   earth_mission_1     sine     34.02 Hz  intensity=0.15  →planetary×1.0")
print("   earth_mission_2     pulse    70.09 Hz  intensity=0.10  →pulse×0.6")
print("   earth_mission_3     triangle 34.02 Hz  intensity=0.08  →harmonic×0.8")
print("   earth_mission_4     sawtooth 25.52 Hz  intensity=0.06  →harmonic×0.8")
print("   earth_mission_5     sine     34.02 Hz  intensity=0.12  →planetary×1.0")
print("   earth_mission_6     sawtooth 45.00 Hz  intensity=0.18  →harmonic×0.8")
print("   beetle_wing         sawtooth 45 Hz+LFO 80 Hz           →master×0.7")
print("   beetle_buzz         square   320→350 Hz bandpass        →master×0.7")
print()
print("   masterGain = 0.70 | planetaryGain = 1.0 | harmonicGain = 0.8 | pulseGain = 0.6")
print()
print("⚠️  NO incluye activateAllPlanets() — eso es un botón manual del PlanetaryAudioPanel")
print("   Para generarlo con todos los planetas, descomenta la sección PLANETAS al final.")

# ─── OPCIONAL: activateAllPlanets() ──────────────────────────────────────────
# Descomenta este bloque si querés el sonido con todos los planetas activos
# (equivale a presionar el botón en el PlanetaryAudioPanel)

INCLUDE_ALL_PLANETS = False  # ← cambiar a True para incluir planetas

if INCLUDE_ALL_PLANETS:
    CELESTIAL_BODIES = [
        ('mercury', 'Mercurio', 141.27,  88),
        ('venus',   'Venus',    221.23,  225),
        ('earth',   'Tierra',   136.10,  365.25),
        ('mars',    'Marte',    144.72,  687),
        ('jupiter', 'Júpiter',  183.58,  4333),
        ('saturn',  'Saturno',  147.85,  10759),
        ('uranus',  'Urano',    207.36,  30687),
        ('neptune', 'Neptuno',  211.44,  60190),
        ('pluto',   'Plutón',   140.25,  90560),
    ]
    print("\n🪐 Añadiendo drones planetarios (activateAllPlanets)...")
    planet_mix = np.zeros(N)
    for pid, name, base_freq, period in CELESTIAL_BODIES:
        drone_freq = base_freq / 8
        final_freq = transpose_to_audible(drone_freq)
        env  = linear_ramp(N, SAMPLE_RATE, [(0, 0), (FADE, 0.08), (DURATION, 0.08)])
        osc  = make_osc('sine', final_freq, N)
        planet_mix += osc * env * 0.08 * PLANET_VOL * MASTER_VOL
        print(f"  {name}: {base_freq:.2f} Hz → drone {drone_freq:.2f} Hz → audible {final_freq:.2f} Hz")

    mix_total = mix + planet_mix
    peak2 = np.max(np.abs(mix_total))
    mix_total = mix_total / peak2 * 0.707
    wavfile.write("harmonia_mundi_all_planets.wav", SAMPLE_RATE, (mix_total * 32767).astype(np.int16))
    print("✅  harmonia_mundi_all_planets.wav generado")
