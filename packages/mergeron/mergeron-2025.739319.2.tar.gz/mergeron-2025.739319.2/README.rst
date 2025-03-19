mergeron: Merger Policy Analysis with Python
============================================

Usage
-----

*Visualizing Guidelines boundaries*

.. code:: python

    %matplotlib inline
    from mergeron.core import guidelines_boundaries as gbl
    from mergeron.core import guidelines_boundary_functions as gbf
    from math import sqrt

    delta_bound = 0.01
    conc_boundary = gbl.ConcentrationBoundary(delta_bound, "ΔHHI")
    share_boundary = gbl.ConcentrationBoundary(2 * sqrt(delta_bound / 2), "Combined share")

    divr_boundary_a = gbl.DiversionRatioBoundary(
        gbl.guppi_from_delta(delta_bound, m_star=1.0, r_bar=0.85),
        agg_method=gbl.UPPAggrSelector.AVG
    )

    divr_boundary_i = gbl.DiversionRatioBoundary(
        gbl.guppi_from_delta(delta_bound, m_star=1.0, r_bar=0.85),
        agg_method=gbl.UPPAggrSelector.MIN
    )

    divr_boundary_x = gbl.DiversionRatioBoundary(
        gbl.guppi_from_delta(delta_bound, m_star=1.0, r_bar=0.85),
        agg_method=gbl.UPPAggrSelector.MAX
    )


Plots are written to PDF, typically, with ``backend="pgf"`` as the
default backend in the function, ``gbf.boundary_plot``. Here, we set the
backend to ``None`` to skip fine-tuning plots for PDF generation.

.. code:: python

    plt, fig, ax, layout_axis = gbf.boundary_plot(backend=None)

    ax.set_title("Concentration and Diversion Ratio Boundaries")

    ax.plot(conc_boundary.coordinates[:, 0], conc_boundary.coordinates[:, 1], color="black", linestyle="-", label="ΔHHI")
    ax.plot(share_boundary.coordinates[:, 0], share_boundary.coordinates[:, 1], color="black", linestyle=":", label="Combined share")
    ax.plot(divr_boundary_a.coordinates[:, 0], divr_boundary_a.coordinates[:, 1], "b-", label="Average Diversion Ratio")
    ax.plot(divr_boundary_i.coordinates[:, 0], divr_boundary_i.coordinates[:, 1], "r-", label="Minimum Diversion Ratio")
    ax.plot(divr_boundary_x.coordinates[:, 0], divr_boundary_x.coordinates[:, 1], "g-", label="Maximum Diversion Ratio")

    _ = fig.legend(loc=(0.4, 0.7), frameon=False)


*Analyzing FTC Merger Investigations Data*

.. code:: python

    from mergeron.core import ftc_merger_investigations_data as fid
    import tabulate

    inv_data = fid.construct_data(fid.INVDATA_ARCHIVE_PATH)


We can now analyze counts of markets reported in the source data, by
table number. Note that odd-numbered tables report FTC investigations
data organized by HHI and ΔHHI, while even-numbered tables report by
firm-count.

.. code:: python

    from mergeron.gen import enforcement_stats as esl

    print("Enforcement Rates in Markets with Entry Barriers, 1996-2003 vs 2004-2011")
    print()
    counts_by_delta_1 = esl.enf_cnts_bydelta(
        inv_data["1996-2003"]["ByHHIandDelta"]["Table 9.2"].data_array
    )
    counts_by_delta_2 = esl.enf_cnts_bydelta(
        inv_data["2004-2011"]["ByHHIandDelta"]["Table 9.2"].data_array
    )
    observed_enforcement_rates = list(zip(
        (
            {_v: _k for _k, _v in fid.CONC_DELTA_DICT.items()}[i]
            for i in counts_by_delta_1[:, 0]
        ),
        (
            f"{_a[1] / _a[-1]: <12.2%}" if _a[-1] else "--"
            for _a in counts_by_delta_1
        ),
        (
            f"{_e[1] / _e[-1]: <12.2%}" if _e[-1] else "--"
            for _e in counts_by_delta_2
        ),
    ))

    observed_enforcement_rates.append([
        "Total",
        f"{counts_by_delta_1[:, 1].sum() / counts_by_delta_1[:, -1].sum(): <12.2%}",
        f"{counts_by_delta_2[:, 1].sum() / counts_by_delta_2[:, -1].sum(): <12.2%}",
    ])

    print(tabulate.tabulate(
        observed_enforcement_rates,
        tablefmt="simple",
        headers=("ΔHHI", "1996-2003", "2004-2011"),
        stralign="center",
        maxcolwidths=36,
        maxheadercolwidths=36,
    ))


.. parsed-literal::

    Enforcement Rates in Markets with Entry Barriers, 1996-2003 vs 2004-2011

        ΔHHI        1996-2003    2004-2011
    -------------  -----------  -----------
       0 - 100         --         100.00%
      100 - 200      33.33%       50.00%
      200 - 300      33.33%       50.00%
      300 - 500      75.00%       77.78%
      500 - 800      59.09%       54.55%
     800 - 1,200     93.33%       81.82%
    1,200 - 2,500    90.91%       84.38%
       2,500 +       96.00%       100.00%
        Total        81.65%       82.86%


Generating synthetic market data and analyzing enforcement rates


