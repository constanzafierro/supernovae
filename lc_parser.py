import numpy as np
import pandas as pd
from os.path import join
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import re

def read_snpcc_lc(fname, data_path):
    start_line = 0
    # Read data from header, is there a nicer way?
    with open(join(data_path, fname)) as f:
        for line in f:
            s=re.findall('SNTYPE:\s*([-+]?\d+)', line)
            if s:
                sn_class_snpcc = int(s[0])
            s=re.findall('HOST_GALAXY_PHOTO-Z:\s*(\d+\.\d+)', line)
            if s:
                photo_z = float(s[0])
            s=re.findall('SN Type = (\w+) ,', line)
            if s:
                sn_class = s[0]
            s=re.search('VARLIST:', line)
            if s:
                break
            start_line += 1
    # Read light curve data
    try:
        df = pd.read_table(join(data_path, fname), skiprows=start_line, delim_whitespace=True)
    except:
        print(fname)
    bands=['g', 'r', 'i', 'z']
    lc = list()
    for i in range(0, len(bands)):
        #tmp = df.query("FLT=='"+str(bands[i])+"' and SNR>0.0").ix[:, ["MJD","FLUXCAL", "FLUXCALERR"]]
        tmp = df.query("FLT=='"+str(bands[i])+"'").ix[:, ["MJD","FLUXCAL", "FLUXCALERR"]]
        tmp = tmp.astype(float).as_matrix()
        lc.append(tmp)
    return lc, photo_z, sn_class, sn_class_snpcc

def plot_snpcc_lc(lc):
    bands=['g', 'r', 'i', 'z']
    colors=['g', 'r', 'm', 'k']
    fig = plt.figure(figsize=(8, 4), dpi=80)
    gs = gridspec.GridSpec(2, 2)
    for i in range(0, len(bands)):
        ax = plt.subplot(gs[i])
        ax.set_title(bands[i])
        ax.errorbar(lc[i][:, 0], lc[i][:, 1], yerr=lc[i][:, 2], color=colors[i], linewidth=1, fmt='.')
        ax.set_xlabel('MJD')
        ax.set_ylabel('FLUX')
        plt.grid()
    gs.tight_layout(fig, pad=0.1)
    