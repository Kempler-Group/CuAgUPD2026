# -*- coding: utf-8 -*-
"""
Created on Tue May  6 10:23:02 2025

@author: stern
"""




import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.optimize import curve_fit
# import sys
# np.set_printoptions(threshold=sys.maxsize)

import os
### fo
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
plt.rcParams["legend.loc"] =  'upper right' 


cl = "black" # color of dots

electrode_area = 0.24 #cm^2
R =  42.4122 # resistance, 0 IF FULLY CORRECTED ON INSTRUMENT
comp = 0.15 # fractional %, iR compensation, if 85% on instrument, do remaining 15% here
Eoc = 0.035 # MSE V vs Erev

conc = 1 # mM conc
concentration = conc/1000 # Molar 10 mM = 0.010 M
#add visual aid for concentration

Emax = 0.56
#BLpoint = 0.45 ###baseline point
Emin = 0.45 #slightly highter than baseline to find the voltage closest to 0.36
bounds = (Emin, Emax)

Coverage = 0.05 # coverage you want to find the coverage at. 
#for strip 0p23 V dont go put in higher coverages bec it will just return the an error 

### Au site density can be back calculated from "ideal" Cu coverage, change for respective ions
TCD = 222e-6 #C/cm^2, Theortical Charge Density (site occupancy) Cu on Au(111) = 440e-6, Ag on Au(111) = 222e-6
N = 1 # elementary charge (n = 2 for Cu2+)
mol_Au = TCD / (N * 96485) # C/cm^2, n, C/mol, will need to change 440e-6 (Cu site cov)
# Would be better to derive this using lattice parameters
#print(mol_Au, "mol cm^(-2)")

# File loading with dictionary and scan rates
library =       {  # Dictionary to store DataFrames and scan rates, the scan rates are the keys to the file path
    25: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-25_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    50: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-50_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    100: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-100_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    250: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-250_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    1000: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-1000_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    # 2500: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-2500_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    10000: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-10000_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    # 25000: r"E:\Kempler\2026\april 2026\2026-04-08 1mM Ag-30mM K - 100pca - v3\LSV-25000_Au(#087)_Pt_Ag[1mM]_1-30-100_Ag-K-HSA_20260408_03_LSV_C02.mpt",
    # #... (rest of your paths)
    }




head=0
BaseLine_const = pd.read_csv(r"C:\Users\stern\OneDrive\Documents\School papers\Kempler Lab\data\Au(111)\HClO4\blanks\2025-04-24 100 mM PCA - BLANK\CV-50_Au(st#038)_Pt_MSE_100_PCA-BLANK_20250424_02_CV_C01.mpt", delimiter='\t', header=head)
BL_inf = { 'R':43.423, 'SA':0.162, 'Cycle':2, 'SR':50}



frames = {}  # Dictionary to store DataFrames, keyed by scan rate
for sr, file in library.items():
    try:
        df = pd.read_csv(file, delimiter='\t', header=head)
        frames[sr] = df  # Store the DataFrame with the scan rate as the key
    except FileNotFoundError:
        print(f"Error: File not found: {file}")
    except Exception as e:
        print(f"Error loading file {file}: {e}")

scan_rates = list(frames.keys()) # Extract scan rates from the dictionary keys
legend = [f"{sr/1000} V/s" for sr in scan_rates]  # Dynamic legend creation
cyclenum = [2] * len(frames)  #create a list of cycle numbers if needed
plotColors = ["#000000", "#300c18", "#640d31", "#920346", "#b9095a", "#de086e", "#fd2084", "#ff65a0", "#ff8eb6", "#ffaeca", "#ffcbdc", "#ffe5ed", "#ffffff"] #for coverage vs potential plot
# plotColors = ["#000000", "#1c0b0f", "#3e1923", "#5e2133", "#7e2642", "#9d2850", "#bb265d", "#d6276a", "#ec3177", "#f84d86", "#ff6996", "#ff86a9", "#ff9eba", "#ffb4c9", "#ffc8d7", "#ffdbe4", "#ffecf1", "#ffffff"]
# plotColors= [ "#000000", "#1e304b", "#265ba1", "#0080ff", "#0080ff"]
# plotColors =["#000000", "blue",  "dodgerblue", "deepskyblue","lightskyblue", "#e7ecfb",  "#000000", "blue",  "dodgerblue", "deepskyblue","lightskyblue", "#e7ecfb", "#ffffff"]


def get_BL(BaseLine, BL_inf):
    
    BaseLine = BaseLine[BaseLine['cycle number'] == BL_inf['Cycle']]
    BaseLine = BaseLine.iloc[round(len(BaseLine) / 2):].copy()  # Use .copy() to avoid SettingWithCopyWarning
    # Calculate current density (vectorized)
    BaseLine['<J>/A cm^-2'] = BaseLine['<I>/mA'] / (BL_inf['SA'] * 1000)
    #correct potetential to Erev
    BaseLine['Ewe/V'] = BaseLine['Ewe/V'] - Eoc
    # Correct potential for IR drop (vectorized)
    BaseLine['E_corr/V'] = BaseLine['Ewe/V'] - (BaseLine['<I>/mA'] / 1000) * BL_inf['R'] * comp
    # Trim BaseLine (vectorized)
    BaseLine = BaseLine[(BaseLine['E_corr/V'] < max(bounds)) & (BaseLine['E_corr/V'] > min(bounds))]
    BaseLine.reset_index(drop=True, inplace=True)
    BLpoint = BaseLine
    
    return BLpoint

BLpoint = get_BL(BaseLine_const, BL_inf)

C = Coverage #fractional
# Constants (define these outside the function if they are truly constant)
e = 1.60217663e-19  # C
kb = 1.380649e-23  # J K-1
T = 293.15  # K
#con = e / (2 * kb * T)  # V

alpha = 0.5
con = ( alpha * e) / (kb * T)  # V  alpha = 0.5 =  e / (2 * kb * T)  # V
con2 = ( (1-alpha) * e) / ( kb * T)  # V
a = C**(1-alpha) * (1 - C)**alpha # (C * (1 - C))**alpha 

def func(x, k):
    return (k * a) * -(np.exp(-(con2 * x)) - np.exp((con * x)))#eqn from suntivisch paper

def run_files(frames, plotColors, legend, scan_rates):  # Add scan_rates as a parameter
    '''
    function plots cov vs potential and returns the driving force and apparent rate constant for coverage =
    '''
    
    #gets the data for the slowest scan and then the last point in that scan (based on Emax) is what our expected coverage is for setting the reference
    sr_i = scan_rates[0]
    frame_i = frames[sr_i]

    cov1, pot1 = Adsorption_Data(frame_i, [Emin, Emax], electrode_area, sr_i, BLpoint)
    Expected_cov = cov1[-1] #C/cm^2, Theortical Charge Density (site occupancy) Cu on Au(111) = 440e-6, Ag on Au(111) = 220e-6, 1st peak in Ag is 60 uC/cm2

      
    
    pca_E = []  #driving force for rate extraction
    P_ks = [] #list of electroadsorption constant
    
    
    plt.figure(figsize=(6,6))
    plt.subplots_adjust( top=0.98, bottom=0.135, left=0.205, right=0.99, hspace=0.2, wspace=0.2)

    plt.xlabel('$\mathit{E}$ (V vs $E_\mathit{rev}$)')
    plt.ylabel('$\mathit{\\theta}_\mathrm{Ag}$')
    #plt.ylim(-0.005, 0.1)
    plt.tick_params(axis='both',which='both',direction='in')
    
    for i, sr in enumerate(scan_rates):  # Iterate through scan rates
        frame = frames[sr]  # Get the DataFrame using the scan rate as the key
        coverage, potential = Adsorption_Data(frame, [Emin, Emax], electrode_area, sr, BLpoint)  # Pass sr as scan rate
        coverage = Expected_cov - np.array(coverage) #for strip 0p23 V, gets actual cov based on amnt taken off surface
        plt.plot(potential, coverage, color=plotColors[i], label=legend[i], linewidth=2.5)

    for i, sr in enumerate(scan_rates):  # Iterate through scan rates
        frame = frames[sr]  # Get the DataFrame using the scan rate as the key
        coverage, potential = Adsorption_Data(frame, [Emin, Emax], electrode_area, sr, BLpoint)  # Pass sr as scan rate
        coverage = Expected_cov - np.array(coverage) #for strip 0p23 V, gets actual cov based on amnt taken off surface
        pca_E.append(find_coverage(coverage, potential, Coverage)) #will return an error if your coverage is higher than the expected coverage
        P_ks.append(lookup_k(frame, pca_E[i], electrode_area, Coverage, BLpoint, sr))

        
    #plt.legend()
    
    print(pca_E)                 
    print(P_ks)
    
    get_K_app(pca_E, P_ks, cl)




def get_K_app(pca_E, P_ks, cl):  # Pass Coverage and cl as arguments
    """Calculates and plots the apparent rate constant.

    Args:
        pca_E (list/np.ndarray): Driving forces.
        P_ks (list/np.ndarray): Rate constants.
        Coverage (float): Coverage value.
        cl (str): Color for the data points.
    """

    P_ksi = np.array(pca_E) - pca_E[0]  # Use NumPy for driving force calculation

    
    
    xData = P_ksi # driving force (greek letter ksi)
    yData = P_ks #apparant rate

    x1 = np.linspace(-0.1, 1, 10000)
    
    
    #curve fits takes 3 things and gives (look up) apparent rate const and error 
    popt, pcov = curve_fit(func, xData, yData, p0=[1])  # Provide an initial guess
    k_app = popt[0]  # Extract the k_app value
    err = pcov  # Keep the error matrix
    print('the apparent rate constant is: [', k_app, '] and the error is ', err) # Print k_app and error matrix
    print(C)

    fig, ax = plt.subplots(figsize=(5, 6))
    # fig.patch.set_facecolor('none')
    # ax.set_facecolor((0, 0, 0, 0))  # Slightly transparent axes background
    # plt.figure(figsize=(5, 6))
    plt.tick_params(axis='both', which='both', direction='in')
    plt.subplots_adjust(top=0.99, bottom=0.145, left=0.28, right=0.98, hspace=0.2, wspace=0.2)

    plt.plot(P_ksi, P_ks, 'o', color=cl, markersize=10, alpha= 0.5)#, markerfacecolor='none')
    plt.plot(x1, func(x1, k_app), color='black', linestyle = "solid")  # Use k_app directly
    plt.tick_params(axis='both', which='both', direction='in')
    plt.yscale('log')
    plt.ylim([5e-3, 5e+2])
    plt.xlim([-0.02, 0.115])

    plt.xlabel('$\mathit{\\xi}$ (V vs $E_{eq}$)')
    plt.ylabel('|$\mathit{r}_\mathrm{app}$| ($\mathregular{s^{-1}}$)')
    # Prepare the equations to display
    s = "$\mathregular{s^{-1}}$"
    K_o = '$\mathit{r}_\mathrm{0}$'
    K_app_str = f"{K_o} = {k_app:.2g} {s}"  # Formatted string for k_app
    theta = "$\mathit{\\theta}_\mathrm{Ag}$"
    coverage_str = f" {theta} = {C:.3f}"
    conc = f"C = {concentration*1000} mM "
    
    
    a_str = "\u03B1"
    alpha_factor = f"{a_str} = {alpha} "
    
    plt.text(0.45, 0.31, conc, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    plt.text(0.45, 0.25, alpha_factor, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    plt.text(0.42, 0.19, coverage_str, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    plt.text(0.45, 0.14, K_app_str, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    
    def func2(x, al):
        
        con = ( al * e) / ( kb * T)  # V
        con2 = ( (1-al) * e) / ( kb * T)  # V
        return (k_app * a) * -(np.exp(-(con2 * x)) - np.exp((con * x)))#eqn from suntivisch paper
    # plt.plot(x1, func2(x1, 0), color='grey', linestyle = "dotted")  # Use k_app directly
    # plt.plot(x1, func2(x1, 1), color='grey', linestyle = "dashed")  # Use k_app directly
    plt.show()


    
    """" plots the trace of what the rate would be at 5 times faster or slower"""
    #plt.plot(x1, func(x1, k_app+err[0]), color='grey', linestyle = "dashed", alpha = 0.5)  # Use k_app directly
    #plt.plot(x1, func(x1, k_app-err[0]), color='grey', linestyle = "dashed", alpha = 0.5)  # Use k_app directly
    
    
    
    
    plt.show()
    
    return k_app, err # Return k_app and err



def lookup_k(frame, potential, area, coverage, baseLine, scanRate):
    '''This function takes a frame and slices to the adsorption trace
    Then it finds the first value greater than the specified potential and converts
    the current measurement at this point to an apparent rate constant, for an assumed
    value of n (# of eletrons transfered)
    
    k is in units of s-1 and is normalized to the number of surface sites
    i = nFA * [k_ox(theta) - k_red(1-theta)] * theta*
    
    units only make sense if theta is in mol/cm^2
    '''
    
    """
    Calculates the apparent rate constant (k) at a given potential.

    Args:
        frame (pd.DataFrame): The DataFrame containing the CV data.
        potential (float): The target potential.
        area (float): Electrode area.
        coverage (float): Target coverage.
        baseLine (float): Baseline potential.
        cycle (int): Cycle number.
        N (int, optional): Number of electrons transferred. Defaults to 2.
        R (float, optional): Uncompensated resistance. Defaults to 0.
        mol_Au (float): Surface site density of gold.

    Returns:
        float: The apparent rate constant k, or None if the potential is not found.
    """

    if mol_Au is None:
        raise ValueError("mol_Au must be provided.")
        #i should make a function for this baseline correction portion
    #frame = frame[frame['cycle number'] == cycle]
    #frame = frame.iloc[round(len(frame) / 2):].copy()
    frame = frame.copy()
    frame['<J>/A cm^-2'] = frame['<I>/mA'] / (area * 1000)
    frame['E_corr/V'] = frame['Ewe/V'] - (frame['<I>/mA'] / 1000) * R * comp

    E = frame['E_corr/V'].values  # NumPy array for potential
    
    

    baseLine_c = baseLine.copy()
    baseLine_c['<J>/A cm^-2'] = baseLine_c['<J>/A cm^-2'] * (scanRate/(2* BL_inf['SR']))
    bL = baseLine_c['<J>/A cm^-2'].mean()  
    corrFrame_J = frame['<J>/A cm^-2'] - ( bL ) # NumPy array for corrected current

    # Find the *first* index where E < potential (swap to E > pot bec going anodically?)
    n_candidates = np.where(E > potential)[0]

    if n_candidates.size > 0:
        n = n_candidates[0]  # First index
        j = corrFrame_J[n]
        print('Current = ', j)
        k = abs(j) / (N * 96485 * (1 - coverage) * mol_Au)
        print('k_app = ', k)
        return k
    else:
        return None



def find_coverage(thetas, Es, coverage): #Q-list is thetas, E -> Es, and coverage is taarget cov (comparing accross scan rates)
   #Q_list is coverage, Es = corrected potential, target coverage (arb) 
    '''This function finds the potential for which a given target coverage is reached'''
    
    print('highst cov is:', thetas[0])
    x = thetas[0] - coverage
    y = thetas[-1]
    for n, theta in enumerate(thetas):
        if x < 0:
            raise ValueError(f"Target coverage '{coverage}' does not exist within the given coverage values, chose a LOWER coverage.")
        if coverage < y:
            raise ValueError(f"Target coverage '{coverage}' does not exist within the given coverage values, chose a HIGHER coverage or remove the scans that do not reach the desired coverage (may effect rate).")   
        
        if theta < coverage: #less than bec were decreasing in coverage
            print(Es.iloc[n])
            return Es.iloc[n]
        else:
            continue




def Adsorption_Data(frame, bounds, electrode_area, scanRate, baseLine):  # Added R as a parameter with default
    """
    Corrects data to a baseline and calculates adsorption coverage.

    Args:
        frame (pd.DataFrame): The DataFrame containing the CV data.
        bounds (list): The potential bounds for the adsorption region.
        electrode_area (float): The electrode area in cm^2.
        scanRate (float): The scan rate in V/s.
        baseLine (float): The baseline potential.
        cycle (int): The cycle number to analyze.
        TCD (float, optional): The normalization charge density. Defaults to 440e-6.
        R (float, optional): The uncompensated resistance. Defaults to 0.

    Returns:
        tuple: A tuple containing the list of adsorption coverages (Q_list) and the corrected potentials (E).
    """

    #frame = frame[frame['cycle number'] == 2]
    #frame = frame.iloc[round(len(frame) / 2):].copy()  # Use .copy() to avoid SettingWithCopyWarning

    # Calculate current density (vectorized)
    frame_copy = frame.copy()
    frame_copy['<J>/A cm^-2'] = frame_copy['<I>/mA'] / (electrode_area * 1000)

    # Correct potential for IR drop (vectorized)
    frame_copy['E_corr/V'] = frame_copy['Ewe/V'] - (frame_copy['<I>/mA'] / 1000) * R * comp

    # Trim frame_copy (vectorized)
    frame_copy = frame_copy[(frame_copy['E_corr/V'] < max(bounds)) & (frame_copy['E_corr/V'] > min(bounds))].copy()
    #frame_copy.reset_index(drop=True, inplace=True)

    E = frame_copy['E_corr/V']

    # Baseline correction (more efficient)
    # i0 = np.argmin(np.abs(E - baseLine))
    # i0min = max(0, i0 - 2)
    # i0max = min(len(frame_copy) - 1, i0 + 2)
    # baseLineArray = frame_copy.iloc[i0min:i0max]['<J>/A cm^-2']
    
    
    
    baseLine_c = baseLine.copy()
    #print(baseLine_c['<J>/A cm^-2'])
    
    baseLine_c['<J>/A cm^-2'] = baseLine_c['<J>/A cm^-2'] * (scanRate/(2* BL_inf['SR']))
    bL = baseLine_c['<J>/A cm^-2'].mean() 
    
    min_J =min(frame_copy['<J>/A cm^-2'])
    check = bL - min_J
    print("the cehck is", check)
    def check_bl(bl, min_j):
        if bl > min_j:
            corrFrame_J = frame_copy['<J>/A cm^-2'] - ( bL ) # NumPy array for corrected current
            
        else:
            corrFrame_J = frame_copy['<J>/A cm^-2'] - ( min_J )
        return corrFrame_J
    
    corrFrame_J = check_bl(bL, min_J)
    
    # corrFrame_J = frame_copy['<J>/A cm^-2'] - ( min_J )
    
    
    # def check_bl(bl, min_j):
    #     if bl > min_j:
    #         corrFrame_J = frame['<J>/A cm^-2'] - ( bL ) # NumPy array for corrected current
            
    #     else:
    #         corrFrame_J = frame['<J>/A cm^-2'] - ( min_J )
    #     return corrFrame_J
    
    # corrFrame_J = check_bl(bL, min_J)
    
    #print("the baseline current is", bL)
    # plt.figure()
    # plt.plot(E, corrFrame_J['<J>/A cm^-2'], color = 'black' )
    # plt.show()

    # Calculate adsorption coverage (Corrected and more efficient)
    Q_list = []
    Q = 0
    time = frame_copy['time/s'].values
    corrFrame_J_values = corrFrame_J.values
    #simpler/different intergration that doesnt use np.trapz
    for i in range(1, len(frame_copy)):
        dt = time[i] - time[i - 1] #time differenctiated over (1 second)
        #intergration (make box with hight J + J+1, and length dt, then divide to get trangle (trapaziod integration bec in a for-loop)
        Q += (corrFrame_J_values[i] + corrFrame_J_values[i - 1]) * dt / 2 
        adsorption = Q / TCD #normalize to coverage
        Q_list.append(adsorption)

    # E has one more element than Q_list, so we slice E to match
    E_matched = E.iloc[1:] # slice E to match the length of Q_list

    return Q_list, E_matched  # Return E_matched



run_files(frames, plotColors, legend, scan_rates)
