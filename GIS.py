#cut matrix
#resample matrix to 30x30

def ClipRes (Tif_fd, InputTif_fn, Shp_fd, InputShp_fn, SaveTif_fd, Output_fn):
    import os
    import numpy as np
    import rioxarray as rio
    import pandas as pd
    import xarray as xr
    import geopandas as gpd
    from rasterio.enums import Resampling
    
    os.chdir (Tif_fd)
    Dem_ds = rio.open_rasterio(InputTif_fn)
    
    downscale_factor = 6
    new_width = int(Dem_ds.rio.width / downscale_factor)
    new_height = int(Dem_ds.rio.height / downscale_factor)
    DemRes_ds = Dem_ds.rio.reproject(
        Dem_ds.rio.crs,
        shape=(new_height, new_width),
        resampling=Resampling.bilinear)
    
    
    os.chdir(Shp_fd)
    gdf = gpd.read_file (InputShp_fn)
    ClipDem_ds = DemRes_ds.rio.clip (gdf.geometry, gdf.crs)
    os.chdir (SaveTif_fd)
    # DemRes_ds.rio.to_raster(Output_fn)
    print('''Resampling is Done. The grid size for MODFLOW is: height vs width = {},{}. \n\n
          Its resolution is {} \n\n'''.format(ClipDem_ds.rio.height, ClipDem_ds.rio.width, ClipDem_ds.rio.resolution()))
    
  
Tif_fd = 'C:/Users/svi002/OneDrive/04_Assignment/01_RawData/GIS/Raster'
InputTif_fn = 'DEM_Area.tif'
Shp_fd = 'C:/Users/svi002/OneDrive/04_Assignment/01_RawData/GIS/Vector/Shape_area'
InputShp_fn = 'Shape_area.shp'
SaveTif_fd = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data/GIS/TIF'
Output_fn = 'DEMAreaClipRes.tif'
ClipRes (Tif_fd, InputTif_fn, Shp_fd, InputShp_fn, SaveTif_fd, Output_fn) #clipping and resampling