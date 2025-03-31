import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ast

from functions import calcArea, calcVolumes, showErrorBar, showLinearRegression

dataFrame = pd.read_csv("measures.csv", converters={'Diameters': lambda x: ast.literal_eval(x)}) # Diameters convertido a listas

def main():

     # Calculate Data

     ## AREA

     areas = []

     for length in dataFrame["Length"]:
          areas.append(calcArea(length))

     dataFrame["Area"] = areas

     ## DIAMETER

     dMid = [] # Diameter's Average (no uncertainty)
     dSTD = [] # Standard Deviation
     dEST = [] # STD Error
     dUncertainity = [] # dAverage Uncertainty
     dAvg = [] # Diameter's Average (uncertainty included)

     for diameters in dataFrame["Diameters"]:
          dMid.append(round(np.average(diameters),2))
          dSTD.append(round(np.std(diameters),2))

     nSqrt = np.sqrt(len(dataFrame["Diameters"]))

     for i in dSTD:
          dEST.append(round(i/nSqrt, 2))

     for i, error in enumerate(dEST):
          uncertainty = round(np.sqrt(error**2 + 0.1**2),2) # dAverage Uncertainty
          dUncertainity.append(uncertainty)
          dAvg.append(f"[{round(dMid[i] - uncertainty, 2)},{round(dMid[i] + uncertainty, 2)}]")

     dataFrame["DiameterAverage"] = dAvg
     dataFrame["DiameterSTD"] = dSTD
     dataFrame["DiameterEST"] = dEST

     ## VOLUME

     volumes, vUncertainites = calcVolumes(dMid, dUncertainity)

     dataFrame["Volume"] = volumes

     dataFrame.to_csv("data.csv", index=False) 

     # ==========================================================================================================================================

     # Graphs
          
     ## 1) Diameter / Mass (Normal Scale)

     plt.style.use('_mpl-gallery')

     x1 = np.array(dataFrame.loc[dataFrame["PaperWeight"] == 80, "Mass"].to_list())
     x2 = np.array(dataFrame.loc[dataFrame["PaperWeight"] == 150, "Mass"].to_list())
     x3 = np.array(dataFrame.loc[dataFrame["PaperWeight"] == 240, "Mass"].to_list())

     y1= dMid[:10]
     y2 = dMid[10:15]
     y3 = dMid[15:]

     showErrorBar(x1,y1,dUncertainity[0:10], "black", "Mass[g]", "Diameter[cm]", "Diameter / Mass", "Diameter Average (Paper Weight = 80g/m^2)")
     showErrorBar(x2,y2,dUncertainity[10:15], "blue", "Mass[g]", "Diameter[cm]", "Diameter / Mass", "Diameter Average (Paper Weight = 150g/m^2)")
     showErrorBar(x3,y3,dUncertainity[15:], "red", "Mass[g]", "Diameter[cm]", "Diameter / Mass", "Diameter Average (Paper Weight = 240g/m^2)")

     ## 2) Diameter / Mass (Normal Scale + Linear Regression)

     showLinearRegression(x1,y1,dUncertainity[0:10], "black", "Mass[g]", "Diameter[cm]", "Diameter / Mass", "Diameter Average (Paper Weight = 80g/m^2)")
     showLinearRegression(x2,y2,dUncertainity[10:15], "blue", "Mass[g]", "Diameter[cm]", "Diameter / Mass", "Diameter Average (Paper Weight = 150g/m^2)")
     showLinearRegression(x3,y3,dUncertainity[15:], "red", "Mass[g]", "Diameter[cm]", "Diameter / Mass", "Diameter Average (Paper Weight = 240g/m^2)")

     ## 3) Diameter / Mass (Logarithm scale)

     x1 = np.log10(((dataFrame.loc[dataFrame["PaperWeight"] == 80, "Mass"]).to_list()))
     x2 = np.log10(((dataFrame.loc[dataFrame["PaperWeight"] == 150, "Mass"]).to_list()))
     x3 = np.log10(((dataFrame.loc[dataFrame["PaperWeight"] == 240, "Mass"]).to_list()))

     y1 = dMid[:10]
     y2 = dMid[10:15]
     y3 = dMid[15:]
     err = []

     for i in range(len(dMid)):
          err.append(dUncertainity[i]/(dMid[i] * np.log(10)))

     showErrorBar(x1,y1,err[0:10], "black", "log10 Mass[g]", "log10 Diameter[cm]", "Diameter / Mass (Logarithm Base)", "Diameter Average (Paper Weight = 80g/m^2)")
     showErrorBar(x2,y2,err[10:15], "blue", "log10 Mass[g]", "log10 Diameter[cm]", "Diameter / Mass (Logarithm Base)", "Diameter Average (Paper Weight = 150g/m^2)")
     showErrorBar(x3,y3,err[15:], "red", "log10 Mass[g]", "log10 Diameter[cm]", "Diameter / Mass (Logarithm Base)", "Diameter Average (Paper Weight = 240g/m^2)")

     # # 4) Diameter / Mass (Logarithm scale + Lineal Regression)

     showLinearRegression(x1,y1,err[0:10], "black", "log10 Mass[g]", "log10 Diameter[cm]", "Diameter / Mass (Logarithm Base)", "Diameter Average (Paper Weight = 80g/m^2)")
     showLinearRegression(x2,y2,err[10:15], "blue", "log10 Mass[g]", "log10 Diameter[cm]", "Diameter / Mass (Logarithm Base)", "Diameter Average (Paper Weight = 150g/m^2)")
     showLinearRegression(x3,y3,err[15:], "red", "log10 Mass[g]", "log10 Diameter[cm]", "Diameter / Mass (Logarithm Base)", "Diameter Average (Paper Weight = 240g/m^2)")

     # # 5) Volume / Mass (Normal Scale)

     x1 = np.array(dataFrame.loc[dataFrame["PaperWeight"] == 80, "Mass"].to_list())
     x2 = np.array(dataFrame.loc[dataFrame["PaperWeight"] == 150, "Mass"].to_list())
     x3 = np.array(dataFrame.loc[dataFrame["PaperWeight"] == 240, "Mass"].to_list())

     volumesValues = [round((float(v.strip('[]').split(',')[0])+float(v.strip('[]').split(',')[1])) / 2, 2) for v in volumes]  # Extraer el promedio del volumen

     showErrorBar(x1, volumesValues[:10], vUncertainites[0:10], "black", "Mass[g]", "Volume[cm^3]", "Volume / Mass", "Volume (Paper Weight = 80g/m^2)")
     showErrorBar(x2, volumesValues[10:15], vUncertainites[10:15], "blue", "Mass[g]", "Volume[cm^3]", "Volume / Mass", "Volume (Paper Weight = 150g/m^2)")
     showErrorBar(x3, volumesValues[15:], vUncertainites[15:], "red", "Mass[g]", "Volume[cm^3]", "Volume / Mass", "Volume (Paper Weight = 240g/m^2)")

     # 6) Volume / Mass (Logarithm Scale + Linear Regression)

     logVUncertainity = [] 

     for i in range(len(vUncertainites)):
          logVUncertainity.append(vUncertainites[i] / (volumesValues[i] * np.log(10)))

     showLinearRegression(np.log10(x1), np.log10(volumesValues[:10]), logVUncertainity[:10], "black", "log10 Mass[g]", "log10 Volume[cm^3]",  "Volume / Mass (Logarithm Scale)", "Volume (Paper Weight = 80g/m^2)")
     showLinearRegression(np.log10(x2), np.log10(volumesValues[10:15]), logVUncertainity[10:15], "blue", "log10 Mass[g]","log10 Volume[cm^3]",  "Volume / Mass (Logarithm Scale)", "Volume (Paper Weight = 150g/m^2)")
     showLinearRegression(np.log10(x3), np.log10(volumesValues[15:]), logVUncertainity[15:], "red", "log10 Mass[g]","log10 Volume[cm^3]",  "Volume / Mass (Logarithm Scale)", "Volume (Paper Weight = 240g/m^2)")

if __name__ == '__main__':
     main()