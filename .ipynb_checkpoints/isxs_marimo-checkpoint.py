import math
import numpy as np
import csv
import bilby
import re
import plotly.graph_objects as go
import marimo as mo
from IPython.display import display
import plotly.io as pio
pio.renderers.default = 'iframe'

G = 6.67430e-11
c = 3e8
M = 6.563e+31
r = 3.086e24


"""
Creating the noise curves
"""
ce = bilby.gw.detector.psd.PowerSpectralDensity(psd_file = 'CE_psd.txt', asd_file = 'CE_wb_asd.txt')
ligo_o4 = bilby.gw.detector.psd.PowerSpectralDensity(asd_file = 'aLIGO_O4_high_asd.txt')

ce_asd_file = open(ce.asd_file, "r")
ce_asd = ce_asd_file.readlines()
ce_asd_file.close()
ce_asd_amplitude = []; ce_asd_frequency = []
for i in ce_asd:
    split_line = re.split(" |\n", i)
    ce_asd_amplitude.append(float(split_line[0]))
    ce_asd_frequency.append(float(split_line[1]))
#print(ce_asd_frequency)

ligo_o4_asd_file = open(ligo_o4.asd_file, "r")
ligo_o4_asd = ligo_o4_asd_file.readlines()
ligo_o4_asd_file.close()
ligo_o4_asd_amplitude = []; ligo_o4_asd_frequency = []
for i in ligo_o4_asd:
    split_line = re.split(" |\n", i)
    ligo_o4_asd_amplitude.append(float(split_line[0]))
    ligo_o4_asd_frequency.append(float(split_line[1]))
#print(ligo_o4_asd_frequency)

def load_data():
    """
    loads the data of the included strains
    returns array of lm modes, array of h ids, nested arrays of htilde and frequencies, and array of metadatas
    """
    file = np.load("marimo_data.npz", allow_pickle=True)
    data = file['arr_0']
    hlm = data[0]
    h_id_list = []
    strain_data = []
    metadata_list = []
    for strain in data[1:]:
        h_id_list.append(strain[0])
        strain_data.append(strain[1:3])
        metadata_list.append(strain[3])
    
    return hlm, h_id_list, strain_data, metadata_list

def load_index(h_id_list , h_id):
    """
    returns the id of corresponding strain
    """
    return find_index(h_id_list, h_id)


def load_plots(strain_data, h_id_index):
    """
    returns the htilde strain and frequency arrays of corresponding h_id
    """
    strain = strain_data[h_id_index]
    frequencies = strain[0]
    htilde = strain[1]
    return frequencies, htilde
    
def find_index(data, value):
    try:
        idx = data.index(value)
    except ValueError:
        print(f"{value} is not a supported strain")
    return idx

def iplt_lm(xStrain, yStrain, hlm, Mass, Distance):
    mscale = (Mass*1.989e+30)/M
    dscale = (Distance*3.086e+22)/r
    f_x_strain = xStrain/mscale
    f_y_strain = mscale**(3/2) * yStrain / dscale
    
    fig = go.Figure()
    for i in range(len(f_x_strain)):
        fig.add_trace(go.Scatter(x=f_x_strain[i], y=f_y_strain[i],
                         line=dict(color='royalblue', width=1),
                         name=f"({hlm[i][0]}, {hlm[i][1]})"))
        fig.add_annotation(x=math.log10(f_x_strain[i][0]), y=math.log10(f_y_strain[i][0]),
            text=f"({hlm[i][0]}, {hlm[i][1]})",
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
                 text='frequency / Hz'
            )
        ),
        xaxis_type="log",
        yaxis=dict(
            range=[np.log10(1e-25), np.log10(5e-21)],
            title=dict(
                text=r'$ \mathrm{amplitude\ / \ } (Hz^{-1})^{1/2} $'
             ),
        ),
        yaxis_type="log"
    )
    return fig

def make_markdown(metadata_list, dropdown, idx):
    line1 = mo.md(f"""<h1 style="font-size: 24px;">{dropdown.value} Metadata Info:</h1>""")
    line3 = mo.md(
        f"""
        n orbits: {metadata_list[idx][1][0]:.3g}  
        mass ratio: {metadata_list[idx][1][1]:.3g}  
        eccentricity: {metadata_list[idx][1][2]:.3g}  
        chi1: {metadata_list[idx][1][3]}  
        chi2: {metadata_list[idx][1][4]}  
        chi1_perp: {metadata_list[idx][1][5]:.3g}  
        chi2_perp: {metadata_list[idx][1][6]:.3g}
        """
    )
    markdown = mo.vstack([line1, mo.md("-----------"), line3])
    return markdown
    
def run(h_id, h_id_list, strain_data, metadata_list, hlm, Mass, Distance, dropdown):
    dropdown
    h_idx = load_index(h_id_list, h_id)
    freq, htilde = load_plots(strain_data, h_idx)
    fig = iplt_lm(freq, htilde, hlm, Mass.value, Distance.value)
    fig.add_trace(go.Scatter(x=ce_asd_amplitude, y=ce_asd_frequency,
                         line=dict(color='orange', width=2),
                         name="CE Noise Curve"))
    fig.add_trace(go.Scatter(x=ligo_o4_asd_amplitude, y=ligo_o4_asd_frequency,
                         line=dict(color='orchid', width=2),
                         name="aLIGO Noise Curve"))
    markdown = make_markdown(metadata_list, dropdown, h_idx)
    plot = mo.vstack([dropdown, mo.md("-----------------------------"), Distance, Mass, fig, markdown])
    plot 
    
    return plot