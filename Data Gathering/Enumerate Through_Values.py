#This code dowload the Yelp db business rating, number of reviews and details.
#The method utilised was based on geospatial location since yelp restricts the total offset number and the location is inclomplete for some cases.
#Thus each London area was modifies on ArcGis and centroids were calculated.
#Then each shape/area was enclosed in a rectangle and the sides size were calculated.
#Then in another code we utilised pythagoreum to calculate diameter and radius of each search parameter/area.
#Then we used those centroids cartesian coordinates along with radius to search for the businesses on Yelp.
#Import the required libraries
import pandas as pd
import time
import requests
from pandas.io.json import json_normalize
#Import csv file to export the data
final=pd.read_csv('final.csv')
#Import csv file with the centroids and radius to call
sp=pd.read_csv('Search.csv')
#This for loop loops through each London area and returns the Longtitude,Latitude and radius of each area
for index,row in sp.iterrows() :
    Lat=row.Lat
    Long=row.Long
    Radius=row.Radius
    i=-20
    check=pd.read_csv('check.csv')
#This while statement ensures that the offset parameter is below the limit specified by Yelp.
#If i counter goes above it will return error message
    while i<1000: 
        i+=20
#This statement is used to check if we get consecutive blank responses which means there are no more restaurants in the area.
#At the moment this allows 2 blank responses before it break the while loop.
#It checks the difference between response theoritical count to actual count.
        if i-len(check)>80:
            break
        else:
#These are the parameters and the link to call the yelp api
#The long,radius and lat parameters change for each area
            url = 'https://api.yelp.com/v3/businesses/search'
            headers = {'Authorization': 'Bearer ​hNJYVUNqeTCflzfm_Wd3BBQ2KpmX9oD9zUitWOfW0jSNiTCeedX_5cds7vyTXxFp3DcHHU5SOUpQ6oVTJAB0DdKO14ppzWReE5ErtAaSV3IWoUAh5WObRmZEMiAXWHYx'}
            params = {'term': 'restaurants',
                      'latitude': Lat,
                      'longitude': Long,
                      'radius': int(Radius),
                      'sort_by': 'rating',
                      'offset': i
                      }
#This is where the code send the request to yelp api.
            resp = requests.get(url=url, params=params, headers=headers)
            print(i)
#The server sends blank responses or error so this is where we examine the response and either continue or loop.
            try:
                tomove=json_normalize(resp.json()['businesses'])
            except (IndexError,KeyError,ValueError):
                continue
            pass
 #Then the file is consolidated into final df after it is normalised from Json response to pandas df.     
            tomove=json_normalize(resp.json()['businesses'])
            check=pd.concat([check,tomove])
            final=pd.concat([final,tomove])
 #Timedelay to keep the connection to Yelp live.
            time.sleep(1)
 #Print statements to keep track of progress.
    print (row.NAME)
    print (len(final))
#Final export to csv file.
final.to_csv('final.csv')
