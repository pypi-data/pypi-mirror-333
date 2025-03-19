"""
Functions to parse margin data compiled by
Prof. Aswath Damodaran, Stern School of Business, NYU.

Provides :func:`margin_data_resampler` for generating margin data
from an estimated Gaussian KDE from the source (margin) data.

Data are downloaded or reused from a local copy, on demand.

For terms of use of Prof. Damodaran's data, please see:
https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datahistory.html

NOTES
-----

Prof. Damodaran notes that the data construction may not be
consistent from iteration to iteration. He also notes that,
"the best use for my data is in real time corporate financial analysis
and valuation." Here, gross margin data compiled by Prof. Damodaran are
optionally used to model the distribution of price-cost margin
across firms that antitrust enforcement agencies are likely to review in
merger enforcement investigations over a multi-year span. The
implicit assumption is that refinements in source-data construction from
iteration to iteration do not result in inconsistent estimates of
the empirical distribution of margins estimated using
a Gaussian kernel density estimator (KDE).

Second, other procedures included in this package allow the researcher to
generate margins for a single firm and impute margins of other firms in
a model relevant antitrust market based on FOCs for profit maximization by
firms facing MNL demand. In that exercise, the distribution of
inferred margins does not follow the empirical distribution estimated
from the source data, due to restrictions resulting from the distribution of
generated market shares across firms and the feasibility condition that
price-cost margins fall in the interval :math:`[0, 1]`.

"""

import shutil
import zipfile
from pathlib import Path
from types import MappingProxyType

import numpy as np
import urllib3
from joblib import Parallel, delayed
from numpy.random import PCG64DXSM, Generator, SeedSequence
from scipy import stats  # type: ignore
from xlrd import open_workbook  # type: ignore

from .. import NTHREADS, VERSION, ArrayDouble, this_yaml  # noqa: TID252
from .. import WORK_DIR as PKG_WORK_DIR  # noqa: TID252
from .. import data as mdat  # noqa: TID252
from . import _mappingproxy_from_mapping

__version__ = VERSION

WORK_DIR = globals().get("WORK_DIR", PKG_WORK_DIR)
"""Redefined, in case the user defines WORK_DIR betweeen module imports."""

MGNDATA_ARCHIVE_PATH = WORK_DIR / "damodaran_margin_data_serialized.zip"

type DamodaranMarginData = MappingProxyType[str, MappingProxyType[str, float | int]]

u3pm = urllib3.PoolManager()


def margin_data_getter(  # noqa: PLR0912
    _table_name: str = "margin",
    *,
    data_archive_path: Path = MGNDATA_ARCHIVE_PATH,
    data_download_flag: bool = False,
) -> DamodaranMarginData:
    if _table_name != "margin":  # Not validated for other tables
        raise ValueError(
            "This code is designed for parsing Prof. Damodaran's margin tables."
        )

    data_archive_path = data_archive_path or MGNDATA_ARCHIVE_PATH
    workbook_path = data_archive_path.parent / f"damodaran_{_table_name}_data.xls"
    if data_archive_path.is_file() and not data_download_flag:
        with zipfile.ZipFile(data_archive_path) as _yzip:
            margin_data_dict = this_yaml.load(
                _yzip.read(data_archive_path.with_suffix(".yaml").name)
            )
        return margin_data_dict
    elif workbook_path.is_file():
        workbook_path.unlink()
        if data_archive_path.is_file():
            data_archive_path.unlink()

    margin_urlstr = (
        f"https://pages.stern.nyu.edu/~adamodar/pc/datasets/{_table_name}.xls"
    )
    try:
        chunk_size_ = 1024 * 1024
        with (
            u3pm.request(
                "GET", margin_urlstr, preload_content=False
            ) as _urlopen_handle,
            workbook_path.open("wb") as margin_file,
        ):
            while True:
                data_ = _urlopen_handle.read(chunk_size_)
                if not data_:
                    break
                margin_file.write(data_)

        print(f"Downloaded {margin_urlstr} to {workbook_path}.")

    except urllib3.exceptions.MaxRetryError as error_:
        if isinstance(error_.__cause__, urllib3.exceptions.SSLError):
            # Works fine with other sites secured with certificates
            # from the Internet2 CA, such as,
            # https://snap.stanford.edu/data/web-Stanford.txt.gz
            print(
                f"WARNING: Could not establish secure connection to, {margin_urlstr}."
                "Using bundled copy."
            )
            if not workbook_path.is_file():
                shutil.copy2(mdat.DAMODARAN_MARGIN_WORKBOOK, workbook_path)
        else:
            raise error_

    xl_book = open_workbook(workbook_path, ragged_rows=True, on_demand=True)
    xl_sheet = xl_book.sheet_by_name("Industry Averages")

    margin_dict_in: dict[str, dict[str, float | int]] = {}
    row_keys: list[str] = []
    read_row_flag = False
    for _ridx in range(xl_sheet.nrows):
        xl_row = xl_sheet.row_values(_ridx)
        if xl_row[0] == "Industry Name":
            read_row_flag = True
            row_keys = xl_row
            continue

        if not xl_row[0] or not read_row_flag:
            continue

        xl_row[1] = int(xl_row[1])
        margin_dict_in[xl_row[0]] = dict(zip(row_keys[1:], xl_row[1:], strict=True))

    margin_dict = _mappingproxy_from_mapping(margin_dict_in)
    with (
        zipfile.ZipFile(data_archive_path, "w") as _yzip,
        _yzip.open(f"{data_archive_path.stem}.yaml", "w") as _yfh,
    ):
        this_yaml.dump(margin_dict, _yfh)

    return margin_dict


def margin_data_builder(
    _src_data_dict: DamodaranMarginData | None = None, /
) -> tuple[ArrayDouble, ArrayDouble]:
    if _src_data_dict is None:
        _src_data_dict = margin_data_getter()

    margin_data_wts, margin_data_obs = (
        _f.flatten()
        for _f in np.hsplit(
            np.array([
                tuple(
                    _src_data_dict[_g][_h] for _h in ["Number of firms", "Gross Margin"]
                )
                for _g in _src_data_dict
                if not _g.startswith("Total Market")
                and _g
                not in {
                    "Bank (Money Center)",
                    "Banks (Regional)",
                    "Brokerage & Investment Banking",
                    "Financial Svcs. (Non-bank & Insurance)",
                    "Insurance (General)",
                    "Insurance (Life)",
                    "Insurance (Prop/Cas.)",
                    "Investments & Asset Management",
                    "R.E.I.T.",
                    "Retail (REITs)",
                    "Reinsurance",
                }
            ]),
            2,
        )
    )

    margin_wtd_avg = np.average(margin_data_obs, weights=margin_data_wts)
    # https://www.itl.nist.gov/div898/software/dataplot/refman2/ch2/weighvar.pdf
    margin_wtd_stderr = np.sqrt(
        np.average((margin_data_obs - margin_wtd_avg) ** 2, weights=margin_data_wts)
        * (len(margin_data_wts) / (len(margin_data_wts) - 1))
    )

    return np.stack([margin_data_obs, margin_data_wts], axis=1, dtype=float), np.round(
        (
            margin_wtd_avg,
            margin_wtd_stderr,
            margin_data_obs.min(),
            margin_data_obs.max(),
        ),
        8,
    )


def margin_data_resampler(
    _dist_parms: ArrayDouble,
    /,
    *,
    sample_size: int | tuple[int, ...],
    seed_sequence: SeedSequence | None = None,
    nthreads: int = NTHREADS,
) -> ArrayDouble:
    """
    Generate draws from the empirical distribution bassed on Prof. Damodaran's margin data.

    The empirical distribution is estimated using a Gaussian KDE; the bandwidth
    selected using Silverman's rule is narrowed to reflect that the margin data
    are multimodal. Margins for firms in finance, investment, insurance,
    reinsurance, and REITs are excluded from the sample used to estimate the
    empirical distribution.

    Parameters
    ----------

    _dist_parms
        Array of margins and firm counts extracted from Prof. Damodaran's margin data

    sample_size
        Number of draws; if tuple, (number of draws, number of columns)

    seed_sequence
        SeedSequence for seeding random-number generator when results
        are to be repeatable

    nthreads
        Number of threads to use in generating margin data.
    Returns
    -------
        Array of margin values

    """

    _dist_parms = margin_data_builder()[0] if _dist_parms is None else _dist_parms

    _seed = seed_sequence or SeedSequence(pool_size=8)

    _x, _w = _dist_parms[:, 0], _dist_parms[:, 1]

    margin_kde = stats.gaussian_kde(_x, weights=_w, bw_method="silverman")
    margin_kde.set_bandwidth(bw_method=margin_kde.factor / 3.0)

    if isinstance(sample_size, int):
        return margin_kde.resample(sample_size, seed=Generator(PCG64DXSM(_seed))).T

    elif isinstance(sample_size, tuple) and len(sample_size) == 2:
        ret_array = np.empty(sample_size, float)

        _ssz, _ncol = sample_size
        dat_list = Parallel(n_jobs=min(nthreads, _ncol), prefer="threads")(
            delayed(margin_kde.resample)(_ssz, seed=Generator(PCG64DXSM(_col_seed)))
            for _col_seed in _seed.spawn(_ncol)
        )

        for _i in range(_ncol):
            ret_array[:, [_i]] = dat_list[_i].T

        return ret_array
    else:
        raise ValueError(f"Invalid sample size: {sample_size!r}")
