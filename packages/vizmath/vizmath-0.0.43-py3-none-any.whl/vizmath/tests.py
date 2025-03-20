#%%
from multichord_diagram import multichord
import pandas as pd

#%%
mc = multichord.random_multichord(num_sets=4, num_multisets=7, percent=75)
mc.multichord_plot(level=3)

#%%
data = [['a,b,d', .1], ['b,c', .1], ['b,d', .1], ['c', 1]]
data = [['a,b,d', .000001], ['b,c', .000001], ['b,d', .000001], ['c', .000001]]
df = pd.DataFrame(data, columns = ['multiset', 'value'])
mc = multichord(df, multiset_field='multiset', value_field='value', percent=50., rotate_deg=0) #order = 'b,c,d,a',
mc.multichord_plot(level = 3, transparency = 0.5)

#%%
mc.o_multichord.df.head()

#%%
mc.upset_df.head()