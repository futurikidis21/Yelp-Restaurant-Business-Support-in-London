#Import the required libraries
import pandas as pd
import numpy as np
#Read the database with Pandas
London_Wards=pd.read_csv('London_Wards.csv')
#Calculate square of length and width of each rectangle
sq_length=London_Wards['Length']**2
sq_width=London_Wards['Width']**2
#Calculate sum of squares
sum=sq_length+sq_width
#Calculate the diameter of each rectangle with pythagorian theorem
diameter=sum.apply(np.sqrt)
#Calculate radius for search parameter
radius=diameter/2
#Add to London_Wards df
London_Wards['Diameter']=diameter
London_Wards['Radius']=radius
#Export to csv file
London_Wards.to_csv('Search.csv')
    