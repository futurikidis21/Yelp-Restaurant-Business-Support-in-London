import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.spatial as sp
points=[]
for i,val in enumerate(clean_db.index):
    point=np.column_stack((clean_db.Longtitude[i],clean_db.Latitude[i]))
    points.append(point)
kdtrees=[sp.cKDTree(p) for p in points]
r = 0.01
points_within_r = np.zeros((len(kdtrees), len(kdtrees)), dtype=np.int)
for j in range(len(kdtrees)):
    for k in range(j+1, len(kdtrees)):
        points_within_r[j, k] = kdtrees[j].count_neighbors(kdtrees[k], r, 2)
        print (points_within_r[j, k])
points_within_r = points_within_r + points_within_r.T
test=points_within_r.sum(axis=0)
df=pd.DataFrame(data=test)
df.columns=['Nearby_Business_Count']
clean_db=clean_db.join(df)

