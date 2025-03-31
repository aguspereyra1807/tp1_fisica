import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

LENGTH_UNCERTAINTY = 0.1 # 𝛿L = Length Uncertainty = 0.1cm

def calcArea(length):
    # A = L^2 ± √(dA/dL|L_0 * 𝛿L)^2
    max = length**2 + np.sqrt((2*length*LENGTH_UNCERTAINTY)**2) 
    min = length**2 - np.sqrt((2*length*LENGTH_UNCERTAINTY)**2)
    return f"[{round(min,2)},{round(max,2)}]"

def calcVolume(diameter, uncertainty):
    # V = (4/3) * π * (d/2)^3 ± √(dV/dd|d_0 * 𝛿d)^2
    radius = diameter / 2
    volume = (4/3) * np.pi * radius**3
    vUncertainty = np.sqrt((2 * np.pi * radius**2 * uncertainty)**2)
    max_volume = volume + vUncertainty
    min_volume = volume - vUncertainty
    return f"[{round(min_volume,2)},{round(max_volume,2)}]", vUncertainty

def calcVolumes(diameters, uncertainities):
     volumes = []
     vUncertainities = []
     for i in range(len(diameters)):
          v, u = calcVolume(diameters[i],uncertainities[i])
          volumes.append(v)
          vUncertainities.append(u)
     return volumes, vUncertainities

def linealFunction(x,a,b):
     return a*x+b

def showErrorBar(x,y,err,color,xLabel, yLabel,title,legend):
     _, ax = plt.subplots(figsize=(9,6))

     ax.errorbar(x,y, yerr=err, fmt='d', linewidth=1, capsize=6, c=color, label=legend)
     ax.set_xlabel(xLabel, fontsize=12)
     ax.set_ylabel(yLabel, fontsize=12)
     ax.legend()

     plt.title(title)

     plt.tight_layout()

     plt.show()

def showLinearRegression(x,y,err,color, xLabel, yLabel,title,legend):
     _, ax = plt.subplots(figsize=(9,6))

     ax.errorbar(x,y, yerr=err, fmt='d', linewidth=1, capsize=6, c=color, label=legend)
     popt, _ = curve_fit(linealFunction, x, y, sigma=err)
     model_distance = linealFunction(x,*popt)
     plt.plot(x,model_distance,c=color,zorder=1)
     ax.set_xlabel(xLabel, fontsize=12)
     ax.set_ylabel(yLabel, fontsize=12)
     ax.legend()

     plt.title(title)

     plt.tight_layout()

     plt.show()