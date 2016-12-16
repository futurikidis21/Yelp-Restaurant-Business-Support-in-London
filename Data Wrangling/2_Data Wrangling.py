#Initial investigation on the data downloaded
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
print('---------------------------------------------------------------------------')
#Import the final downlod file
df=pd.read_csv('final.csv')
#Drop the duplicates to a clean dataframe based on unique urls
final=df.drop_duplicates('url')
#Import clean database and prepare for imporation
clean_db=pd.read_csv('clean_db.csv')
clean_db.drop(clean_db.columns[[0,]],axis=1,inplace=True)
clean_db=clean_db.rename(columns={'Area_code':'Borough_code'})
#Prepare initial db for importation
final_move=final.loc[:,['NAME_1','GSS_CODE','HECTARES']]
final_move.columns=['Area','Area_Code','Area_Size']
final_move.index=final_move.Area
final_move=final_move.drop_duplicates('Area_Code')
clean_db.index=clean_db.Area
clean_db=clean_db.merge(final_move,on='Area',how='left')
#Drop duplicatess from process
clean_db=clean_db.drop_duplicates('URL')
#Translate hectares to km2
clean_db['Area_Size']=clean_db['Area_Size']*0.01
print('---------------------------------------------------------------------------')
#Bring in Census dataset
census=pd.read_excel('london-borough-profiles-2016-Demographics.xls',sheetname='Data',skip_footer=6)
census=census.drop([0])
census=census.reset_index()
census.drop(census[[0,]],axis=1,inplace=True)
#Keep only selected rows
census=census.iloc[:,[1,4,5,6,7,8,9,10,11,29,37,38,39,40,41,42,47,48,52]]
#Calculate and convert hectares to sq.km
census['Inland Area (sq.km)']=census['Inland Area (Hectares)']*0.01
census['Population density (per sq.km)']=census['GLA Population Estimate 2016']/census['Inland Area (sq.km)']
#Drop undwanted columns
census.drop(census.columns[[3,4]],axis=1,inplace=True)
census=census.rename(columns={'New code':'Borough_code'})
#Connect the databases based on Borough code
clean_db=clean_db.merge(census,on='Borough_code',how='left')
print('---------------------------------------------------------------------------')
#Export file for analysis by borough
clean_db.to_csv('By_Borough_Analysis.csv',index=False)
print('---------------------------------------------------------------------------')
#Import db.
wards=pd.read_excel('ward-atlas-2014boundaries.xls',skip_footer=35,sheetname='iadatasheet')
#Drop unwanted columns
wards=wards.rename(columns={'New Code':'Ward_Code','Name':'Ward_Name','Borough':'Borough_Ward'})
wards.index=wards['Ward_Code']
#Clear previous borough profiles
clean_db=clean_db.iloc[:,0:24]
clean_db.index=clean_db['Area_Code']
clean_db=clean_db.join(wards)
#clean_db=clean_db.drop_duplicates('URL')
clean_db.to_csv('By_Ward_Analysis.csv',index=False)







 

