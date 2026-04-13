# -*- coding: utf-8 -*-
"""
Created on Tue May  6 10:35:35 2025

@author: stern
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate
from scipy.optimize import curve_fit
import os
### for plotting
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
plt.rcParams["legend.loc"] =  'lower left' 

###Start here 
colors = [ "navy", "blue", "dodgerblue", "skyblue", "lightblue"] # color of dots "black",
# colors = ["#952516", "#db1b0c",   "#ff5245",      "#ff948f"  ]
markers = ['o','^','s','v', 'o']

conc = xxx # mM conc
concentration = conc/1000 # Molar 10 mM = 0.010 M
#add visual aid for concentration


Eoc = xxx
electrode_areas = [ xxx, xxx,... ] #cm^2 
Rs = [ xxx, xxx,... ] # resistance, 0 IF CORRECTED ON INSTRUMENT  8.986,  8.973, 8.06823
comp = 0.15 # fractional %, iR compensation, if 85% on instrument, do remaining 15% here
#Eoc = 0.0685 # MSe V vs Erev

Emax = xxx #stop integrating
#BLpoint = 0.45 ###baseline point
Emin = xxx #start integrating
bounds = (Emin, Emax)


Coverage = 0.05 # coverage you want to find the coverage at. 
# #for stripping dont go put in higher coverages bec it will just return the an error 

### Au site density can be back calculated from "ideal" Cu coverage, change for respective ions
TCD = 222e-6 #C/cm^2, Theortical Charge Density (site occupancy) Cu on Au(111) = 440e-6, Ag on Au(111) = 222e-6
N = 1 # elementary charge (n = 2 for Cu2+)
mol_Au = TCD / (N * 96485) # C/cm^2, n, C/mol, will need to change 440e-6 (Cu site cov)
# Would be better to derive this using lattice parameters
#print(mol_Au, "mol cm^(-2)")
print(type(TCD))

# File loading with dictionary and scan rates
library = [
    {  # Dictionary to store DataFrames and scan rates, the scan rates are the keys to the file path  #highest cov for all is 10%
    scanrate: r"filepath.mpt"
    },
    {
    scanrate: r"filepath.mpt"
    },
    {
    scanrate: r"filepath.mpt"
    # #... (rest of your paths)
    },
    
    
    ]


##npt using but if you wanted to show the coverage vs potential plots it would get used
plotColors = ["#000000", "#300c18", "#640d31", "#920346", "#b9095a", "#de086e", "#fd2084", "#ff65a0", "#ff8eb6", "#ffaeca", "#ffcbdc", "#ffe5ed", "#ffffff"] #for coverage vs potential plot

head = 0
BaseLine_const = pd.read_csv(r"filepath.mpt", delimiter='\t', header=head)
BL_inf = { 'R':xxx, 'SA':xxx, 'Cycle':xxx, 'SR':xxx}





C = Coverage
# Constants (define these outside the function if they are truly constant)
e = 1.60217663e-19  # C
kb = 1.380649e-23  # J K-1
T = 298.15  # K
alpha = 0.5
con = ( alpha * e) / (kb * T)  # V  alpha = 0.5 =  e / (2 * kb * T)  # V
con2 = ( (1-alpha) * e) / ( kb * T)  # V
a = C**(1-alpha) * (1 - C)**alpha #(C * (1 - C))**alpha


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




def plt_avg_Ko(data_frame, electrode_areas, Rs, colors):
    

    #functon here to generate best fit line
    def func(x, k):
        return (k * a) * -(np.exp(-(con2 * x)) - np.exp((con * x)))#eqn from suntivisch paper
    
    x1 = np.linspace(0, 0.1, 10000) #for plotting the fit
    rates = [] #the k_o's for averaging
    errors = []
    
    #starting the plot

    fig, ax =plt.subplots(figsize=(5, 6))
    plt.subplots_adjust(top=0.965, bottom=0.135, left=0.275, right=0.98, hspace=0.2, wspace=0.2)

    
    # fig, ax =plt.subplots(figsize=(6, 7))
    # plt.subplots_adjust(top=0.965, bottom=0.135, left=0.235, right=0.98, hspace=0.2, wspace=0.2)
    # plt.tick_params(axis='both', which='both', direction='in')

    fig.patch.set_facecolor('none') 
    ax.set_facecolor((0, 0, 0, 0))  # Slightly transparent axes background
    

    plt.tick_params(axis='both', which='both', direction='in')
    # plt.subplots_adjust(top=0.99, bottom=0.145, left=0.28, right=0.98, hspace=0.2, wspace=0.2)
    plt.yscale('log')
    plt.ylim([5e-3, 5e+2])
    plt.xlim([-0.1, 0.1])
    plt.xlim([-0.01, 0.1])

    # plt.xlim([-0.10, 0.10])
    """iterates through each sub dictionary in the library, then for each data set (experimntal trial set)
        it get the driving force (P_ksi) and k_apparant (P_ks, from B-V kinetics) plots them, then calculates the exchnage frequency 
        that exchange frequency is then stored in 'rates = []' and averaged below and then used to plot the line of best fit """
    for i in range(len(data_frame)): #iterate through library, each set of data
        ###processing the data to usable form
        head=0
        frames = {}  # Dictionary to store DataFrames, keyed by scan rate
        for sr, file in data_frame[i].items():
            try:
                df = pd.read_csv(file, delimiter='\t', header=head)
                frames[sr] = df  # Store the DataFrame with the scan rate as the key
            except FileNotFoundError:
                print(f"Error: File not found: {file}")
            except Exception as e:
                print(f"Error loading file {file}: {e}")

        scan_rates = list(frames.keys()) # Extract scan rates from the dictionary keys
        legend = [f"{sr/1000} V/s" for sr in scan_rates]  # Dynamic legend creation
        cyclenum = [2] * len(data_frame[i])  # Create a list of cycle numbers if needed
        ###
        
        P_ksi, P_ks = get_X_Y(frames, plotColors, legend, scan_rates, electrode_areas[i], Rs[i])
        plt.plot(P_ksi, P_ks, markers[i], color=colors[i], markersize=10, alpha=0.65) #plotting each run, alpha is transparancy
        # plt.scatter(P_ksi, P_ks, s = 100 , marker = markers[i], c="none", edgecolors = colors[1]) #plotting each run, alpha is transparancy c='None', edgecolors='C1'
        k_app, err = get_K_app(P_ksi, P_ks, colors[i])
        
        rates.append(k_app)
        errors.append(err)
        
    k_avg = sum(rates)/len(rates)
    k_stdv = (sum([((x - k_avg) ** 2) for x in rates]) /len(rates))**0.5
    errs = [x**2 for x in errors]
    errs = sum(errs)/len(errors)**2
    err_prop = np.sqrt(errs)
    
    
    
    print('the apparent rate constant is: [', k_avg, '] ')#'and the error is ', errors) # Print k_app and error matrix
    print("the standard deviation is", k_stdv ," and the error propogation stdev is", err_prop)
    print(Coverage)
    print("rates = ", rates)
    print("errors = ", errors)
    
    
    plt.plot(x1, func(x1, k_avg), color='black', linestyle= "solid")  # Use k_app directly
    plt.tick_params(axis='both', which='both', direction='in')

    plt.xlabel('$\mathit{\\xi}$ (V vs $\mathit{E}_{eq}$)')
    plt.ylabel('|$\mathit{r}_\mathrm{app}$| ($\mathregular{s^{-1}}$)')
    # Prepare the equations to display
    s = "$\mathregular{s^{-1}}$"
    K_o = '$\mathit{r}_\mathrm{0}$'
    K_app_str = f"{K_o} = {k_avg:.2g} {s}"  # Formatted string for k_app
    theta = "$\mathit{\\theta}_\mathrm{Ag}$"
    coverage_str = f" {theta} = {Coverage}"
    conc = f"conc = {concentration*1000} mM "
    a_str = "\u03B1"
    alpha_factor = f"{a_str} = {alpha} "
    
    plt.text(0.35, 0.31, conc, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    plt.text(0.35, 0.25, alpha_factor, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    plt.text(0.32, 0.19, coverage_str, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    plt.text(0.35, 0.14, K_app_str, transform=plt.gca().transAxes, fontsize=24, color='black', verticalalignment='top')
    
    
    """" plots the trace of what the rate would be at 5 times faster or slower"""
    plt.plot(x1, func(x1, k_avg + k_stdv), color='grey', linestyle = "dashed", alpha = 0.3)  # Use k_app directly
    plt.plot(x1, func(x1, k_avg - k_stdv), color='grey', linestyle = "dashed", alpha = 0.3)  # Use k_app directly
    
    plt.show()

def get_X_Y(frames, plotColors, legend, scan_rates, electrode_area, R):  # Add scan_rates as a parameter
    '''
    function plots cov vs potential and returns the driving force and apparent rate constant for coverage = C
    '''
    sr_i = scan_rates[0]
    frame_i = frames[sr_i]
    
    #gets the data for the slowest scan and then the last point in that scan (based on Emax) is what our expected coverage is for setting the reference
    cov1, pot1 = Adsorption_Data(frame_i, [Emin, Emax], electrode_area, sr_i, R)
    #cov1, pot1 = Adsorption_Data(frames[scan_rates[0]], [Emin, Emax], electrode_area, scan_rates[0], BLpoint)


    Expected_cov = cov1[-1] #max(cov1) #C/cm^2, Theortical Charge Density (site occupancy) Cu on Au(111) = 440e-6, Ag on Au(111) = 220e-6, 1st peak in Ag is 60 uC/cm2
    print('highst cov is:', Expected_cov)
    #print(f"the expected cov is {Expected_cov}")
    
    
    pca_E = []  #driving force for rate extraction
    P_ks = [] #list of electroadsorption constant
    
    
    # plt.figure(figsize=(8,6))
    # plt.subplots_adjust( top=0.955, bottom=0.16, left=0.155, right=0.975, hspace=0.2, wspace=0.2)
    # plt.xlabel('$\mathit{E}$ (V vs $E_{rev}$)')
    # plt.ylabel('$\mathit{\\theta}_\mathrm{Cu}$')
    # plt.tick_params(axis='both',which='both',direction='in')
    
    for i, sr in enumerate(scan_rates):  # Iterate through scan rates
        frame = frames[sr]  # Get the DataFrame using the scan rate as the key
        coverage, potential = Adsorption_Data(frame, [Emin, Emax], electrode_area, sr,  R)  # Pass sr as scan rate
        coverage = Expected_cov - np.array(coverage) #for stripping, gets actual cov based on amnt taken off surface
        print('lowest cov is:', coverage[-1] * 100, '%')
        
        #plt.plot(potential, coverage, color=plotColors[i], label=legend[i])
        pca_E.append(find_coverage(coverage, potential, Coverage))
        P_ks.append(lookup_k(frame, pca_E[i], electrode_area, Coverage,  R, sr))
        
    #plt.legend()
    #plt.show()
    #print(pca_E)                 
    #print(P_ks)
    
    P_ksi = np.array(pca_E) - pca_E[0]  # Use NumPy for driving force calculation
    
    return P_ksi, P_ks
    #get_K_app(pca_E, P_ks, cl)


def get_K_app(P_ksi, P_ks, cl):  # Pass Coverage and cl as arguments
    """Calculates the apparent rate constant.

    Args:
        pca_E (list/np.ndarray): Driving forces.
        P_ks (list/np.ndarray): Rate constants.
        Coverage (float): Coverage value.
        cl (str): Color for the data points.
    """
    xData = P_ksi # driving force (greek letter ksi)
    yData = P_ks #apparant rate
    

    
    def func(x, k):
        return (k * a) * -(np.exp(-(con2 * x)) - np.exp((con * x)))#eqn from suntivisch paper
    
    #curve fits takes 3 things and gives (look up) apparent rate const and error 
    popt, pcov = curve_fit(func, xData, yData, p0=[1])  # Provide an initial guess
    k_app = popt[0]  # Extract the k_app value
    err = pcov  # Keep the error matrix

    return k_app, err # Return k_app and err



def lookup_k(frame, potential, area, coverage,  R, scanRate):
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
    

    baseLine = get_BL(BaseLine_const, BL_inf)
    baseLine_c = baseLine.copy()
    baseLine_c['<J>/A cm^-2'] = baseLine_c['<J>/A cm^-2'] * (scanRate/(2* BL_inf['SR']))
    bL = baseLine_c['<J>/A cm^-2'].mean()  
    corrFrame_J = frame['<J>/A cm^-2'] - ( bL ) # NumPy array for corrected current

    # Find the *first* index where E < potential (swap to E > pot bec going anodically?)
    n_candidates = np.where(E > potential)[0]

    if n_candidates.size > 0:
        n = n_candidates[0]  # First index
        j = corrFrame_J[n]
        #print('Current = ', j)
        k = abs(j) / ((N * 96485  * mol_Au) )#* (1 - coverage))
       # print('k_app = ', k)
        return k
    else:
        return None

def find_coverage(thetas, Es, coverage): #Q-list is thetas, E -> Es, and coverage is taarget cov (comparing accross scan rates)
   #Q_list is coverage, Es = corrected potential, target coverage (arb) 
    '''This function finds the potential for which a given target coverage is reached'''
    
    # print('highst cov is:', thetas[0])
    x = thetas[0] - coverage
    y = thetas[-1]
    for n, theta in enumerate(thetas):
        if x < 0:
            raise ValueError(f"Target coverage '{coverage}' does not exist within the given coverage values, chose a LOWER coverage.")
        if coverage < y:
            raise ValueError(f"Target coverage '{coverage}' does not exist within the given coverage values, chose a HIGHER coverage or remove the scans that do not reach the desired coverage (may effect rate).")   
        
        if theta < coverage: #less than bec were decreasing in coverage
            #print(Es.iloc[n])
            return Es.iloc[n]
        else:
            continue


def Adsorption_Data(frame, bounds, electrode_area, scanRate, R):  # Added R as a parameter with default
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
    frame = frame.copy()
    frame['<J>/A cm^-2'] = frame['<I>/mA'] / (electrode_area * 1000)
    # Correct potential for IR drop (vectorized)
    frame['E_corr/V'] = frame['Ewe/V'] - (frame['<I>/mA'] / 1000) * R * comp
    # Trim frame (vectorized)
    frame = frame[(frame['E_corr/V'] < max(bounds)) & (frame['E_corr/V'] > min(bounds))]
    frame.reset_index(drop=True, inplace=True)
    E = frame['E_corr/V']


    baseLine = get_BL(BaseLine_const, BL_inf)
    baseLine_c = baseLine.copy()
    baseLine_c['<J>/A cm^-2'] = baseLine_c['<J>/A cm^-2'] * (scanRate/(2* BL_inf['SR']))
    bL = baseLine_c['<J>/A cm^-2'].mean()  
    # corrFrame_J = frame['<J>/A cm^-2'] - ( bL ) # NumPy array for corrected current
    
    min_J =min(frame['<J>/A cm^-2'])
    #check = bL - min_J
    #print("the cehck is", check)
    def check_bl(bl, min_j):
        if bl > min_j:
            corrFrame_J = frame['<J>/A cm^-2'] - ( bL ) # NumPy array for corrected current
            
        else:
            corrFrame_J = frame['<J>/A cm^-2'] - ( min_J )
        return corrFrame_J
    
    corrFrame_J = check_bl(bL, min_J)
    

    # Calculate adsorption coverage (Corrected and more efficient)
    Q_list = []
    Q = 0
    time = frame['time/s'].values
    corrFrame_J_values = corrFrame_J.values
    #simpler/different intergration that doesnt use np.trapz
    
    
    for i in range(1, len(frame)):
        dt = time[i] - time[i - 1] #time differenctiated over (1 second)
        #intergration (make box with hight J + J+1, and length dt, then divide to get trangle (trapaziod integration bec in a for-loop)
        Q += (corrFrame_J_values[i] + corrFrame_J_values[i - 1]) * dt / 2 
        
        adsorption = Q / TCD #normalize to coverage
        Q_list.append(adsorption)

    # E has one more element than Q_list, so we slice E to match
    E_matched = E.iloc[1:] # slice E to match the length of Q_list

    return Q_list, E_matched  # Return E_matched



plt_avg_Ko(library, electrode_areas, Rs, colors)
