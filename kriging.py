import os
import numpy as np 
import pandas as pd
import geopandas as gpd

fn = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data'
fn_save = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data/GIS/SHP'
csv_fn = 'BoreholesDatabase.csv'
os.chdir(fn)
df = pd.read_csv (csv_fn)
df = df.loc [df.Depth> 40]
df = df.replace({'zand':'sand', 'veen': 'peat', 'leem': 'loam', 'klei' : 'clay', 'schelpen': 'shells' , 
                 'grind' : 'gravel', 'niet benoemd': 'unnamed', 'hout':'wood', 'geen monster': 'no sample'}) 
df = df.replace({'unnamed': 'sand', 'no sample': 'sand'}) # these are always in the shallow horizon, which is basically sand
df = df.replace({'loam': 'clay'}) #loam can be local variations of clay
df = df.replace({'wood': 'sand'}) #2 layers of wood occur in the sand
df = df.replace({'shells': 'sand'}) #layers of shell are thin, not laterally continue and occur within the sand. 
df = df.replace({'gravel': 'sand'}) #gravel is thick only in the confined aquifer
gdf = gpd.GeoDataFrame (df, geometry=gpd.points_from_xy(df.X, df.Y) ).reset_index(drop= True)
gdf.crs = 'epsg:32632'
print(gdf.Layer.unique())

columns = gdf.columns.to_list()
columns = columns.append(['Zb', 'Thickness'])
borehole_gdf = gpd.GeoDataFrame(columns = columns)



for borehole in gdf.Code.unique():
    gdf1 = gdf.loc[gdf.Code == borehole].reset_index(drop = True)
    bottom_list = []
    for j, layer in enumerate(gdf1.Layer):
        if j == 0:
            SandTop = gdf1.Zt[j]
        if j == gdf1.Layer.size - 1:
            bottom = gdf1.Depth[j]
        else: bottom = gdf1.Zt[j+1]
        bottom_list.append(bottom)
    gdf1['Zb'] = bottom_list
    gdf1['Thickness'] = np.abs(gdf1.Zt - gdf1.Zb)
    borehole_gdf = pd.concat ([borehole_gdf , gdf1])

borehole_gdf = borehole_gdf.drop(columns = ['X', 'Y'])

#unconfined aquifer
unconfined_gdf = borehole_gdf.replace({'peat': 'sand'})
unconfined_gdf = unconfined_gdf.loc[(unconfined_gdf.Layer == 'sand') & (unconfined_gdf.Zt < 12)]
unconfined_df = pd.DataFrame (columns =unconfined_gdf.columns)
for i, borehole in enumerate(unconfined_gdf.Code.unique()):
    unconfined_gdf2 = unconfined_gdf.loc [unconfined_gdf.Code == borehole].reset_index(drop = True)
    Zt = unconfined_gdf2.iloc[0,3]
    Zb = unconfined_gdf2.iloc[-1,-2]
    unconfined_gdf3 = unconfined_gdf2.iloc[0,:].copy().to_frame().T
    unconfined_gdf3['Zt'] = Zt
    unconfined_gdf3['Zb'] = Zb
    unconfined_df = pd.concat([unconfined_df, unconfined_gdf3])
    unconfined_df = unconfined_df.drop(['Thickness'], axis = 1)
unconfined_gdf = gpd.GeoDataFrame(unconfined_df, crs = 'epsg:32632' )
    
#confined aquifer
confined_gdf = borehole_gdf.replace({'peat': 'sand'})
confined_gdf =  borehole_gdf.loc[(borehole_gdf.Layer == 'sand') & (borehole_gdf.Zt > 12) & (borehole_gdf.Zb < 70) & (borehole_gdf.Thickness > 1) ]
confined_df = pd.DataFrame (columns =confined_gdf.columns)
for i, borehole in enumerate(confined_gdf.Code.unique()):
    confined_gdf2 = confined_gdf.loc [confined_gdf.Code == borehole].reset_index(drop = True)
    Zt = confined_gdf2.iloc[0,3]
    Zb = confined_gdf2.iloc[-1,-2]
    confined_gdf3 = confined_gdf2.iloc[0,:].copy().to_frame().T
    confined_gdf3['Zt'] = Zt
    confined_gdf3['Zb'] = Zb
    confined_df = pd.concat([confined_df, confined_gdf3])
    confined_df = confined_df.drop(['Thickness'], axis = 1)
confined_gdf = gpd.GeoDataFrame(confined_df, crs = 'epsg:32632' )
 
peat_gdf = borehole_gdf.loc[(borehole_gdf.Layer == 'peat') & (borehole_gdf.Zb < 20)] #ignore deep peat

aquitard1_gdf = borehole_gdf.loc[(borehole_gdf.Layer == 'clay') & (borehole_gdf.Zb < 30) & (borehole_gdf.Thickness > 1)] 
aquitard2_gdf = borehole_gdf.loc[(borehole_gdf.Layer == 'clay') & (borehole_gdf.Zb > 30) & (borehole_gdf.Thickness > 1)] 

os.chdir(fn_save)
units_list = [unconfined_gdf, confined_gdf, peat_gdf, aquitard1_gdf, aquitard2_gdf, borehole_gdf]
units_name_list = ['unconfined_gdf', 'confined_gdf', 'peat_gdf', 'aquitard1_gdf', 'aquitard2_gdf', 'borehole_gdf']
for i, unit in enumerate(units_list):
    file_name = units_name_list[i].split('_')[0]
    unit.to_file('{}.shp'.format(file_name))
        
    


#check to rename layers 
# for i, layer in enumerate(gdf.Layer):
#     if layer == 'gravel':
#         code = gdf.iloc [i,0]
#         print(gdf.loc[gdf.Code == code])
        







 
