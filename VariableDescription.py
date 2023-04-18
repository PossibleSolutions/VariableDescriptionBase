#import necessary modules
import pandas as pd
import geopandas as gpd
import fiona
import os
from datetime import date

#Define dataset and output location. Default output location = same as input data folder as VariableDescription_xxx.xlsx
DataPath = r"YourDataPath"

Filename = os.path.basename(DataPath)
Folder = os.path.dirname(DataPath)
OutPath = Folder + "\VariableDescription_" + Filename + ".xlsx"
print("Saving To: ", OutPath)

#Use OutFolder instead if you want to save to a spesific path and replace Folder with OutFolder in OutPath
#OutFolder = r"YourOutPath"

#list layers within a gpkg, gdb, shp
Layers = fiona.listlayers(DataPath)
print(Layers)

#Date properties
date = date.today()
print(date)

#create empty Excel with metainfo and variable description
ExplainingVariables2 = ["DataSource","Variable","Explanation", "AdditionalRemarks", "Source", "Date", "Creator"]
df2 = pd.DataFrame([DataPath,"A variable that appears in the data","Its explanation","Additional Remarks and usage suggestions. E.g. Generally value X seems to be missclassified","Source of data, usually the data provider. E.g. SYKE", date,"Your name and organization"],ExplainingVariables2)
with pd.ExcelWriter(OutPath) as writer:
    df2.to_excel(writer, sheet_name="Explanation") 
    
#Column names in Excel, sheet1 and sheet2
ExplainingVariables = ["Variable","Explanation", "AdditionalRemarks"]

for Layer in Layers:
    #read 1 row of each layer and extract its columns
    Data = gpd.read_file(DataPath, rows=1, layer=Layer)
    DataVariables = Data.columns
    #convert column list to table, transpose
    df = pd.DataFrame([DataVariables,"",""],ExplainingVariables)
    df = df.transpose()
    #write columns as rows. excel sheet is named according to layer name, mode a is append.
    with pd.ExcelWriter(OutPath,mode="a") as writer:
        df.to_excel(writer, sheet_name=Layer)