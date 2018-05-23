import numpy as np 
from scipy import stats 
import pandas 
import matplotlib.pyplot as plt 
import statsmodels.api as sm

from statsmodels.graphics.api import qqplot

print sm.datasets.sunspots.NOTE

Number of Observation - 309 (Annual 1700 - 2008)
Number of Variable – 1
Variable name definitions::
SUNACTIVITY - Number of sunspots for each year
The data file contains a 'YEAR' variable that is not returned by load.

dta = sm.datasets.sunspots.load_pandas().data

dta.index = pandas.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
del dta["YEAR"]

