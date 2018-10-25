import numpy as np
from pandas import Series, DataFrame
import re

'''
Organiser les colonnes en wide :
dim1 - dim2 - dim3 - dim4 ... - dimN - valeur

Passer du long au wide => PIVOT
Passer du wide au long => MELT
'''

# Relevé de metriques - Temperature

# Creation du dataframe

# Pandas Pivot et Melt sur le DF

# df_piv = df.pivot
df_wide.columns
df_wide.index
df_wide.reset_index()
df_melt = pd.melt(df_wide.reset_index(), index=['day'], ['soleil','pluie'])