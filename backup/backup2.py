import os
import pandas as pd
import geopandas as gpd
import skgstat as skg
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

Shpfd = 'C:/Users/svi002/OneDrive/04_Assignment/02_Data/GIS/SHP'
os.chdir(Shpfd)

files = ['aquitard2', 'unconfined', 'confined', 'peat','aquitard1']
file = files[-1]
gdf = gpd.read_file(file+'.shp')
gdf['x'] = gdf.geometry.x
gdf['y'] = gdf.geometry.y

gdf = gdf.drop_duplicates(subset=['Code'])
gdf = gdf.drop_duplicates(subset=['Zb'])
gdf = gdf.loc[(gdf.Zb > 1) & (gdf.Zb<25) & (gdf.Thickness > 3)]

gdf.plot('Zb', legend = True)


# gdf.plot('Zb', legend = True)
# sns.histplot(gdf.Zb)

# We determine xmin, xmax, ymin and ymax from our dataset:
# xv = gdf['x'].values
# yv = gdf['y'].values
# xmin, xmax = min(xv), max(xv)
# ymin, ymax = min(yv), max(yv)
# res_x = 248
# res_y = 281
# # res_y = int((ymax - ymin)*res_x/(xmax - xmin))
# xx,yy = np.mgrid[xmin:xmax:complex(res_x), 
#                  ymin:ymax:complex(res_y)]

# V_width = (gdf.geometry.x.max() - gdf.geometry.x.min() ) / 2
# V = skg.Variogram(gdf[['x', 'y']].values, gdf.Zb.values, maxlag= V_width, n_lags=25,
#                   model='gaussian', normalize=False)

# ok = skg.OrdinaryKriging(V, min_points=2, max_points=20, mode='exact')

# points = np.asanyarray(gdf[['x', 'y']])
# values = gdf['Zb'].values


# hh_hat = ok.transform(xx.flatten(), yy.flatten()).reshape(xx.shape)

# fig, axs = plt.subplots(1, 2 ,figsize=(15, 10), sharey=True)

# ax = axs[0]

# # Contour fringes of the kriging process:
# ctr_hh = ax.contourf(xx, yy, hh_hat,
#                      range(150,200,5),
#                      cmap = "viridis_r", 
#                      alpha = 0.5)

# # Contour fringes of the kriging process:
# ctr_hh = ax.contourf(xx, yy, hh_hat,
#                      range(150,200,5),
#                      cmap = "viridis_r", 
#                      alpha = 0.5)

# ax.set_title("Ordinary kriging estimation")
# # V.plot()
# # 
# # V.experimental.plot()
# # plt.scatter(V.bins, V.experimental)
# # plt.ylim([0,V.experimental.max()+100])
# # plt.show()

