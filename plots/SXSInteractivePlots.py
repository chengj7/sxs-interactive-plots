# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ipython==9.7.0",
#     "marimo==0.17.8",
#     "matplotlib==3.10.7",
#     "numpy==2.3.4",
#     "pandas==2.3.3",
#     "plotly==6.4.0",
#     "requests==2.32.5",
#     "scipy==1.16.3",
# ]
# ///

import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full", app_title="waveform-explorer")


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
    import plotly.graph_objects as go
    import plotly.io as pio
    pio.renderers.default = 'iframe'
    import requests
    import os
    script_file_path = "https://chengj7.github.io/sxs-interactive-plots/plots/isxs_marimo.py"
    script_response = requests.get(script_file_path)

    base_dir = os.getcwd()
    public_dir = os.path.join(base_dir, "public")
    os.makedirs(public_dir, exist_ok=True)

    if script_response.status_code == 200:
        file_path = os.path.join(public_dir, "isxs_marimo.py")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script_response.text)
    else:
        raise Exception(f"Failed to download file: {script_response.status_code}")

    sys.path.append(public_dir)
    import isxs_marimo as isxs
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
    Distance_MR = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True, full_width=True)
    Mass_MR = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True, full_width=True)
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
    Distance_ecc = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True, full_with=True)
    Mass_ecc = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True, full_width=True)
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
    Distance_prec = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True, full_width=True)
    Mass_prec = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True, full_width=True)
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
