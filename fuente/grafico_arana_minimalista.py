"""Gráfico de araña de la VGI – versión minimalista (100% = mejor resultado)."""
import sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# (escala, puntaje, máximo, invertida?, umbral de normalidad como fracción de desempeño)
D = [("MNA-SF", 11, 14, False, 12/14), ("Pfeiffer", 0, 10, True, 8/10), ("MMSE", 27, 30, False, 27/30),
     ("MoCA", 25, 30, False, 26/30), ("T@M", 47, 50, False, 44/50), ("PHQ-9", 11, 27, True, 18/27),
     ("Hamilton", 9, 52, True, 45/52), ("Barthel", 100, 100, False, 1.0), ("FRAIL", 1, 5, True, 1.0),
     ("SARC-F", 0, 10, True, 7/10), ("SPPB", 10, 12, False, 10/12), ("Tinetti", 27, 28, False, 25/28),
     ("Downton", 3, 11, True, 9/11), ("Escala social UC", 0, 5, True, 1.0)]

INK, MUTED, GRID, BLUE, RED = "#222222", "#8a8a8a", "#e6e6e6", "#2a78d6", "#e34948"
v = np.array([100 * ((m - p) / m if inv else p / m) for _, p, m, inv, _ in D])
u = np.array([100 * t for *_, t in D])
n = len(D); a = np.linspace(0, 2 * np.pi, n, endpoint=False); A = np.r_[a, a[0]]
low = v < u - 1e-9

plt.rcParams["font.family"] = ["Carlito", "DejaVu Sans"]
fig = plt.figure(figsize=(8, 8.2), dpi=300)
ax = fig.add_axes([0.16, 0.12, 0.68, 0.70], polar=True)
ax.set_theta_offset(np.pi / 2); ax.set_theta_direction(-1)
ax.set_ylim(0, 100)
ax.set_yticks([25, 50, 75, 100]); ax.set_yticklabels([])
ax.set_xticks(a); ax.set_xticklabels([])
ax.grid(color=GRID, lw=0.7); ax.spines["polar"].set_visible(False)

ax.plot(A, np.r_[u, u[0]], color=MUTED, lw=0.9, ls=(0, (3, 3)))
ax.fill(A, np.r_[v, v[0]], color=BLUE, alpha=0.08, lw=0)
ax.plot(A, np.r_[v, v[0]], color=BLUE, lw=1.8)
ax.scatter(a[~low], v[~low], s=18, color=BLUE, zorder=3)
ax.scatter(a[low], v[low], s=26, color=RED, zorder=4)

for ang, (name, p, m, *_), val, bad in zip(a, D, v, low):
    s = np.sin(ang)
    ha = "center" if abs(s) < 0.2 else ("left" if s > 0 else "right")
    ax.text(ang, 114, name, ha=ha, va="bottom", fontsize=10.5, color=INK)
    ax.text(ang, 114, f"{p}/{m}", ha=ha, va="top", fontsize=9.5, color=RED if bad else MUTED)

fig.text(0.5, 0.94, "Gráfico de araña · Valoración Geriátrica Integral", ha="center", fontsize=15, color=INK)
fig.text(0.5, 0.912, "Desempeño por escala (100% = mejor resultado)", ha="center", fontsize=10.5, color=MUTED)
h = [Line2D([], [], color=BLUE, lw=1.8, label="Paciente"),
     Line2D([], [], color=MUTED, lw=0.9, ls=(0, (3, 3)), label="Umbral de normalidad"),
     Line2D([], [], color="none", marker="o", mfc=RED, mec=RED, ms=5, label="Bajo el umbral")]
fig.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, 0.03), ncol=3, frameon=False,
           fontsize=10, labelcolor=INK, handlelength=2.2, columnspacing=2.2)
fig.savefig(sys.argv[1] if len(sys.argv) > 1 else "grafico_arana_minimalista.png", dpi=300, facecolor="white")
