"""
Plot the empirical distribution derived using the Gaussian KDE with
margin data downloaded from Prof. Damodaran's website at NYU.

"""

import warnings
from pathlib import Path

import numpy as np
from matplotlib.ticker import StrMethodFormatter
from numpy.random import PCG64DXSM, Generator, SeedSequence
from scipy import stats  # type: ignore

import mergeron.core.empirical_margin_distribution as emd
from mergeron import WORK_DIR as PKG_WORK_DIR
from mergeron.core.guidelines_boundary_functions import boundary_plot

WORK_DIR = globals().get("WORK_DIR", PKG_WORK_DIR)
"""Redefined, in case the user defines WORK_DIR betweeen module imports."""

SAMPLE_SIZE = 10**6
BIN_COUNT = 25
margin_data, margin_data_stats = emd.margin_data_builder()

margin_data_obs, margin_data_wts = margin_data[:, 0], margin_data[:, 1]

print(repr(margin_data_obs))
print(repr(margin_data_stats))

plt, mgn_fig, mgn_ax, set_axis_def = boundary_plot(mktshare_plot_flag=False)
mgn_fig.set_figheight(6.5)
mgn_fig.set_figwidth(9.0)

_, mgn_bins, _ = mgn_ax.hist(
    x=margin_data_obs,
    weights=margin_data_wts,
    bins=BIN_COUNT,
    alpha=0.4,
    density=True,
    label="Downloaded data",
    color="#004488",  # Paul Tol's High Contrast Blue
)

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    # Don't warn regarding the below; ticklabels have been fixed before this point
    mgn_ax.set_yticklabels([
        f"{float(_g.get_text()) * np.diff(mgn_bins)[-1]:.0%}"
        for _g in mgn_ax.get_yticklabels()
    ])

mgn_kde = stats.gaussian_kde(
    margin_data_obs, weights=margin_data_wts, bw_method="silverman"
)
mgn_kde.set_bandwidth(bw_method=mgn_kde.factor / 3.0)

mgn_ax.plot(
    (_xv := np.linspace(0, BIN_COUNT, 10**5) / BIN_COUNT),
    mgn_kde(_xv),
    color="#004488",
    rasterized=True,
    label="Estimated Density",
)

mgn_ax.hist(
    x=mgn_kde.resample(
        SAMPLE_SIZE, seed=Generator(PCG64DXSM(SeedSequence(pool_size=8)))
    )[0],
    color="#DDAA33",  # Paul Tol's High Contrast Yellow
    alpha=0.6,
    bins=BIN_COUNT,
    density=True,
    label="Generated data",
)

mgn_ax.legend(
    loc="best",
    fancybox=False,
    shadow=False,
    frameon=True,
    facecolor="white",
    edgecolor="white",
    framealpha=1,
    fontsize="small",
)

mgn_ax.set_xlim(0.0, 1.0)
mgn_ax.xaxis.set_major_formatter(StrMethodFormatter("{x:>3.0%}"))
mgn_ax.set_xlabel("Price Cost Margin", fontsize=10)
mgn_ax.set_ylabel("Relative Frequency", fontsize=10)

mgn_fig.tight_layout()
plt.savefig(WORK_DIR / f"{Path(__file__).stem}.pdf")
