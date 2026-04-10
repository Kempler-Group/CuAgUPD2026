# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 16:30:02 2025

@author: stern
"""



import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

from scipy import interpolate
from scipy.optimize import curve_fit
from matplotlib.ticker import MaxNLocator

import os
SMALL_SIZE = 10
MEDIUM_SIZE = 10
BIGGER_SIZE = 10
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
plt.rcParams["font.family"] = "Arial" #MESS WITH THIS
plt.rcParams["mathtext.default"] = "regular"  # MAKES ITALICS NORMAL
plt.rcParams["xtick.major.size"] = 6
plt.rcParams["ytick.major.size"] = 6
plt.rcParams["legend.loc"] =  'upper left' 
lw = 10 #line width

a ="Ti2p Scan"
b ='O1s Scan'
c ='C1s Scan'
d ='Au4f Scan'
e = 'Ag3d Scan'

sample_1a = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XPS\Stern - XPS\Sample 3 - sample 2 with 20 min cycling\High resolution_Post sputter.xlsx", sheet_name = a )
sample_1b = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XPS\Stern - XPS\Sample 3 - sample 2 with 20 min cycling\High resolution_Post sputter.xlsx", sheet_name = b )
sample_1c = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XPS\Stern - XPS\Sample 3 - sample 2 with 20 min cycling\High resolution_Post sputter.xlsx", sheet_name = c )
sample_1d = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XPS\Stern - XPS\Sample 3 - sample 2 with 20 min cycling\High resolution_Post sputter.xlsx", sheet_name = d )
sample_1e = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XPS\Stern - XPS\Sample 3 - sample 2 with 20 min cycling\High resolution_Post sputter.xlsx", sheet_name = e )

# Ann2 = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XRD\xrd\annealed.xlsx")
# UnAnn = pd.read_excel(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\XRD\Au Films\XRD\UnAnnealed Au film.xlsx")

# Ann['intensity'] = Ann['intensity'] #- sum(Ann['intensity'])/len(Ann['intensity'])
# UnAnn['intensity'] = (UnAnn['intensity'] - min(UnAnn['intensity']))/6#- sum(UnAnn['intensity'])/len(UnAnn['intensity'])

# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# pd.set_option('display.max_colwidth', -1)

# # print (Ann)
# print(sample_1a['eV'])
# print(sample_1a['Counts / s'])
# # print(UnAnn)

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(6, 1.7))#, sharey=True)
plt.subplots_adjust( top=0.775, bottom=0.215, left=0.06, right=0.985, hspace=0.2, wspace=0.15)
ax1.tick_params(axis='both',which='both',direction='in')
ax2.tick_params(axis='both',which='both',direction='in')
ax3.tick_params(axis='both',which='both',direction='in')
ax4.tick_params(axis='both',which='both',direction='in')
ax5.tick_params(axis='both',which='both',direction='in')



ax1.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
ax3.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
ax4.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
ax5.ticklabel_format(axis='y', style='sci', scilimits=(0,0))


ax1.set_ylabel("counts")
# ax1.set_xlabel("Binding Energy (eV)")
ax3.set_xlabel("Binding Energy (eV)")

ax1.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
# ax1.set_yscale("log")

col = "#fd2084"

#Gold
ax5.set_title(d)
ax5.plot(sample_1d['eV'], sample_1d['Counts / s']-sample_1d['bkg Counts / s'], color = col)
ax5.set_xlim( 93, 80)

#Carbon
ax4.set_title(c)
ax4.plot(sample_1c['eV'], sample_1c['Counts / s']-sample_1c['bkg Counts / s'], color = col)
ax4.set_xlim(293, 283)
ax4.set_ylim(-100, 9e3)

#Silver
ax3.set_title(e)
ax3.plot(sample_1e['eV'], sample_1e['Counts / s']-sample_1e['bkg Counts / s'], color = col)
ax3.set_xlim(378, 364)
ax3.set_ylim(-4e1, 4e4)

#Titanium
ax2.set_title(a)
ax2.plot(sample_1a['eV'], sample_1a['Counts / s']-sample_1a['bkg Counts / s'], color = col)
ax2.set_xlim( 469, 456)

#Oxygen
ax1.set_title(b)
ax1.plot(sample_1b['eV'], sample_1b['Counts / s']-sample_1b['bkg Counts / s'], color = col)
ax1.set_xlim( 534.3, 524.5)


# ax6 = ax5.twinx()
# s2 = np.sin(2*np.pi*t)
# ax2.plot(t, s2, 'r.')
# ax6.set_ylabel("counts")

# ax6.tick_params()




##
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(2.5, 1.7), sharey=True)
plt.subplots_adjust( top=0.775, bottom=0.215, left=0.175, right=0.965, hspace=0.2, wspace=0.05)
ax1.tick_params(axis='both',which='both',direction='in')
ax2.tick_params(axis='both',which='both',direction='in')


ax1.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
# ax2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

ax1.set_ylabel("counts/norm")
# ax1.set_xlabel("Binding Energy (eV)")
ax1.set_xlabel("                 Binding Energy (eV)")

# ax1.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
# ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
# ax1.set_yscale("log")

# col = "black"

#Gold
Au = sample_1d['Counts / s']-sample_1d['bkg Counts / s']
# print(max(Au))
ax2.set_title(d)
ax2.plot(sample_1d['eV'], Au/max(Au), color = col)
ax2.set_xlim(93, 79.5)

ticks = (90, 85, 80)
labs = ('90', '', '80')
plt.xticks(ticks, labs)


#Silver
Ag = sample_1e['Counts / s']- sample_1e['bkg Counts / s']
print(max(Ag))
ax1.set_title(e)
ax1.plot(sample_1e['eV'], Ag/(max(Ag)) , color = col)
ax1.set_xlim( 378, 364)
# ax2.set_ylim(-4e1, 4e4)

###











# ax5.xaxis.set_major_locator(MaxNLocator(integer=True))

# Some example data to display
# x = np.linspace(0, 2 * np.pi, 400)
# y = np.sin(x ** 2)

# fig, axs = plt.subplots(1, 4)
# axs[0, 0].plot(sample_1a['eV'], sample_1a['Counts / s'])
# # axs[0, 0].set_title('Axis [0, 0]')
# axs[0, 1].plot(sample_1b['eV'], sample_1b['Counts / s'], 'tab:orange')
# # axs[0, 1].set_title('Axis [0, 1]')
# # axs[0, 2].plot(x, -y, 'tab:green')
# # axs[0, 2].set_title('Axis [1, 0]')
# # axs[0, 3].plot(x, -y, 'tab:red')
# # axs[0, 3].set_title('Axis [1, 1]')


# print('done!')


