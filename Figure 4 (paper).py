# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 11:32:24 2025

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
plt.rcParams["legend.loc"] =  'lower right' 
lw = 10 #line width



# print(len(library[0]))
#print(library[1][0.02])
concentrations = [ 0.001, 0.003, 0.01] # Molar, the concentrations of the  Cu in the solutions  0.0001, 0.0003,
#concentrations = [ 0.0001, 0.001, 0.01] # Molar, the concentrations of the  Cu in the solutions  0.0001, 0.0003,
rxn_ord = []
coverages = []
error_min = []
error_max = []
# plt.figure(figsize=(6,7))
# plt.subplots_adjust( top=0.965, bottom=0.135, left=0.235, right=0.98, hspace=0.2, wspace=0.2)
# plt.tick_params(axis='both',which='both',direction='in')
# "10 mM $\mathregular{Cu^{2+}}$" label = "1 mM $\mathregular{Cu^{2+}}$"



des_cov = 0.05

ag = "dodgerblue"
cu = "#ff5245"
cuHSA = "#B16DA6"

# plt.figure(figsize=(6,6))

fig, ax =plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('none') 
ax.set_facecolor((0, 0, 0, 0))  # Slightly transparent axes background

plt.subplots_adjust( top=0.98, bottom=0.18, left=0.215, right=0.98, hspace=0.2, wspace=0.2)
plt.tick_params(axis='both',which='both',direction='in')


# Cu in 0.1 M PCA
Cu_p1 = [3.52,  9.2683, 34.387] #the exchgange frequcny/rate for the coverage youre itterating through
Cu_p1_err = [1.125, 2.54, 17.9]

# Cu in 1 M PCA
Cu_1 = [5.2, 14.237, 72.7] #the exchgange frequcny/rate for the coverage youre itterating through
Cu_1_err = [2.6, 1.58,21.7]

# Ag in 0.1 M PCA
Ag_p1 = [28.86 ,56.98, 173.21] #the exchgange frequcny/rate for the coverage youre itterating through
Ag_p1_err = [8.26, 9.827, 12.68]

# Ag in 1 M PCA
Ag_1 = [30.278, 129.89, 468.47] #the exchgange frequcny/rate for the coverage youre itterating through
Ag_1_err = [2.27, 19.94, 99.35]



# Cu in 1 M HSA
Cu_1HSA = [7.674, 113.18, 298.053] #the exchgange frequcny/rate for the coverage youre itterating through
Cu_1_HSAerr = [1.15, 11.18, 38.45]
concs_HSA = [ 0.001, 0.01, 0.1]

# Cu in 1 M HSA
Cu_p1HSA = [10.536, 62.989] #the exchgange frequcny/rate for the coverage youre itterating through
Cu_p1_HSAerr = [2.1761, 9.81]
concs_p1HSA = [ 0.001, 0.01]




def fit_display(given_freq, concentrations, color):
    log_freq = np.log10(given_freq)
    log_conc =  np.log10(concentrations)
    fit_params, cov = np.polyfit(log_conc, log_freq, 1, cov=True)
    err = np.sqrt(cov[0][0])#np.sqrt(np.diag(cov))
    print("the error in the fit of", fit_params[0], "is", err)
    # print(sum(error[0]))
    def func (params, x):
        m, b = params
        #x = np.log(x)
        return 10**b * (x**m)  #np.exp(m*x+b)
    
    x1 = np.linspace(min(concentrations), max(concentrations), 10000) #for plotting the fit
    fit = func(fit_params, x1)
    plt.plot(x1, fit, color = color)
    return fit_params
#coverages.append(covs[j])   
    # print(rates[covs[1]])
    # print(covs[1])
#print(given_freq)
# log_freq = np.log10(given_freq)
# log_conc =  np.log10(concentrations)

#plt.plot(concentrations, given_freq, 'o', color =  "#ff5245",  markersize = 10, alpha = 0.5)
#print(errors)

slope_cu = "$\mathit{m}_\mathrm{Cu}$"
slope_ag = "$\mathit{m}_\mathrm{Ag}$"

# K_o = '$\mathit{r}_\mathrm{0}$'
# # r0 = '$\mathit{r}_\mathrm{0}$'
# M = '[$\mathregular{M^{n+}}$]'
# d = '$\mathit{∂}$'
# slope = '$\mathit{d} $\mathit{r}_\mathrm{0}$'

# test = r'$\frac{\mathit{∂}log[\mathit{r}_\mathrm{0}]}{\mathit{∂}log[\mathregular{M^{n+}}]}$'
# rxn_ord = f"{test} = {m[0]:.2g}"
# plt.text(0.05, 0.35, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= ag, verticalalignment='top')


# PCA_conc = 0.1

# plt.errorbar(concentrations, Ag_p1, yerr = Ag_p1_err, fmt="o", color =  ag, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10, label = "$\mathregular{Ag^{+}}$")
# m = fit_display(Ag_p1, concentrations, ag)
# rxn_ord = f"{slope_ag} = {m[0]:.2g}"
# plt.text(0.1, 0.23, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= ag, verticalalignment='top')

# plt.errorbar(concentrations, Cu_p1, yerr = Cu_p1_err, fmt="o", color =  cu, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10, label = "$\mathregular{Cu^{2+}}$")
# m = fit_display(Cu_p1, concentrations, cu )
# rxn_ord = f"{slope_cu} = {m[0]:.2g}"
# plt.text(0.1, 0.13, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= cu, verticalalignment='top')


PCA_conc = 1
plt.errorbar(concentrations, Ag_1, yerr = Ag_1_err, fmt="o", color =  ag, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10, label = "$\mathregular{Ag^{+}}$")
m = fit_display(Ag_1, concentrations, ag)
rxn_ord = f"{slope_ag} = {m[0]:.2g}"
plt.text(0.1, 0.23, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= ag, verticalalignment='top')

plt.errorbar(concentrations, Cu_1, yerr = Cu_1_err, fmt="o", color =  cu, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10, label = "$\mathregular{Cu^{2+}}$")
m = fit_display(Cu_1, concentrations, cu )
rxn_ord = f"{slope_cu} = {m[0]:.2g}"
plt.text(0.1, 0.13, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= cu, verticalalignment='top')

## polyfit(Xdata, Ydata, degree of fitting polynomila, lin = 1)

# """ sulfuric acid
# """
# PCA_conc = 1
# plt.errorbar(concs_HSA, Cu_1HSA, yerr = Cu_1_HSAerr, fmt="o", color =  cuHSA, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10, label = "$\mathregular{Cu^{2+}}$")
# m = fit_display(Cu_1HSA, concs_HSA, cuHSA )
# rxn_ord = f"{slope_cu} = {m[0]:.2g}"
# plt.text(0.1, 0.13, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= cuHSA, verticalalignment='top')

# PCA_conc = 0.1
# plt.errorbar(concs_p1HSA, Cu_p1HSA, yerr = Cu_p1_HSAerr, fmt="o", color =  cuHSA, alpha = 0.5, markersize = 10, elinewidth = 2, capsize = 10, label = "$\mathregular{Cu^{2+}}$")
# m = fit_display(Cu_p1HSA, concs_p1HSA, cuHSA )
# rxn_ord = f"{slope_cu} = {m[0]:.2g}"
# plt.text(0.1, 0.13, rxn_ord, transform=plt.gca().transAxes, fontsize=24, color= cuHSA, verticalalignment='top')



plt.yscale('log')
plt.xscale('log')

plt.ylabel('$\mathit{r}_\mathrm{0}$ (s$^\mathrm{-1}$)')
plt.xlabel('[ $\mathregular{ T^{n+}}$] (M)') #$\mathit{j}$

plt.ylim([1e-2, 25e+2])
plt.xlim([5e-4, 0.025])

# plt.xlim([5e-4, 0.15]) #for hsa
# plt.ylim([1e0, 25e+2]) #for hsa

# print(error[0][0])

# print(fit_params[0])

# rxn_ord = f" Slope = {fit_params[0]:.2g}"
theta = "$\mathit{\\theta}_\mathrm{M}$"
coverage_str = f" {theta} = {des_cov:.2g}"
PCA = "Cl$O_{4}$$\mathregular{^{-}}$" #"$\mathregular{HClO^{-}}$" [Cl$O_{4}$$\mathregular{^{-}}$] (M)
# PCA = "S$O_{4}$$\mathregular{^{2-}}$" #"$\mathregular{HClO^{-}}$" [Cl$O_{4}$$\mathregular{^{-}}$] (M)
PCA2 = "$\mathregular{^{-}}$"
#PCA_c = f"{PCA_conc} M {PCA}{PCA2}"
PCA_c = f"{PCA_conc} M {PCA}"


plt.text(0.025, 0.95, coverage_str, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
plt.text(0.04, 0.85, PCA_c, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
# plt.text(0.63, 0.1, rxn_ord, transform=plt.gca().transAxes, fontsize=20, color='black', verticalalignment='top')

#fit params = (slope, intercept)
#error_min.append(error[0][0]) #appends errror in slope
#error_max.append(error[0][1])
#rxn_ord.append(fit_params[0])
plt.legend( )#frameon= False)
plt.show()






