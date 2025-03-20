#%%
from vizmath.multichord_diagram import multichord
import pandas as pd

#%%
mc = multichord.random_multichord(num_sets=4, num_multisets=7, percent=75)
mc.multichord_plot(level=3)

#%%
data = [['a,b,d', .1], ['b,c', .1], ['b,d', .1], ['c', 1]]
data = [['a,b,d', .000001], ['b,c', .000001], ['b,d', .000001], ['c', .000001]]
df = pd.DataFrame(data, columns = ['multiset', 'value'])
mc = multichord(df, multiset_field='multiset', value_field='value', percent=50., rotate_deg=-90) #order = 'b,c,d,a',
mc.multichord_plot(level = 3, transparency = 0.5)

#%%
mc.o_multichord.df.head()

#%%
mc.upset_df.head()


#%%
#Year,Month,Game,Value
import pandas as pd
import os
df = pd.read_csv(os.path.dirname(__file__) + '/vidgames.csv')
df = df[df["Value"].notna() & (df["Value"] != 0)]
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}
df["Month_Num"] = df["Month"].map(month_map)
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month_Num"].astype(str) + "-01")
min_date = df["Date"].min()
df["order_x"] = ((df["Date"].dt.year - min_date.year) * 12 +
    (df["Date"].dt.month - min_date.month)) + 1
df.head()

#%%
# from vizmath.stream_chart import stream
from stream_chart import stream
sc = stream(df, 'order_x', 'Game', 'Value', buffer=200000)
sc.stream_plot()

#%%
sc.stream_df().head(20)