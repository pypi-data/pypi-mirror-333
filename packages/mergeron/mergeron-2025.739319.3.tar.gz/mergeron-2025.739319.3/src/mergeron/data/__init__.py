"""
Data useful for empirical analysis of merger enforcement policy

These data are processed for further analysis within relevant
submodules of the parent package. Thus, direct access is
unnecessary in routine use of this package.
"""

from importlib import resources

from .. import _PKG_NAME, VERSION  # noqa: TID252

__version__ = VERSION

data_resources = resources.files(f"{_PKG_NAME}.data")

DAMODARAN_MARGIN_WORKBOOK = data_resources / "damodaran_margin_data.xls"
"""
Python object pointing to included copy of Prof. Damodaran's margin data

Only used as a fallback, in case direct download from source fails.

NOTES
-----
Source data are from Prof. Aswath Damodaran, Stern School of Business, NYU; available online
at https://pages.stern.nyu.edu/~adamodar/pc/datasets/margin.xls


Use as, for example:

.. code-block:: python

    from mergeron.data import DAMODARAN_MARGIN_WORKBOOK

    shutil.copy2(DAMODARAN_MARGIN_WORKBOOK, Path.home() / f"{DAMODARAN_MARGIN_WORKBOOK.name}")
"""

FTC_MERGER_INVESTIGATIONS_DATA = data_resources / "ftc_merger_investigations_data.zip"
"""
FTC merger investigtions data published in 2004, 2007, 2008, and 2013

NOTES
-----
Raw data tables published by the FTC are loaded into a nested distionary, organized by
data period, table type, and table number. Each table is stored as a numerical array
(:mod:`numpy` arrray), with additonal attrubutes for the industry group and additonal
evidence noted in the source data.

Data for additonal data periods (time spans) not reported in the  source data,
e.g., 2004-2011, are constructed by subtracting counts in the base data from counts
in the cumulative data, by table, for "enforced" mergers and "closed" mergers, when
the cumulative data for the longer period are consistent with the base data for
a sub-period.
"""
