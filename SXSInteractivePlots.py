import marimo

__generated_with = "0.14.0"
app = marimo.App()


@app.cell
def _():
    import sys
    sys.path.append('public')
    import marimo as mo
    import re
    import math
    import numpy as np
    import pandas as pd
    import scipy.interpolate  
    import matplotlib.pyplot as plt
    from IPython.display import display
    import isxs_marimo as isxs
    import plotly.graph_objects as go
    import plotly.io as pio
    pio.renderers.default = 'iframe'
    import /public/isxs_marimo
    return isxs, mo


@app.cell
def _(isxs):
    hlm, h_id_list, strain_data, metadata_list = isxs.load_data()
    return h_id_list, hlm, metadata_list, strain_data


@app.cell
def _(mo):
    mo.md(r"""# Varying <span style="color:red">Mass Ratios</span> Examples #""")
    return


@app.cell
def _(mo):
    dropdown_MR = mo.ui.dropdown(
        options=["SXS:BBH:1154 (MR:1)", "SXS:BBH:2139 (MR:3)", "SXS:BBH:1441 (MR:8)", "SXS:BBH:1107 (MR:10)"],
        value="SXS:BBH:1154 (MR:1)",
        label="Choose a Mass Ratio",
        searchable=True,
    )
    Distance_MR = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True)
    Mass_MR = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True)
    return Distance_MR, Mass_MR, dropdown_MR


@app.cell
def _(
    Distance_MR,
    Mass_MR,
    dropdown_MR,
    h_id_list,
    hlm,
    isxs,
    metadata_list,
    strain_data,
):
    isxs.run(dropdown_MR.value[:12], h_id_list, strain_data, metadata_list, hlm, Mass_MR, Distance_MR, dropdown_MR)
    return


@app.cell
def _(mo):
    mo.md(r"""# High <span style="color:green">Eccentricity</span> Examples #""")
    return


@app.cell
def _(mo):
    dropdown_ecc = mo.ui.dropdown(
        options=["SXS:BBH:2527 (MR:1)", "SXS:BBH:3946 (MR:2)", "SXS:BBH:2550 (MR:4)", "SXS:BBH:2557 (MR:6)", "SXS:BBH:2595 (MR:1)", "SXS:BBH:2537 (MR:3)", "SXS:BBH:2553 (MR:6)", "SXS:BBH:2560 (MR:8)"],
        value="SXS:BBH:2527 (MR:1)",
        label="Choose a system:",
        searchable=True,
    )
    Distance_ecc = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True)
    Mass_ecc = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True)
    return Distance_ecc, Mass_ecc, dropdown_ecc


@app.cell
def _(
    Distance_ecc,
    Mass_ecc,
    dropdown_ecc,
    h_id_list,
    hlm,
    isxs,
    metadata_list,
    strain_data,
):
    isxs.run(dropdown_ecc.value[:12], h_id_list, strain_data, metadata_list, hlm, Mass_ecc, Distance_ecc, dropdown_ecc)
    return


@app.cell
def _(mo):
    mo.md(r"""# High <span style="color:lightblue">Precession</span> Examples #""")
    return


@app.cell
def _(mo):
    dropdown_prec = mo.ui.dropdown(
        options=["SXS:BBH:2442 (MR:1)", "SXS:BBH:2443 (MR:1)", "SXS:BBH:0832 (MR:2)"],
        value="SXS:BBH:2442 (MR:1)",
        label="Choose a system:",
        searchable=True,
    )
    Distance_prec = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True)
    Mass_prec = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True)
    return Distance_prec, Mass_prec, dropdown_prec


@app.cell
def _(
    Distance_prec,
    Mass_prec,
    dropdown_prec,
    h_id_list,
    hlm,
    isxs,
    metadata_list,
    strain_data,
):
    isxs.run(dropdown_prec.value[:12], h_id_list, strain_data, metadata_list, hlm, Mass_prec, Distance_prec, dropdown_prec)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
