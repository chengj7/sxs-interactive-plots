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
    script_file_path = "https://raw.githubusercontent.com/chengj7/sxs-interactive-plots/refs/heads/main/plots/isxs_marimo.py"
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
def _(mo):
    header = mo.vstack([mo.md(r"""<h1 style="text-align: center;">Waveform Explorer</h1>"""), mo.md("-------------------------------")])
    header
    return


@app.cell
def _(isxs):
    hlm, h_id_list, strain_data, metadata_list = isxs.load_data()
    return h_id_list, hlm, metadata_list, strain_data


@app.cell
def _(mo):
    show_CE = mo.ui.checkbox(value=True, label="CE Noise Curve")
    show_aLIGO = mo.ui.checkbox(value=True, label="aLIGO Noise Curve")
    show_aPlus = mo.ui.checkbox(value=True, label="A+ LIGO Noise Curve")
    return show_CE, show_aLIGO, show_aPlus


@app.cell
def _(mo):
    tabs = mo.ui.tabs({
    "Mass Ratio": mo.md(r"""# Varying <span style="color:red">Mass Ratios</span> Examples #"""),
    "Eccentricity": mo.md(r"""# High <span style="color:green">Eccentricity</span> Examples #"""),
    "Precession": mo.md(r"""# High <span style="color:lightblue">Precession</span> Examples #"""),
    "Custom": mo.md(r"""# User Added Systems #""")
    })
    tabs
    return (tabs,)


@app.cell
def _(h_id_list, mo, tabs):
    if tabs.value == "Mass Ratio":
        dropdown = mo.ui.dropdown(
            options=["SXS:BBH:1154 (MR:1)", "SXS:BBH:2139 (MR:3)", "SXS:BBH:1441 (MR:8)", "SXS:BBH:1107 (MR:10)"],
            value="SXS:BBH:1154 (MR:1)",
            label="Choose a Mass Ratio",
            searchable=True,
        )
    elif tabs.value == "Eccentricity":
        dropdown = mo.ui.dropdown(
            options=["SXS:BBH:2527 (MR:1)", "SXS:BBH:3946 (MR:2)", "SXS:BBH:2550 (MR:4)", "SXS:BBH:2557 (MR:6)", "SXS:BBH:2595 (MR:1)", "SXS:BBH:2537 (MR:3)", "SXS:BBH:2553 (MR:6)", "SXS:BBH:2560 (MR:8)"],
            value="SXS:BBH:2527 (MR:1)",
            label="Choose a system:",
            searchable=True,
        )
    elif tabs.value == "Precession":
        dropdown = mo.ui.dropdown(
            options=["SXS:BBH:2442 (MR:1)", "SXS:BBH:2443 (MR:1)", "SXS:BBH:0832 (MR:2)"],
            value="SXS:BBH:2442 (MR:1)",
            label="Choose a system:",
            searchable=True,
        )
    elif tabs.value == "Custom":
        dropdown = mo.ui.dropdown(
            options=[h_id for h_id in h_id_list[19:]],
            value = h_id_list[19],
            label="Choose a system:",
            searchable=True,
        )
    Distance = mo.ui.slider(100.0,10000.0,10.0, label="Distance (Mpc)", include_input=True, full_width=True)
    Mass = mo.ui.slider(5.0,10000.0,1.0, label="Mass (Solar Mass M☉)", value=33 ,include_input=True, full_width=True)
    return Distance, Mass, dropdown


@app.cell
def _(
    Distance,
    Mass,
    dropdown,
    h_id_list,
    hlm,
    isxs,
    metadata_list,
    show_CE,
    show_aLIGO,
    show_aPlus,
    strain_data,
):
    dropdown.value and isxs.run(dropdown.value[:12], h_id_list, strain_data, metadata_list, hlm, Mass, Distance, dropdown, show_CE, show_aLIGO, show_aPlus)
    return


@app.cell
def _(mo):
    mo.md("""
    -------------------------------
    """)
    return


@app.cell
def _(mo):
    tabs_writeup = mo.ui.tabs({
    "Science": mo.md(r"""# About the science #"""),
    "Code": mo.md(r"""# About the code #"""),
    })
    tabs_writeup
    return (tabs_writeup,)


@app.cell
def _(mo):
    para_code = mo.md(r"""
    Waveform Explorer uses marimo, a reactive Python notebook that allows for user
    interactivity, to explore a set of gravitational waveform simulations produced by the
    Simulating eXtreme Spacetimes (SXS) collaboration. This tool is meant to be used to
    explore current gravitational waveforms in the context of the next-generation
    gravitational wave detector, Cosmic Explorer. In this tab, we discuss the key
    specifics of how the code works, for the curious reader.

    ## Data Source

    Since SXS is not compatible with running marimo in a WebAssembly environment, we
    instead pull several handpicked waveforms that demonstrate various physical features
    spanning mass ratio, eccentricity, and precession. In total, fifteen different SXS
    waveforms are present in Waveform Explorer, with room and instructions to add more in
    a local copy.

    The data is saved in a `.npz` file, `marimodata.npz`, generated using the script
    `premarimo_load.py`. This file includes each waveform's strain data in the frequency
    domain along with its metadata.

    ## Creating the Dataset (`premarimo_load.py`)

    ### 1. Dimensionalizing the strain

    Raw SXS catalog waveforms are independent of mass and distance. Since our goal is to
    view these waveforms under the physical lens of varying mass and distance, we
    dimensionalize the strain as follows:

    ```python
    h.time = h.time * G * (M / (c**3))
    h = h * (M / r) * (G / (c**2))
    ```

    This leaves `h.time` with dimensions of time, and the strain `h` as dimensionless.
    Here, $h$ is the strain, $G$ is the gravitational constant, $M$ is mass, $r$ is
    distance, and $c$ is the speed of light.

    ### 2. Pre-processing

    We then want to transform the strain into the frequency domain using a Fast Fourier
    Transform. Before doing so, we follow a pre-processing procedure outlined below.
    Since Waveform Explorer is designed to examine the harmonic modes of a selected
    waveform, we interpolate, taper, and transition each mode individually. The only
    significant deviation is that two different padding values are used for eccentric
    versus non-eccentric systems:

    ```python
    h_lm = h[:, h.index(l, m)]
    h_lm_interpolated = h_lm.interpolate(np.arange(h_lm.t[0], h_lm.t[-1], dt))
    hlm_tapered = h_lm_interpolated.taper(0, h.t[0] + 1000 * (G * (M / (c**3))))
    hlm_transitioned = hlm_tapered.transition_to_constant(
        h.max_norm_time() + 100 * (G * (M / (c**3)))
    )

    if type(metadata.reference_eccentricity) == float and (
        metadata.reference_eccentricity > 0.3
    ):
        hlm_padded = hlm_transitioned.pad(250000 * (G * (M / (c**3))))
    else:
        hlm_padded = hlm_transitioned.pad(25000 * (G * (M / (c**3))))

    hlm_line_subtracted = hlm_padded.line_subtraction().real
    ```

    Higher padding yields higher frequency resolution but slower execution time. A padding
    value of `25000` was suitable for most non-eccentric systems. For high-eccentricity
    systems, however, this value produced low resolution, so a much higher value of
    `250000` was used instead.

    ### 3. Taking the FFT
    Now, we take the FFT to transform the strain into the frequency domain:

    ```python
    htilde_lm = np.abs(np.fft.rfft(hlm_line_subtracted.ndarray.astype(float)) * dt)
    frequencies_lm = np.abs(
        np.fft.rfftfreq(len(hlm_line_subtracted.ndarray.astype(float)), dt)
    )
    htilde_lm_scaled = 2 * np.abs(htilde_lm) * np.abs(np.sqrt(frequencies_lm))
    ```

    ### 4. Cleaning up noise

    We're now almost ready to use and plot the strain. However, the Fourier-transformed strain still contains noise at high frequencies (after
    ringdown) and low frequencies (before the simulation "turns on"). Much of this, though
    not all, is removed by resampling logarithmically in frequency with this function:

    ```python
    def cut_freq(freq, htilde):
        log_original_frequencies = np.log(freq)
        log_original_htilde = np.log(htilde)

        min_freq = freq.min()
        max_freq = freq.max()
        new_frequencies = np.logspace(np.log10(min_freq), np.log10(max_freq), 480)
        log_new_frequencies = np.log(new_frequencies)
        log_new_frequencies[0] = log_original_frequencies[0]
        log_new_frequencies[-1] = log_original_frequencies[-1]

        interpolation_function = scipy.interpolate.interp1d(
            log_original_frequencies, log_original_htilde, kind="linear"
        )
        log_interpolated_htilde = interpolation_function(log_new_frequencies)

        interpolated_htilde = np.exp(log_interpolated_htilde)

        return new_frequencies, interpolated_htilde
    ```

    These processed strains are saved into `marimodata.npz`, along with each waveform's
    corresponding metadata and SXS ID number.

    ## Visualization (`SXSInteractivePlots.py`)

    The marimo notebook `SXSInteractivePlots.py` extracts and loads this data file, and
    plots all waveform modes in the frequency domain alongside the Cosmic Explorer,
    aLIGO, and A+ LIGO noise curves (taken from `bilby`). Three tabs are provided
    for the three categories of example waveforms explored here: high/low mass ratios,
    eccentricities, and precession. A table containing relevant metadata about each binary
    system — including number of orbits, spin, and eccentricity — is also included.
    """)
    return (para_code,)


@app.cell
def _(mo, para_code, tabs_writeup):
    if tabs_writeup.value == "Code":
        tabs_science = None
        _out = para_code
    elif tabs_writeup.value == "Science":
        tabs_science = mo.ui.tabs({
            "Motivation": mo.md(r"""# Motivation #"""),
            "Mass Ratio": mo.md(r"""# Mass Ratio #"""),
            "Eccentricity": mo.md(r"""# Eccentricity #"""),
            "Precession": mo.md(r"""# Precession #"""),
        })
        _out = tabs_science
    else:
        tabs_science = None
        _out = None

    _out
    return (tabs_science,)


@app.cell
def _(mo):
    para_motivation = mo.md(r"""

    Cosmic Explorer is a next-generation gravitational wave detector, more sensitive than
    any current LIGO facility. For one, the lower frequency limit of Cosmic Explorer is
    half that of aLIGO/Virgo/KAGRA — roughly 5 Hz, compared to the current detectors'
    10 Hz (1). At that frequency, the CE strain sensitivity is better than
    $\sim 10^{-23}\ \mathrm{Hz}^{-1/2}$, compared to aLIGO achieving that same
    $10^{-23}\ \mathrm{Hz}^{-1/2}$ sensitivity only at $\sim 100$ Hz. At 100 Hz, Cosmic
    Explorer is one order of magnitude more sensitive than aLIGO (3). Thus, in principle,
    with this improved sensitivity CE covers a wider range of detectable gravitational
    waves from binary black hole systems, ranging from masses of roughly
    $100$–$1000\ M_\odot$.

    ## Lower Frequency Limit

    The improved lower frequency limit for Cosmic Explorer is crucial in one other way.
    Low-mass binaries ($<10^4\ M_\odot$) radiate in the frequency band generally covered
    by terrestrial detectors like LIGO/Virgo/KAGRA (LVK), roughly 10–1000 Hz, but
    Numerical Relativity (NR) simulations are typically very computationally expensive. As
    a result, NR simulations generally cover only the last ~20 orbits of inspiral before
    computation becomes prohibitively expensive and phase error begins to significantly
    affect simulation accuracy.

    These ~20 orbits are not guaranteed to cover the entire LVK detection band, which
    becomes an even more serious problem for Cosmic Explorer, given its lower frequency
    limit of ~5 Hz, potentially missing important physics. Not only does CE observe more
    signals at lower frequencies, but for a fixed mass, a system spends longer at lower
    frequencies. This means the system can be observed for longer, more data can be
    gathered to fit its parameters, and its evolution over time can be better understood.

    This matters both for detection and for studying subtler physics encoded in the
    waveform's evolution, such as dark matter effects or physics beyond General
    Relativity. If NR alone isn't capable of consistently and efficiently producing
    waveforms spanning CE's full frequency band, this motivates the development of hybrid
    models, such as combining post-Newtonian and Numerical Relativity approaches.

    ## Harmonic Modes

    Gravitational waveforms are mathematically described by decomposing them into
    spin-weighted spherical harmonics. Since these harmonic modes can in principle be
    described *ad infinitum*, a natural question when generating waveform simulations is
    how many modes are "enough" to adequately represent the system without losing
    significant physics. The SXS catalog includes modes up to $(l, m) = (8, 8)$, which has
    proven effective for aLIGO, but Waveform Explorer aims to investigate whether Cosmic
    Explorer's improved sensitivity demands more.

    While the $(2,2)$ mode remains dominant, binary black hole systems where the late
    inspiral and merger contribute significantly to the waveform's signal-to-noise ratio
    (SNR) have been shown to place greater importance on higher harmonics (). Furthermore,
    as the mass ratio between the two black holes in a binary increases, so does the
    significance of additional harmonics. Waveform Explorer demonstrates this
    qualitatively: comparing a mass-ratio-1 (MR=1) system against a mass-ratio-10 (MR=10)
    system, both with fixed mass $M = 33\ M_\odot$ and distance $R = 100$ Mpc, noticeably
    more modes are visible for the MR=10 system with both aLIGO and CE.

    Higher harmonics generally enable more accurate descriptions of the binary system ().
    The measurement of a second harmonic in addition to the dominant $(2,2)$ mode is what
    first enables measurement of the system's properties, with additional harmonics acting
    as refinements that improve accuracy. Measuring several harmonics is particularly
    useful for breaking known degeneracies, such as between a system's distance and orientation,
    or between the binary black holes' mass ratio and individual spins ().
    """)
    return (para_motivation,)


@app.cell
def _(mo):
    para_massratio = mo.md(r"""

    ## Equal vs. Unequal Mass Ratios

    For an equal-mass, non-spinning binary on a quasicircular orbit, the gravitational
    waveform is dominated by even-$m$ harmonic modes, and most notably by the $(2,2)$ mode.
    Odd-$m$ modes, such as $(2,1)$ and $(3,3)$, vanish almost entirely in this limit. To understand
    this, one can consider the arguments:

    **1. Symmetry.** An equal-mass binary is invariant under a $\pi$-rotation
    about the axis perpendicular to the orbital plane (swapping the two identical bodies
    is indistinguishable from rotating the system by 180°). This symmetry forces the
    amplitude of every odd-$m$ mode to vanish exactly. To see this, consider that
    $h_{\ell m} \propto e^{-im\Phi(t)}$, where $\Phi(t)$ is the orbital phase. So, for an identical binary system,
    rotating by $\pi$ gives 
    $$e^{-im(\Phi + \pi)} = e^{-im\pi}\, e^{-im\Phi} = (-1)^m\, e^{-im\Phi},$$
    so symmetry requires 
    $$h_{\ell m} = (-1)^m\, h_{\ell m}.$$
    For this to be held true for odd modes, notice that $h_{\ell m}$ must be zero.
    The same argument has been
    demonstrated explicitly in numerical-relativity studies of equal-mass mergers, where
    odd-$m$ mode amplitudes go to zero because of this $\pi$-rotation symmetry, only
    becoming non-negligible once the masses are unequal.

    **2. Post-Newtonian scaling.** In PN theory, the mode amplitudes can be
    organized by how they scale with the binary's mass parameters, typically the
    symmetric mass ratio $\eta = m_1 m_2 / M^2$ and the (normalized) mass difference
    $\delta = (m_1 - m_2)/M$. The leading-order PN mode structure shows a clean pattern:
    even-$m$ modes ($h_{22}$, $h_{44}$, ...) scale with powers of $\eta$, while odd-$m$
    modes ($h_{21}$, $h_{33}$, ...) scale with odd powers of $\delta$. Since
    $\delta \to 0$ exactly when $m_1 = m_2$, the odd-$m$ modes vanish identically in the
    equal-mass limit, while the even-$m$ modes remain since they only depend on $\eta$ 
    (which stays nonzero for any mass ratio). This leading-order mode structure is laid out
    explicitly in (3.1) in Borhanian et al. (2019) [arXiv:1901.08516], depicting the PN
    mode amplitude predictions according to theory.

    ## Higher Harmonics

    As the mass ratio departs from unity, $\delta$ grows away from zero, and the odd-$m$
    modes (along with higher harmonics more generally) become increasingly significant
    relative to the dominant $(2,2)$ mode. This is exactly what Waveform Explorer
    illustrates qualitatively: comparing a mass-ratio-1 system against a mass-ratio-10
    system at fixed mass and distance, noticeably more modes become visible above the
    noise floor for both aLIGO and CE as the mass ratio increases.

    This trend has also been quantified directly. In a study of higher-order mode
    measurability, the $(3,3)$ mode was shown to grow steadily more significant relative to
    the dominant $(2,2)$ mode as mass ratio increases. For example, for a system with total mass of
    $50\,M_\odot$, the $(3,3)$ mode reaches about ~10% of the $(2,2)$ mode's amplitude at a 2:1
    mass ratio, growing to about 20% at a 5:1 mass ratio, and can exceed one-third of the
    $(2,2)$ mode's significance at high total mass and high mass ratio (Mills & Fairhurst,
    2021, [arXiv:2007.04313]).

    ## Potential Consequences for Waveform Modeling

    Unequal mass ratios don't just affect the waveform's harmonics, but they also make it harder
    for PN and NR methods to agree with each other, which matters directly for building
    hybrid waveforms (PN inspiral + NR merger):

    > For unequal masses, the errors between different PN approximants increase with mass
    > ratio. Thus, at 3.5PN, hybrids for higher-mass-ratio systems would require NR
    > waveforms with many more gravitational-wave cycles to guarantee no adverse impact on
    > parameter estimation.
    >
    > — MacDonald et al. (2013), *Phys. Rev. D* 87, 024009
    > [[link]](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.87.024009)

    In other words, as mass ratio increases, not only does the physical content of the
    waveform become richer (more significant higher harmonics), but the NR simulations
    themselves need to be run for longer (covering more inspiral cycles) for a hybrid
    waveform to remain trustworthy for parameter estimation. This compounds with the
    motivation discussed in the Motivation tab: Cosmic Explorer's improved low-frequency
    sensitivity demands NR waveforms that are both longer *and*, for high-mass-ratio
    systems, richer in harmonic modes, which can be quite an expensive computational ask.
    """)
    return (para_massratio,)


@app.cell
def _(mo):
    para_eccentricity = mo.md(r"""

    The key detail in the gravitational waveforms of eccentric binary black hole systems
    is the highly oscillatory nature of the system's inspiral. The intuitive description
    is as follows:

    1. At periapsis (the closest point between the two black holes in an eccentric
       orbit), the black holes orbit each other at their fastest rate, giving a high
       orbital frequency, $f_{\mathrm{orbital,max}}$.
    2. At apoapsis (the farthest point between the two black holes in an eccentric
       orbit), the black holes orbit each other at their slowest rate, giving a low
       orbital frequency, $f_{\mathrm{orbital,min}}$.
    3. If the two black holes were not approaching merger, and were simply orbiting one
       another indefinitely, the overall frequency of the system would oscillate between
       $f_{\mathrm{orbital,max}}$ and $f_{\mathrm{orbital,min}}$.
    4. However, the two black holes are slowly approaching merger due to the emission of
       gravitational waves, introducing an "inspiral frequency," $f_{\mathrm{inspiral}}$,
       that increases monotonically over time.
    5. Combining these two effects, the system's frequency increases overall while
       oscillating, depicting a chirping signal with a superimposed periodic modulation.

    Another key observation is that as the binary nears merger, the orbit loses energy
    through the emission of gravitational waves and gradually becomes less eccentric and
    more circular — a process known as circularization (Peters 1964). More power is emitted 
    during periapsis compared to apoapsis due to the stronger gravitational pulls from the 
    two black holes. This is why, qualitatively, the modes in Waveform Explorer appear to 
    "flatten out" as the system approaches merger, with merger and ringdown behaving similarly to 
    those of non-eccentric systems.
    """)
    return (para_eccentricity,)


@app.cell
def _(mo):
    para_precession = mo.md(r"""

    The key part of the intuition behind precessing binary black hole systems lies in the
    concept of frame dragging, which has historically been described using one of two
    pictures:

    ## 1. The Fluid Analogy
    *(more physically intuitive, but less accurate)*

    - Imagine a mass (such as a black hole) spinning within a "fluid," causing the fluid
      immediately surrounding it to swirl.
    - The swirling fluid affects the motion of another mass (a companion black hole)
      "caught" in the swirling motion, causing it to wobble, or precess.

    ## 2. The Gravitomagnetic Analogy
    *(more accurate description)*

    Analogously to how electric charge relates to electric/magnetic fields, moving
    mass-energy generates a gravitomagnetic field:

    - Electric charge is like mass: charge creates an electric field that pulls
      opposite charges inward; mass warps space and time, pulling other masses inward.
    - Moving charge is like spin: a moving charge generates a non-uniform magnetic
      field that curls around it, just as a spinning mass generates a non-uniform
      gravitomagnetic field that curls around it.
    - A black hole moving through this non-uniform gravitomagnetic field experiences a
      torque, which causes it to precess.

    ## Inertial vs. Co-precessing Frames

    For a precessing system, the binary can be viewed either through an inertial frame
    or a non-inertial, co-precessing frame (a frame that rotates along with the
    binary). The spherical harmonics of the waveform in the inertial frame are a sum of
    multiple harmonics in the co-precessing frame, with the transformation between the two
    described by Wigner-D matrices, which characterize rotations of angular momentum
    states.

    In simplified terms, each $l$ mode in the inertial frame can be decomposed as a
    combination of the $m$ modes for that same $l$. For example, the $(2,2)$ mode in the
    inertial frame can be decomposed into a combination of the five harmonics in the
    co-precessing frame:

    $$(l{=}2, m{=}{-}2),\quad (l{=}2, m{=}{-}1),\quad (l{=}2, m{=}0),\quad
    (l{=}2, m{=}1),\quad (l{=}2, m{=}2)$$

    Since the Wigner-D matrices depend on the time-varying Euler angles that describe the
    precession, the amount of energy mixing from each co-precessing-frame mode into the
    inertial-frame (observer-frame) modes also depends on time. As a result, the harmonics
    evolve over time, producing a modulation effect in their amplitudes.
    """)
    return (para_precession,)


@app.cell
def _(
    para_eccentricity,
    para_massratio,
    para_motivation,
    para_precession,
    tabs_science,
):
    if tabs_science.value == "Motivation":
        _out = para_motivation
    elif tabs_science.value == "Mass Ratio":
        _out = para_massratio
    elif tabs_science.value == "Eccentricity":
        _out = para_eccentricity
    elif tabs_science.value == "Precession":
        _out = para_precession
    else:
        _out = None
    _out
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
