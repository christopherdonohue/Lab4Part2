import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Olympic2016Rio.csv')

# Sorting values and select 20 first value
new_df = df.sort_values(by=['Total'], ascending=[False]).head(20)

# Preparing data
trace1 = go.Bar(x=new_df['NOC'], y=new_df['Gold'], name='Gold',
marker={'color': '#FFD700'})
trace2 = go.Bar(x=new_df['NOC'], y=new_df['Silver'], name='Silver',
marker={'color': '#C0C0C0'})
trace3 = go.Bar(x=new_df['NOC'], y=new_df['Bronze'], name='Bronze',
marker={'color': '#8C7853'})
data = [trace1, trace2, trace3]

# Preparing layout
layout = go.Layout(title='2016 Olympics Medals Rio Top 20 Countries ', xaxis_title="Country",
                    yaxis_title='Number of Medals', barmode='stack')

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='olympicsStackBarchart.html')