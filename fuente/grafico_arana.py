"""Gráfico de araña (radar) de la VGI – % de desempeño por escala (100% = mejor resultado)."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

# (escala, puntaje, máximo, invertida?, umbral de normalidad expresado en % de desempeño, esfera)
# Invertida = a mayor puntaje, peor resultado -> % = (máx - puntaje)/máx
D = [
    ("MNA-SF",        11, 14, False, 12/14,        "Nutricional"),
    ("Pfeiffer",       0, 10, True,  (10-2)/10,    "Cognitiva"),
    ("MMSE",          27, 30, False, 27/30,        "Cognitiva"),
    ("MoCA",          25, 30, False, 26/30,        "Cognitiva"),
    ("TAM",           47, 50, False, 44/50,        "Cognitiva"),
    ("PHQ-9",         11, 27, True,  (27-9)/27,    "Afectiva"),
    ("Hamilton",       9, 52, True,  (52-7)/52,    "Afectiva"),
    ("Barthel",      100,100, False, 100/100,      "Funcional"),
    ("FRAIL",          1,  5, True,  (5-0)/5,      "Funcional"),
    ("SARC-F",         0, 10, True,  (10-3)/10,    "Funcional"),
    ("SPPB",          10, 12, False, 10/12,        "Funcional"),
    ("Tinetti",       27, 28, False, 25/28,        "Funcional"),
    ("Downton",        3, 11, True,  (11-2)/11,    "Funcional"),
    ("Escala social UC", 0, 5, True, (5-0)/5,      "Social"),
]
ESF = {"Nutricional": "#eda100", "Cognitiva": "#2a78d6", "Afectiva": "#e87ba4",
       "Funcional": "#1baf7a", "Social": "#4a3aa7"}
INK, INK2, PAT, THR, ALT = "#0b0b0b", "#52514e", "#2a78d6", "#52514e", "#e34948"

def pct(p, m, inv): return 100*((m-p)/m if inv else p/m)
vals = np.array([pct(p, m, i) for _, p, m, i, _, _ in D])
thr = np.array([100*t for *_, t, _ in D])
n = len(D); ang = np.linspace(0, 2*np.pi, n, endpoint=False)
A = np.r_[ang, ang[0]]

plt.rcParams["font.family"] = "DejaVu Sans"
fig = plt.figure(figsize=(10, 10.4), dpi=300)
ax = fig.add_axes([0.19, 0.20, 0.62, 0.62], polar=True)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.set_ylim(0, 100)

# bandas de esfera (fondo muy tenue)
w = 2*np.pi/n
for a, (_, *_r, esf) in zip(ang, D):
    ax.bar(a, 100, width=w, color=ESF[esf], alpha=0.10, edgecolor="none", zorder=0)

ax.set_yticks([20, 40, 60, 80, 100]); ax.set_yticklabels(["20", "40", "60", "80", "100%"], color=INK2, fontsize=7.5)
ax.set_rlabel_position(360/n/2)
ax.yaxis.grid(True, color="#d6d5d0", lw=0.6); ax.xaxis.grid(True, color="#d6d5d0", lw=0.6)
ax.spines["polar"].set_color("#bdbcb6"); ax.spines["polar"].set_linewidth(0.8)

ax.plot(A, np.r_[thr, thr[0]], ls=(0, (4, 3)), lw=1.4, color=THR, zorder=3)
ax.fill(A, np.r_[vals, vals[0]], color=PAT, alpha=0.10, zorder=2)
ax.plot(A, np.r_[vals, vals[0]], lw=2, color=PAT, zorder=4)
bajo = vals < thr - 1e-9
ax.scatter(ang[~bajo], vals[~bajo], s=34, color=PAT, edgecolor="white", lw=1.2, zorder=5)
ax.scatter(ang[bajo], vals[bajo], s=62, marker="D", color=ALT, edgecolor="white", lw=1.2, zorder=6)

ax.set_xticks(ang); ax.set_xticklabels([])
for a, (name, p, m, inv, t, esf), v in zip(ang, D, vals):
    ha = "center" if abs(np.sin(a)) < 0.2 else ("left" if np.sin(a) > 0 else "right")
    ax.text(a, 113, f"{name}\n{p}/{m}  ·  {v:.0f}%", ha=ha, va="center", fontsize=9,
            color=INK, fontweight="bold" if bajo[list(ang).index(a)] else "normal", linespacing=1.3)

fig.text(0.5, 0.955, "Gráfico de araña – Valoración Geriátrica Integral", ha="center",
         fontsize=15, fontweight="bold", color=INK)
fig.text(0.5, 0.928, "Residente M.T.L., 85 años · Hogar Italiano · Septiembre 2026", ha="center",
         fontsize=10, color=INK2)
h = [Line2D([], [], color=PAT, lw=2, marker="o", mfc=PAT, mec="white", label="Desempeño del paciente"),
     Line2D([], [], color=THR, lw=1.4, ls=(0, (4, 3)), label="Umbral de normalidad"),
     Line2D([], [], color="none", marker="D", mfc=ALT, mec="white", ms=8, label="Bajo el umbral (alterado)")]
h2 = [Patch(color=c, alpha=0.35, label=f"Esfera {k.lower()}") for k, c in ESF.items()]
fig.legend(handles=h, loc="lower center", bbox_to_anchor=(0.5, 0.075), ncol=3, frameon=False, fontsize=9)
fig.legend(handles=h2, loc="lower center", bbox_to_anchor=(0.5, 0.042), ncol=5, frameon=False, fontsize=8.5)
fig.text(0.5, 0.012, "100% = mejor resultado posible. Escalas en que un mayor puntaje indica peor resultado "
         "\n(Pfeiffer, PHQ-9, Hamilton, FRAIL, SARC-F, Downton, Escala social UC) se invirtieron: (máx − puntaje)/máx.",
         ha="center", fontsize=7.5, color=INK2)
import sys
out = sys.argv[1] if len(sys.argv) > 1 else "grafico_arana.png"
fig.savefig(out, dpi=300, facecolor="white")
print(list(zip([d[0] for d in D], vals.round(1), thr.round(1))))
