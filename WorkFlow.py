import os

os.chdir('C:/Users/svi002/OneDrive/04_Assignment/03_Scripts/PreProcessing')

import geology


fd = 'C:/Users/svi002/OneDrive/04_Assignment/01_RawData/AMWADU'
Save_fd = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data'

# geology.GeologyToCsv(fd, Save_fd)

fd = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data'
csv_fn = 'BoreholesDatabase.csv' 
Save_fd = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data/GIS/SHP'
shp_fn = 'BoreholesDatabase.shp'
crs = 'epsg:32632 '



geology.GeologyCsvToShp(fd, csv_fn, Save_fd, shp_fn, crs)


# Tif_fd = 'C:/Users/svi002/OneDrive/04_Assignment/01_RawData/GIS/Raster'
# InputTif_fn = 'DEM_Area.tif'
# Shp_fd = 'C:/Users/svi002/OneDrive/04_Assignment/01_RawData/GIS/Vector/Shape_area'
# InputShp_fn = 'Shape_area.shp'
SaveTif_fd = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data/GIS/TIF'
Output_fn = 'DEMAreaClipRes.tif'
# GIS.ClipRes (Tif_fd, InputTif_fn, Shp_fd, InputShp_fn, SaveTif_fd, Output_fn) #clipping and resampling


#kriging was not inputed in the workflow. Detailed analysis
