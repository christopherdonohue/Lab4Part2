import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
from calendar import month_name

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Preparing data



new_df = df.groupby(['month','day']).agg({'month': 'min', 'day': 'min', 'record_max_temp': 'max'})

data = [go.Heatmap(x=new_df['day'],
y=new_df['month'],
z=new_df['record_max_temp'].values.tolist(),
colorscale='Jet')]

# Preparing layout
layout = go.Layout(title='Max Temperature on Days', xaxis_title="Day of Week",
yaxis_title="Month of Year")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='heatmap.html')