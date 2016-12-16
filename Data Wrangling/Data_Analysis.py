#Initial investigation on the data downloaded
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.decomposition import PCA
print('---------------------------------------------------------------------------')
#Load concatenated db
df=pd.read_csv('Analysis.csv')
print('---------------------------------------------------------------------------')

#Keep only columns to be analysed.
#On this phase the data will be analysed on the borough level
#Filtering the ratings and demographic values
analysis=df.loc[:,['Borough_code','Borough','London_WA_Rating','Review_Count','PriceV','Nearby_Business_Count', 'GLA Population Estimate 2016',
 'GLA Household Estimate 2016',
 'Average Age, 2016',
 'Proportion of population aged 0-15, 2016',
 'Proportion of population of working-age, 2016',
 'Proportion of population aged 65 and over, 2016',
 'Employment rate (%) (2015)',
 'Proportion of working age people with no qualifications (%) 2015',
 'Proportion of working age with degree or equivalent and above (%) 2015',
 'Gross Annual Pay, (2015)',
 'Gross Annual Pay - Male (2015)',
 'Gross Annual Pay - Female (2015)',
 'Modelled Household median income estimates 2012/13',
 'Number of active businesses, 2014',
 'Two-year business survival rates (started in 2012)',
 'Median House Price, 2014',
 'Inland Area (sq.km)',
 'Population density (per sq.km)']]
#Group by borough
analysis=analysis.groupby(['Borough']).mean()
#Group by borough and unique key to get business count
c_b=df.loc[:,['Borough','URL']]
c_b=c_b.groupby(['Borough']).count()
c_b=c_b.rename(columns={'URL':'Business_Count'})
#Join the business count with the rest of the database
analysis=analysis.join(c_b)
print('---------------------------------------------------------------------------')
