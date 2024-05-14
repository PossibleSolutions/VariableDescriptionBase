#import necessary modules
import pandas as pd
import geopandas as gpd
import fiona
import os
from datetime import date
import numpy as  np


#Define dataset and output location. Default output location = same as input data folder as VariableDescription_xxx.xlsx
DataPath = r"YourPath"
Filename = os.path.basename(DataPath)
Folder = os.path.dirname(DataPath)
#Use OutFolder if you want to save to a spesific path and replace Folder with OutFolder in OutPath
#OutFolder = r"YourFolderPath"
OutPath = Folder + "\VariableDescription_" + Filename + ".xlsx"
print("Saving To: ", OutPath)

#list layers within a gpkg, gdb, shp
Layers = fiona.listlayers(DataPath)
print(Layers)

date = date.today()
print(date)

#create empty Excel with metainfo and variable description
ExplainingVariables2 = ["DataSource","Variable","Explanation", "NumberOfRows","NullPercentage","UniqueValues","UniqueValuesList","AdditionalRemarks", "Source", "Date", "Creator"]
df2 = pd.DataFrame([DataPath,"A variable that appears in the data","Its explanation","Number of rows","Percentage of nulls, if 100, remove field","Number of distinct values","List of unique values if less than 10","Additional Remarks and usage suggestions. E.g. Generally value X seems to be missclassified","Source of data, usually the data provider. E.g. SYKE", date,"Your name and organization"],ExplainingVariables2)
with pd.ExcelWriter(OutPath) as writer:
    df2.to_excel(writer, sheet_name="Explanation") 

ExplainingVariables = ["NumberOfRows","Nullpercentage","UniqueValues","UniqueValuesList","Explanation", "AdditionalRemarks"]

for Layer in Layers:
    #read each layer
    Data = gpd.read_file(DataPath, layer=Layer) 
    print(Layer, len(Data))
    DataVariables = Data.columns
    #calculate nnumber of columns and null percentage for each column
    NumberOfRows = len(Data)
    Nullpercentage = Data.isnull().mean() * 100
    #calculate unique values for each column
    UniqueValues = Data.nunique()
    #create a DataFrame with DataVariables as the index
    df = pd.DataFrame(index=DataVariables, columns=ExplainingVariables)
    #assign NumberOfRows,Nullpercentage,UniqueValues to the corresponding column in the DataFrame
    df["NumberOfRows"] = NumberOfRows
    df["Nullpercentage"] = Nullpercentage
    df["UniqueValues"] = UniqueValues
    #if unique values less than 10, store the unique values in a new column "UniqueValuesList"
    df["UniqueValuesList"] = df.apply(lambda row: ', '.join(str(v) for v in Data[row.name].unique()) if row.UniqueValues < 10 else np.nan, axis=1)
    df = df.reset_index().rename(columns={"index": "Variable"})
    #with layer name instead of creation of a new excel for each layer within a geopackage
    with pd.ExcelWriter(OutPath,mode="a") as writer:
        df.to_excel(writer, sheet_name=Layer)