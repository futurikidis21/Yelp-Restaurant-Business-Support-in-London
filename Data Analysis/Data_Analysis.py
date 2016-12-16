#Initial investigation on the data downloaded
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from sklearn.decomposition import PCA
import statsmodels.api as sm
import scipy.stats as stats
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from wordcloud import WordCloud
#Load mixed LOAC database
df=pd.read_csv('by_LOAC.csv')
#Convert the data types to numberic
df[['Rating','Review_Cou','loac_population','loac_POPDEN_sqkm','loac_Households','loac_area','Population_change_lsoa','Population_2014_lsoa','2015_Median_House_Price_LSOA','House_price_%5yChange_LSOA','Business_survival_rate','RV_floorspace_Borough_level_5ychange','RV_floorspace_Borough_level','population_density_sqkm_borough']]=df[['Rating','Review_Cou','loac_population','loac_POPDEN_sqkm','loac_Households','loac_area','Population_change_lsoa','Population_2014_lsoa','2015_Median_House_Price_LSOA','House_price_%5yChange_LSOA','Business_survival_rate','RV_floorspace_Borough_level_5ychange','RV_floorspace_Borough_level','population_density_sqkm_borough']].apply(pd.to_numeric)
#create numberic dataset as df2
df2=df[['Rating','Review_Cou','loac_population','loac_POPDEN_sqkm','loac_Households','loac_area','Population_change_lsoa','Population_2014_lsoa','2015_Median_House_Price_LSOA','House_price_%5yChange_LSOA','Business_survival_rate','RV_floorspace_Borough_level_5ychange','RV_floorspace_Borough_level','population_density_sqkm_borough']]
print('---------------------------------------------------------------------------')
#PCA Testings
#scale the feature for PCA
numberOfColumnsToLook = 9
columns=df2.columns
scaled = preprocessing.StandardScaler().fit_transform(df2)
scaled = pd.DataFrame(scaled, columns=df2.columns)
print ("New Variances:\n", scaled.var())
print ("New Describe:\n", scaled.describe())
#PCA
pca = PCA(n_components=2)
pca.fit(scaled)
PCA(copy=True, n_components=2, whiten=False)
axes = pca.transform(scaled)
scaled.shape
axes.shape
#Plot results of PCA
plt.figure(1)
plt.suptitle('First two components')
plt.xlabel('PC_1')
plt.ylabel('PC_2')
plt.scatter(axes[:,0], axes[:,1], c = "#D06B36", s = 50, alpha = 0.4, linewidth='0')
#Print Components
#######Fist Component
columns=np.asarray(df2.columns.values)
#print( pca.components_)
comp1Loadings = np.asarray(pca.components_[0])[np.argsort( np.abs(pca.components_[0]))[::-1]][0:numberOfColumnsToLook]
comp1Names = np.asarray(columns)[np.argsort( np.abs(pca.components_[0]))[::-1]][0:17]
print ("First component: ")
for i in range(0, numberOfColumnsToLook):
    print ( "Column \"" , comp1Names[i] , "\" has a loading of: ", comp1Loadings[i])
print('---------------------------------------------------------------------------')
#######Second Component
comp2Loadings = np.asarray(pca.components_[1])[np.argsort( np.abs(pca.components_[1]))[::-1]][0:numberOfColumnsToLook]
comp2Names = np.asarray(columns)[np.argsort( np.abs(pca.components_[1]))[::-1]][0:numberOfColumnsToLook]
print ("Second component: ")
for i in range(0, numberOfColumnsToLook):
    print ( "Column \"" , comp2Names[i] , "\" has a loading of: ", comp2Loadings[i])
print('---------------------------------------------------------------------------')
#Ploting the values
rating = np.asarray(scaled[['Rating']], 'f')
plt.figure(2)
plt.suptitle('PCs for Ratings')
plt.xlabel('PC_1')
plt.ylabel('PC_2')
plt.scatter(axes[:,0], axes[:,1], c = rating, cmap = plt.cm.Blues, s = 50, linewidth='0')
#PCA on second component:
columnNames=np.asarray(df2.columns.values)
columnsToAnalyse = np.argsort( np.abs(pca.components_[1]))[::-1][0:numberOfColumnsToLook]
columnNamesFiltered = columnNames[columnsToAnalyse]
filteredLocalArray = scaled[columnsToAnalyse]
# Build a model that will return two principal components
pca3 = PCA(n_components=2)

# We first fit a PCA model to the data
pca3.fit(filteredLocalArray)

# have a look at the components directly if we can notice any interesting structure
projectedAxes = pca3.transform(filteredLocalArray)
# now on to drawing
plt.figure(3)
plt.suptitle('PCs for a sub group of related variables')
plt.xlabel('PC_1')
plt.ylabel('PC_2')
plt.scatter(projectedAxes[:,0], projectedAxes[:,1], c = rating, cmap = plt.cm.Blues, s = 50, linewidth='0')
print('---------------------------------------------------------------------------')
print ("A local analysis fo PCA 1")
print ("First component: ")
comp1Loadings = np.asarray(pca3.components_[0])[np.argsort( np.abs(pca3.components_[0]))[::-1]][0:numberOfColumnsToLook]
comp1Names = np.asarray(columnNamesFiltered)[np.argsort( np.abs(pca3.components_[0]))[::-1]][0:numberOfColumnsToLook]

for i in range(0, numberOfColumnsToLook):
    print ( "Column \"" , comp1Names[i] , "\" has a loading of: ", comp1Loadings[i])
    
print ("\n Second component: ")
comp2Loadings = np.asarray(pca3.components_[1])[np.argsort( np.abs(pca3.components_[1]))[::-1]][0:numberOfColumnsToLook]
comp2Names = np.asarray(columnNamesFiltered)[np.argsort( np.abs(pca3.components_[1]))[::-1]][0:numberOfColumnsToLook]

for i in range(0, numberOfColumnsToLook):
    print ( "Column \"" , comp2Names[i] , "\" has a loading of: ", comp2Loadings[i])
print('---------------------------------------------------------------------------')
# Barchart for survival rates and business count
bar=df[['Borough']]
bar=bar.groupby(['Borough'])['Borough'].count()
bar.name='Business_Count'
bar2=df[['Borough','Business_survival_rate']]
bar2=bar2.drop_duplicates()
bar2.index=bar2['Borough']
bar2=bar2.join(bar)
bar2=bar2.sort(columns='Business_Count',axis=0,ascending=False)
ax=bar2[['Borough','Business_Count']].plot.bar(x='Borough',title="Business survival rates by London Borough",legend=True,figsize=(10, 4),rot=90)
ax.set_ylabel("Business Count")
ax2=bar2[['Business_survival_rate']].plot.line(figsize=(10, 4),secondary_y=True,rot=90,color='Grey',ax=ax,linewidth=2,marker='o')
ax2.set_ylabel("Business Surviival Rate (%)")
plt.style.use('seaborn-colorblind')
plt.show()
print('---------------------------------------------------------------------------')
# Barchart for survival rates and business count
floor=df[['Borough','RV_floorspace_Borough_level_5ychange','RV_floorspace_Borough_level']]
floor['RV_floorspace_Borough_level_5ychange']=floor['RV_floorspace_Borough_level_5ychange']*100
floor=floor.groupby(['Borough'])['RV_floorspace_Borough_level','RV_floorspace_Borough_level_5ychange'].mean()
floor=floor.sort(columns='RV_floorspace_Borough_level',axis=0,ascending=False)
floor['Borough']=floor.index
ax=floor[['Borough','RV_floorspace_Borough_level']].plot.bar(x='Borough',title="Floorspace Rateable Value by Borough",legend=True,figsize=(10, 4),rot=90)
ax.set_ylabel("Floorspace Rateable Value (£/sq.m)")
ax2=floor[['RV_floorspace_Borough_level_5ychange']].plot.line(figsize=(10, 4),secondary_y=True,rot=90,color='Grey',ax=ax,linewidth=2,marker='o')
ax2.set_ylabel("RV 5 Year Average Change (%)")
plt.style.use('seaborn-colorblind')
plt.show()
print('---------------------------------------------------------------------------')
# Correlation Matrix excluding rating and review count
data=df[['Rating','Review_Cou','Nearby_Bus','loac_population','loac_POPDEN_sqkm','loac_Households','loac_area','Population_change_lsoa','Population_2014_lsoa','2015_Median_House_Price_LSOA','House_price_%5yChange_LSOA','Business_survival_rate','RV_floorspace_Borough_level_5ychange','RV_floorspace_Borough_level','population_density_sqkm_borough']]
import seaborn as sns
corr = data.corr()
sns.heatmap(corr, 
            xticklabels=corr.columns.values,
            yticklabels=corr.columns.values)
print('---------------------------------------------------------------------------')
# Wordcloud for supergroups
from wordcloud import WordCloud
# import list of supergroups and iteration between supergroups
list_SG=df['super_group_name'].unique()
for i, val in enumerate(list_SG):
    subset=df[((df['super_group_name']==str(val))&(df['Title']!='Bars'))]
    subset['Title']=subset['Title'].replace(to_replace=' ',value='_')
    data=subset[['super_group_name','Title','Rating']]
    data['Review_Cou']=data['Rating'].map(int)
    data=data.groupby(['super_group_name','Title'],as_index=False)['Rating'].mean()

# Generate a word cloud image
    wordcloud = WordCloud(background_color="white", max_words=2000).generate(str(data.Title))

# Display the generated image:
# the matplotlib way:
    plt.imshow(wordcloud)
    plt.axis("off")
    print(val)
    plt.show()
    
print('---------------------------------------------------------------------------')
# Nearby businesses count heatmap with seaborn
data=df[['Borough','Rating','Nearby_Bus']]
data=data.groupby(['Borough','Rating'],as_index=False)['Nearby_Bus'].mean()
data['Nearby_Bus']=data['Nearby_Bus'].round()
data['Nearby_Bus']=data['Nearby_Bus'].astype(int)
import seaborn as sns
sns.set()

# Load the example flights dataset and conver to long-form
map_tree = data.pivot("Borough", "Rating", "Nearby_Bus")

# Draw a heatmap with the numeric values in each cell
sns.heatmap(map_tree, annot=False,annot_kws={"size": 7})

# Pop density in sq.km heatmap with seaborn
data=df[['Borough','Rating','loac_POPDEN_sqkm']]
data=data.groupby(['Borough','Rating'],as_index=False)['loac_POPDEN_sqkm'].mean()
data['population_density_sqkm_borough']=data['loac_POPDEN_sqkm'].round()
data['population_density_sqkm_borough']=data['loac_POPDEN_sqkm'].astype(int)
import seaborn as sns
sns.set()

# Load the example flights dataset and conver to long-form
map_tree = data.pivot("Borough", "Rating", "loac_POPDEN_sqkm")

# Draw a heatmap with the numeric values in each cell
sns.heatmap(map_tree, annot=False,annot_kws={"size": 7})



