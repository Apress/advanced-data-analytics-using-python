import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('longley.csv', index_col=0)
#print df
b = df.Employed  
A = df.GNP  
A = sm.add_constant(A)  

est = sm.OLS(b, A)
est = est.fit()
print est.summary()
