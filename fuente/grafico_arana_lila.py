"""Gráfico de araña de la VGI – estilo minimalista lila (grilla poligonal, sin título ni leyenda).
Cada escala en % de desempeño: 100% = mejor resultado; escalas inversas como (máx − puntaje)/máx."""
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = [("MNA-SF", 11, 14, False), ("Pfeiffer", 0, 10, True), ("MMSE", 27, 30, False), ("MoCA", 25, 30, False),
     ("T@M", 47, 50, False), ("PHQ-9", 11, 27, True), ("Hamilton", 9, 52, True), ("Barthel", 100, 100, False),
     ("FRAIL", 1, 5, True), ("SARC-F", 0, 10, True), ("SPPB", 10, 12, False), ("Tinetti", 27, 28, False),
     ("Downton", 3, 11, True), ("Escala social UC", 0, 5, True)]
LINE, FILL, GRID, INK = "#8e6cc9", "#cdbdf0", "#cfcfcf", "#333333"

v = np.array([(m - p) / m if inv else p / m for _, p, m, inv in D])
n = len(D)
ang = np.pi / 2 - 2 * np.pi * np.arange(n) / n          # empieza arriba, sentido horario
ux, uy = np.cos(ang), np.sin(ang)
close = lambda a: np.r_[a, a[:1]]

plt.rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
fig, ax = plt.subplots(figsize=(7, 7), dpi=300)
ax.set_aspect("equal"); ax.axis("off")
for r in (0.2, 0.4, 0.6, 0.8, 1.0):                      # anillos poligonales
    ax.plot(close(r * ux), close(r * uy), color=GRID, lw=0.8, zorder=1)
for x, y in zip(ux, uy):                                  # radios
    ax.plot([0, x], [0, y], color=GRID, lw=0.8, zorder=1)
ax.fill(close(v * ux), close(v * uy), color=FILL, alpha=0.7, lw=0, zorder=2)
ax.plot(close(v * ux), close(v * uy), color=LINE, lw=1.6, zorder=3)
ax.scatter(v * ux, v * uy, s=16, color=LINE, zorder=4)
for (name, *_), x, y in zip(D, ux, uy):
    ha = "center" if abs(x) < 0.15 else ("left" if x > 0 else "right")
    va = "center" if abs(y) < 0.9 else ("bottom" if y > 0 else "top")
    ax.text(1.12 * x, 1.12 * y, name, ha=ha, va=va, fontsize=11, color=INK)
ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.25, 1.25)
fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "grafico_arana_lila.png", dpi=300,
            facecolor="white", bbox_inches="tight", pad_inches=0.15)
