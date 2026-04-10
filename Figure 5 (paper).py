# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 16:10:44 2025

@author: stern
"""


import matplotlib.pyplot as plt
import numpy as np
import math
SMALL_SIZE = 24
MEDIUM_SIZE = 24
BIGGER_SIZE = 24
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
lw = 10 #line width



# print(len(library[0]))
#print(library[1][0.02])
# concentrations = [ 0.001, 0.003, 0.01] # Molar, the concentrations of the  Cu in the solutions  0.0001, 0.0003,
#concentrations = [ 0.0001, 0.001, 0.01] # Molar, the concentrations of the  Cu in the solutions  0.0001, 0.0003,
rxn_ord = []
coverages = []
error_min = []
error_max = []
# plt.figure(figsize=(6,7))
# plt.subplots_adjust( top=0.965, bottom=0.135, left=0.235, right=0.98, hspace=0.2, wspace=0.2)
# plt.tick_params(axis='both',which='both',direction='in')
# "10 mM $\mathregular{Cu^{2+}}$" label = "1 mM $\mathregular{Cu^{2+}}$"

# PCA_conc = 0.1

des_cov = 0.05

c1 = "#B16DA6"
c = "#ff5245"

# plt.figure(figsize=(6,6))

fig, ax =plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('none') 
ax.set_facecolor((0, 0, 0, 0))  # Slightly transparent axes background

plt.subplots_adjust( top=0.975, bottom=0.175, left=0.215, right=0.98, hspace=0.2, wspace=0.2)
plt.tick_params(axis='both',which='both',direction='in')


# # Cu in 0.1 M PCA
# given_freq = [3.52,45.5,76] #the exchgange frequcny/rate for the coverage youre itterating through
# errors = [1.125,2.665,47.3]

# Cu in 1 M PCA
# given_freq = [6.88,48.8,72.7] #the exchgange frequcny/rate for the coverage youre itterating through
# errors = [1.77,4.07,21.7]

# # Ag in 0.1 M PCA
# given_freq = [22.8,62.123,179.22] #the exchgange frequcny/rate for the coverage youre itterating through
# errors = [11.05,6.77,14.69]

# # Ag in 1 M PCA
# given_freq = [32.37,131,468.47] #the exchgange frequcny/rate for the coverage youre itterating through
# errors = [1.83,20.12,103.1]

# HClO4 in 1 mM Cu

PCA_conc = 0.001
given_freq = [1.2, 3.52, 5.2, 12.86] #the exchgange frequcny/rate for the coverage youre itterating through
errors = [0.472, 1.125, 2.6, 1.42]
concentrations = [ 0.01, 0.1, 1, 10]

log_freq = np.log10(given_freq)
log_conc =  np.log10(concentrations)


given_freq_HSA = [6.124, 10.536, 7.674]#, 7] #the exchgange frequcny/rate for the coverage youre itterating through
errors_HSA = [1.8285, 2.1761, 1.15]#, 1]
concentrations_HSA = [ 0.01, 0.1, 1]#, 10]

log_freq2 = np.log10(given_freq_HSA)
log_conc2 =  np.log10(concentrations_HSA)

# given_freq_HSA2 = [60, 80, 140] #the exchgange frequcny/rate for the coverage youre itterating through
# errors_HSA2 = [0, 0, 0]
# concentrations_HSA2 = [ 0.1, 1, 10]

# log_freq3 = np.log10(given_freq_HSA2)
# log_conc3 =  np.log10(concentrations_HSA2)


#coverages.append(covs[j])   
    # print(rates[covs[1]])
    # print(covs[1])
#print(given_freq)

#plt.plot(concentrations, given_freq, 'o', color =  "#ff5245",  markersize = 10, alpha = 0.5)
#print(errors)
plt.errorbar(concentrations, given_freq, yerr = errors, fmt="o", color =  c, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10)


plt.errorbar(concentrations_HSA, given_freq_HSA, yerr = errors_HSA, fmt="o", color =  c1, alpha = 0.7, markersize = 10, elinewidth = 2, capsize = 10)
# plt.errorbar(concentrations_HSA2, given_freq_HSA2, yerr = errors_HSA2, fmt="o", color =  "maroon", alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10)
### polyfit(Xdata, Ydata, degree of fitting polynomila, lin = 1)

fit_params, error = np.polyfit(log_conc, log_freq, 1, cov=True)

fit_params2, error2 = np.polyfit(log_conc2, log_freq2, 1, cov=True)

# fit_params3, error3 = np.polyfit(log_conc3, log_freq3, 1, cov=True)

def func (params, x):
    m, b = params
    #x = np.log(x)
    return 10**b * (x**m)  #np.exp(m*x+b)

x1 = np.linspace(min(concentrations), max(concentrations), 10000) #for plotting the fit
fit = func(fit_params, x1)
plt.plot(x1, fit, "grey")


# 1 mM Cu HSA
x1 = np.linspace(min(concentrations_HSA), max(concentrations_HSA), 10000) #for plotting the fit
fit = func(fit_params2, x1)
plt.plot(x1, fit, "grey")

# 10 mM Cu HSA
# x1 = np.linspace(min(concentrations_HSA2), max(concentrations_HSA2), 10000) #for plotting the fit
# fit = func(fit_params3, x1)
# plt.plot(x1, fit, "grey")

plt.yscale('log')
plt.xscale('log')

plt.ylabel('$\mathit{r}_\mathrm{0}$ (s$^\mathrm{-1}$)')
plt.xlabel('[A] (M)') #$\mathit{j}$ [Cl$O_{4}$$\mathregular{^{-}}$]
# plt.xlabel('[$\mathregular{Cu^{2+}}$] (M)')
# plt.xlabel('[$\mathregular{Ag^{+}}$] (M)')

# plt.ylim([5e-1, 10e+2])
# plt.xlim([5e-4, 0.025])

plt.ylim([1e-1, 25e+1])
plt.xlim([5e-3, 25])

print(error[0][0])

print(fit_params[0])


slope_PCA = "$\mathit{m}_\mathrm{ClO_{4}\mathregular{^{-}}}$"
slope_HSA = "$\mathit{m}_\mathrm{SO_{4}\mathregular{^{2-}}}$"

rxn_ord = f" {slope_PCA} = {fit_params[0]:.2g}"


theta = "$\mathit{\\theta}_\mathrm{Cu}$"
coverage_str = f" {theta} = {des_cov:.2g}"
PCA = "Cl$O_{4}$$\mathregular{^{-}}$" #"$\mathregular{HClO^{-}}$"
#PCA2 = "$\mathregular{Cu^{2+}}$"
PCA2 = "$\mathregular{Cu^{2+}}$"
#PCA_c = f"{PCA_conc} M {PCA}{PCA2}"
PCA_c = f"{PCA_conc} M {PCA2}"


plt.text(0.025, 0.95, coverage_str, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
plt.text(0.04, 0.85, PCA_c, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
plt.text(0.43, 0.1, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color=c, verticalalignment='top')

rxn_ord = f" {slope_HSA} = {fit_params2[0]:.1g}"
plt.text(0.43, 0.2, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color=c1, verticalalignment='top')

# rxn_ord = f" Slope = {fit_params3[0]:.2g}"
# plt.text(0.53, 0.3, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')

#fit params = (slope, intercept)
#error_min.append(error[0][0]) #appends errror in slope
#error_max.append(error[0][1])
#rxn_ord.append(fit_params[0])
plt.show()






