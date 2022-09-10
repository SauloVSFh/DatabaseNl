import os
import rioxarray as rio
import xarray as xr
from osgeo import gdal
import numpy as np
import pandas as pd

#base for projection
os.chdir('C:/Users/svi002/OneDrive/04_Assignment/02_Data/GIS/TIF')
fn2 = 'DEM_Area30_255x294_30x30.tif'
ds2 = gdal.Open(fn2)
proj = ds2.GetProjection()

os.chdir('C:/Users/svi002/OneDrive/04_Assignment/02_Data/ET/Raster files')
fn = 'ET_rate2_3030.tif'
ds = gdal.Open(fn)
array = ds.GetRasterBand(1).ReadAsArray()

new_height = 294 
new_width = 255
xsize = ysize = 30
x_min = 92765
x_max = 100385
y_min = 478475
y_max = 487265

# fn_name = 'ET_rate2_{}x{}.tif'.format(str(new_width), str(new_height))
# dsRes = gdal.Warp(fn_name,
#                   ds,  width = new_width, height = new_height,
#                   resampleAlg = "bilinear")
# dsRes = ds = ds2 = None 

# outputBounds = (x_min-15, y_min-15, x_max+15, y_max+15)

# fn_output = 'ET_rate2_{}x{}_30x30.tif'.format(str(new_width), str(new_height))
# ds = gdal.Open(fn_name)
# dsRes = gdal.Warp(fn_output,
#                   ds,  width = new_width, height = new_height,
#                   resampleAlg = "bilinear")
# dsRes = ds = ds2 = None 



# 
# # dsRes = gdal.Warp(fn_output, ds, xRes= 30, yRes = 30, 
# #                   resampleAlg = "bilinear")
# # dsRes = ds  = None
# # os.remove(fn_name)


ds = rio.open_rasterio('ET_depth_m_3030.tif')
arr = ds.to_numpy()[0]
m,n = arr.shape
X,Y = ds.x.values, ds.y.values
x,y = np.meshgrid(X, Y)
out = np.column_stack((x.ravel(),y.ravel(), arr.ravel()))

os.chdir('C://Users//svi002//OneDrive//04_Assignment//02_Data//ET')
df = pd.DataFrame(out, columns = ['x', 'y', 'z'])
df = df.loc [df.z != df.z.min()]
df.to_csv('ET_depth_XYZ.dat', index = False)