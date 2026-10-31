"""
Figure for the "Teorema de Existência e Unicidade de Picard" section:
a solution curve y(t) inside the rectangle

    R = [alpha, beta] x [gamma, delta],

where beta = t0 + a, gamma = y0 - b2 and delta = y0 + b1.

The curve starts at (t0, y0) and ends at t = t0 + theta.
Run the script to save the figure as ``fig/picard_rectangle.pdf``.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT = Path(__file__).resolve().parent.parent / "fig" / "picard_rectangle.pdf"

# --- Geometry (arbitrary units; only the shape matters) ----------------------
ALPHA, BETA = 1.2, 9.4     # horizontal sides of R (wider than tall)
GAMMA, DELTA = 1.0, 5.0    # vertical sides of R

T0, Y0 = 2.1, 2.8          # first point of the curve (lower left of R)
T_END = 7.6                # t0 + theta (here theta = b / M < a)
Y_END = 3.8

T_MAX, Y_MAX = 10.6, 6.2   # extent of the drawn axes

# For the figure to agree with the theorem, the curve must satisfy
# |y(t) - y0| <= M (t - t0) <= b on [t0, t0 + theta], with M = b / theta.
B = min(DELTA - Y0, Y0 - GAMMA)
M = B / (T_END - T0)

# --- Style -------------------------------------------------------------------
RECT_COLOR = "#2b6cb0"
CURVE_COLOR = "#c0392b"
GUIDE_STYLE = dict(color="0.55", linestyle=(0, (4, 3)), linewidth=0.9, zorder=1)

plt.rcParams.update({
    "font.size": 13,
    "mathtext.fontset": "cm",   # Computer Modern, matches LaTeX notes
    "font.family": "serif",
})


def curve(t):
    """A smooth increasing curve from (T0, Y0) to (T_END, Y_END) with a slight wiggle."""
    s = (t - T0) / (T_END - T0)                      # s in [0, 1]
    smooth = 3 * s**2 - 2 * s**3                      # smoothstep
    wiggle = 0.12 * np.sin(2 * np.pi * s) * s * (1 - s) * 4
    return Y0 + (Y_END - Y0) * smooth + wiggle


def draw_axes(ax):
    """Draw first-quadrant axes as arrows through the origin."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_position("zero")
        ax.spines[side].set_linewidth(1.1)

    # Arrow heads at the end of each axis
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, ms=6)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, ms=6)

    ax.set_xlim(0, T_MAX)
    ax.set_ylim(0, Y_MAX)
    ax.set_xlabel("$t$", loc="right", fontsize=16)
    ax.set_ylabel("$y$", loc="top", rotation=0, fontsize=16)
    ax.xaxis.set_label_coords(1.0, -0.02)
    ax.yaxis.set_label_coords(-0.01, 1.02)


def main():
    fig, ax = plt.subplots(figsize=(9, 5.4), layout="constrained")
    draw_axes(ax)

    # Rectangle R
    rect = plt.Rectangle(
        (ALPHA, GAMMA), BETA - ALPHA, DELTA - GAMMA,
        facecolor=RECT_COLOR, alpha=0.08, edgecolor="none", zorder=0,
    )
    ax.add_patch(rect)
    ax.add_patch(plt.Rectangle(
        (ALPHA, GAMMA), BETA - ALPHA, DELTA - GAMMA,
        fill=False, edgecolor=RECT_COLOR, linewidth=1.6, zorder=2,
    ))
    ax.text(BETA - 0.25, DELTA - 0.25, "$R$", color=RECT_COLOR,
            fontsize=20, ha="right", va="top")

    # Curve y(t)
    t = np.linspace(T0, T_END, 400)
    y = curve(t)
    assert np.all(np.abs(y - Y0) <= M * (t - T0) + 1e-9), "curve leaves the cone"
    ax.plot(t, y, color=CURVE_COLOR, linewidth=2.2, zorder=3)
    ax.plot([T0, T_END], [Y0, y[-1]], "o", color=CURVE_COLOR, ms=5, zorder=4)
    ax.text(t[300] - 0.1, y[300] + 0.25, "$y(t)$", color=CURVE_COLOR,
            fontsize=17, ha="right", va="bottom")

    # Dashed guides from the marked points to the axes
    ax.plot([ALPHA, ALPHA], [0, GAMMA], **GUIDE_STYLE)
    ax.plot([BETA, BETA], [0, GAMMA], **GUIDE_STYLE)
    ax.plot([0, ALPHA], [GAMMA, GAMMA], **GUIDE_STYLE)
    ax.plot([0, ALPHA], [DELTA, DELTA], **GUIDE_STYLE)
    ax.plot([T0, T0], [0, Y0], **GUIDE_STYLE)
    ax.plot([0, T0], [Y0, Y0], **GUIDE_STYLE)
    ax.plot([T_END, T_END], [0, y[-1]], **GUIDE_STYLE)

    # Coordinates on the axes
    ax.set_xticks(
        [ALPHA, T0, T_END, BETA],
        [r"$\alpha$", "$t_0$", r"$t_0 + \theta$", r"$\beta = t_0 + a$"],
    )
    ax.set_yticks(
        [GAMMA, Y0, DELTA],
        [r"$\gamma = y_0 - b_2$", "$y_0$", r"$\delta = y_0 + b_1$"],
    )
    ax.tick_params(length=4, width=1, labelsize=14)

    OUTPUT.parent.mkdir(exist_ok=True)
    # No creation date, so re-running the script without changes gives an identical file
    fig.savefig(OUTPUT, metadata={"CreationDate": None})


if __name__ == "__main__":
    main()
