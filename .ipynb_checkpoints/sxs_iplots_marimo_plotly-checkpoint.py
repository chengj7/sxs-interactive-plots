import sxs
import math
import numpy as np
import pandas as pd
import scipy.interpolate
import plotly.graph_objects as go
import marimo as mo
from IPython.display import display
import plotly.io as pio
pio.renderers.default = 'iframe'

G = 6.67430e-11
c = 3e8
M = 6.563e+31
r = 3.086e24
dt = 1e-4 #np.min(np.diff(h.t))


df = sxs.load("dataframe", tag="3.0.0")

def sort(binary_id):
    for i in range(len(df[:-20])):
        if df.iloc[i].name[-8:] == binary_id:
            return i

def load_strain(h_id):
    simulations = sxs.load("simulations")
    sxs_bbh_n = sxs.load(h_id)
    metadata = sxs_bbh_n.metadata
    h = sxs_bbh_n.h
    reference_index = h.index_closest_to(metadata.reference_time)
    h=h[reference_index:]
    print(f"n_orbits: {metadata.number_of_orbits:.3g} \nMass ratio: {metadata.reference_mass_ratio:.3g} \nEccentricity: {metadata.reference_eccentricity:.3g} \nchi1: [{", ".join(f"{c:.3g}" for c in metadata.reference_dimensionless_spin1)}] \nchi2: [{", ".join(f"{c:.3g}" for c in metadata.reference_dimensionless_spin2)}] \nchi1_Perp: {metadata.reference_chi1_perp} \nchi2_Perp: {metadata.reference_chi2_perp}")
    #print(int(h_id))
    #print(type(int(h_id)))
    n = sort(h_id[4:])
    display(df[n:n+1])
    return metadata, h

def dimensionalize(h, G, c, M, r):
    print(h.t)
    h.t = h.t * G * (M/(c**3))
    #print(h)
    h = h * (M/r) * (G/(c**2))
    t = h.t
    return h, t

def SPA_fft_calc(l,m, h, t, metadata):
    """
    Calculate the SPA and FFT of user selected mode of strain h
    """
    """
    #calculate for SPA
    h22 = h.data[:, h.index(2,2)]
    phi22 = np.unwrap(np.angle(h22))
    phi22_t = scipy.interpolate.CubicSpline(t, phi22)
    f22 = phi22_t.derivative()(t) / (2*np.pi)
    df22dt = phi22_t.derivative(2)(t) / (2*np.pi)
    hlm = h.data[:, h.index(l,m)]
    i1 = h.index_closest_to(0.5)
    i2 = h.max_norm_index()
    dt = 1e-4 #np.min(np.diff(h.t))
    Alm = np.abs(hlm)
    philm = np.unwrap(np.angle(hlm))
    philm_t = scipy.interpolate.CubicSpline(t, philm)
    flm, dflmdt = convertlm(m, f22, df22dt)
    """
    #calculate for FFT
    h_lm = h[:, h.index(l,m)]
    h_lm_interpolated = h_lm.interpolate(np.arange(h_lm.t[0], h_lm.t[-1], dt))
    hlm_tapered = h_lm_interpolated.taper(0, h.t[0]+1000*(G*(M/(c**3))))
    #hlm_transitioned = hlm_tapered.transition_to_constant(h.t[h.max_norm_index()+100])#, h.max_norm_time()+200*(G*(M/(c**3))))
    hlm_transitioned = hlm_tapered.transition_to_constant(h.max_norm_time()+100*(G*(M/(c**3))))#, h.max_norm_time()+200*(G*(M/(c**3))))
    if type(metadata.reference_eccentricity) == float and ((metadata.reference_eccentricity) > 0.1):
        hlm_padded = hlm_transitioned.pad(250000*(G*(M/(c**3))))
    else:
        hlm_padded = hlm_transitioned.pad(25000*(G*(M/(c**3))))
    hlm_line_subtracted = hlm_padded.line_subtraction().real
    #print(type(hlm_line_subtracted.ndarray))
    htilde_lm = np.abs(np.fft.rfft(hlm_line_subtracted.ndarray.astype(float))*dt)
    frequencies_lm = np.abs(np.fft.rfftfreq(len(hlm_line_subtracted.ndarray.astype(float)), dt))
    htilde_lm_scaled = 2*(np.abs(htilde_lm))*np.abs(np.sqrt(frequencies_lm))
    """
    #amplitude and frequency scaling
    f= -flm[i1:i2]
    amp = 2*np.abs(((1/2)*np.abs(hlm[i1:i2])) / np.sqrt(np.abs(dflmdt[i1:i2])))*np.sqrt(np.abs(flm[i1:i2]))
    """
    return frequencies_lm, htilde_lm_scaled #f, amp

def find_index(data, value):
    array = np.asarray(data)
    idx = (np.abs(data - value)).argmin()
    return idx

def create_functions(h, t, metadata):

    hlm = []
    for ell in range(2, h.ell_max + 1):
        for m in range(-ell, ell + 1):
            if ell < 7:
                if m > 0 and m >= ell - 2:
                    hlm.append([ell, m])
            else:
                if m == ell:
                    hlm.append([ell, m])
    
    frequencies_lm=[]; htilde_lm_scaled=[];
    fin_freq = (np.linalg.norm(h.angular_velocity[h.max_norm_index()]) / (2*np.pi))
    for i in hlm:
        frequencies_lm_i, htilde_lm_scaled_i = SPA_fft_calc(i[0], i[1], h, t, metadata);
        ini_freq_m = ((metadata.initial_orbital_frequency / (2*np.pi)) * i[-1]) * c**3/(G*M) * 1.15
        fin_freq_m = fin_freq * i[-1]
        ini_index_strain = find_index(frequencies_lm_i, ini_freq_m)
        fin_index_strain = find_index(frequencies_lm_i, fin_freq_m)
        cutoff_amp = htilde_lm_scaled_i[fin_index_strain] * 1e-2
        cutoff_index = find_index(htilde_lm_scaled_i[fin_index_strain:], cutoff_amp)
        #test_index = find_index(htilde_lm_scaled_i, amp_i[0])
        frequencies_lm.append(np.array(frequencies_lm_i)[ini_index_strain:fin_index_strain+cutoff_index][::12])
        htilde_lm_scaled.append(np.array(htilde_lm_scaled_i)[ini_index_strain:fin_index_strain+cutoff_index][::12])
    #print(len(f))
    frequencies_lm=np.array(frequencies_lm, dtype=object); htilde_lm_scaled=np.array(htilde_lm_scaled, dtype=object)
        
    return frequencies_lm, htilde_lm_scaled, hlm

def load_plots(h, t, metadata):
    f_x_strain_test, f_y_strain_test, hlm = create_functions(h, t, metadata)
    """
    print(f_x_SPA_test(Mass, Distance))
    print(f_x_SPA_test(Mass, Distance)[0])
    print(f_x_SPA_test(Mass, Distance)[1])
    print(len(f_x_SPA_test(Mass, Distance)))
    print(len(f_y_SPA_test(Mass, Distance)))
    print(len(f_x_strain_test(Mass, Distance)))
    print(len(f_y_strain_test(Mass, Distance)))
    """
    return f_x_strain_test, f_y_strain_test, hlm
    
def iplt_lm(xStrain, yStrain, hlm, Mass, Distance):
    mscale = (Mass*1.989e+30)/M
    dscale = (Distance*3.086e+22)/r
    f_x_strain = xStrain/mscale
    f_y_strain = mscale**(3/2) * yStrain / dscale
    
    fig = go.Figure()
    for i in range(len(f_x_strain)):
        fig.add_trace(go.Scatter(x=f_x_strain[i], y=f_y_strain[i],
                         line=dict(color='royalblue', width=1),
                         name=f"{hlm[i]}"))
        fig.add_annotation(x=math.log10(f_x_strain[i][0]), y=math.log10(f_y_strain[i][0]),
            text=f"{hlm[i]}",
            showarrow=True,
            xshift=-5,
            font=dict(
                color="mediumvioletred"
            )
        )
        #print(i)

    # Edit the layout
    fig.update_layout(
        title=dict(
            text='CE vs aLIGO comparison'
        ),
        xaxis=dict(
            range=[np.log10(3), np.log10(5e3)],
            title=dict(
                 text='frequency'
            )
        ),
        xaxis_type="log",
        yaxis=dict(
            range=[np.log10(1e-25), np.log10(5e-21)],
            title=dict(
                text='amplitude'
             ),
        ),
        yaxis_type="log"
    )
    return fig