# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 21:20:45 2021

@author: mgome
"""

import glob, os
import pandas as pd
import numpy as np


dataname="GW_levels_allwells"
path =r'C:\Users\DELL\OneDrive\Groundwatch\DELFT\GDCI\Hydrogeostatistics\dinotek\Groundwater levels, Well\original'
path_output=r'C:\Users\DELL\OneDrive\Projetos\Python\python'
filenames = glob.glob(path + "/*1_1.csv")


dfs = []
xcor_v=[]
ycor_v=[]
zcor_v=[]
dfilter_v=[]
i=0
ic=0
for filename in filenames:

       dat=pd.read_csv(filename,sep=",",engine='python', header=11, index_col=False)
       if dat.columns[0] == "Locatie":
           dfs.append(dat)
           lendat=len(dat)
           ic+=1
       else:
           dat_2=pd.read_csv(filename,sep=",",engine='python', header=12,  index_col=False)
#           print(dat.columns[0])
           if dat_2.columns[0] == "Locatie":
               dfs.append(dat_2)
               lendat=len(dat_2)
               ic+=1
           else:
               dat_3=pd.read_csv(filename,sep=",",engine='python', header=13,  index_col=False)
               if dat_3.columns[0] == "Locatie":
                   dfs.append(dat_3)
                   lendat=len(dat_3)
                   ic+=1
       if ic!=0:

           dat2=pd.read_csv(filename,sep="\t",engine='python',header=None)[0][9:11]
           dat3=dat2.str.split(',',expand=True)
           # lendat=len(dat)
           #dfs.append(dat)
           
           xcor=[int(dat3[3][10])]*lendat
           ycor=[int(dat3[4][10])]*lendat
           try:
               dfilter=[int(dat3[12][10])]*lendat
               zcor=[int(dat3[5][10])]*lendat
           except:
               dfilter=[9999]*lendat
               zcor=[9999]*lendat
        
           xcor_v.append(xcor)
           ycor_v.append(ycor)
           zcor_v.append(zcor)
           dfilter_v.append(dfilter)
       ic=0
       i+=1
       #print(lendat)

       
fulldata = pd.concat(dfs, ignore_index=True)
d = {'x': np.hstack(xcor_v), 'y': np.hstack(ycor_v), 'z' :np.hstack(zcor_v), 'depth_filter': np.hstack(dfilter_v) }
Coor = pd.DataFrame(data=d)

com_data=pd.concat([Coor, fulldata], axis=1)

timeseries=com_data[com_data.columns[:10]]
#%%


bnames=timeseries[timeseries.columns[4]].values
borenames=np.unique(np.array(bnames))

rangedates=pd.date_range('01-1990','01-2020', freq='M')
rangdat=pd.DataFrame(rangedates)
rangdat.rename(columns={0:'dates'}, inplace=True)
rangdat2 = rangdat['dates'].dt.strftime("%Y-%m")
rangdat3=pd.DataFrame(rangdat2)
rangdat3.set_index('dates', inplace=True)
timeseries["dates"] = pd.to_datetime(timeseries["Peildatum"])
#timeseries["dates_index"] = timeseries["dates"].dt.strftime("%Y-%m")
#timeseries3=pd.DataFrame(timeseries2)

matrix=np.zeros((360,len(borenames)))
for i in range(len(borenames)):
    datbor=timeseries.loc[timeseries.Locatie==borenames[i]]
    datbor.set_index('dates', inplace=True)
    monthdata=datbor.resample('M').mean()
    monthdata['datesind']=monthdata.index
    monthdata['datesind']=pd.to_datetime(monthdata['datesind'])
    monthdata['dates_id']=monthdata['datesind'].dt.strftime("%Y-%m")
    monthdata.set_index('dates_id',inplace=True)   
    dateborehole=monthdata[monthdata.columns[-2]]
    dateborehole=pd.DataFrame(dateborehole)
    dateborehole.rename(columns={dateborehole.columns[0]:borenames[i]}, inplace=True)
    rangedata=rangdat3.join(dateborehole)
    matrix[:,i]=np.hstack(rangedata.values)
    

finalmatrix=pd.DataFrame(matrix)
finalmatrix.columns=borenames
finalmatrix.insert(0, "Dates",rangdat3.index)
finalmatrix.to_excel(path_output + '/'+str(dataname)+'.xlsx', index=True)


#timeseries["Date"] = pd.to_datetime(timeseries["Peildatum"])
#timeseries.to_csv(path_output + '/'+str(dataname))
timeseries.to_excel(path_output + '/'+str(dataname)+'.xlsx')
