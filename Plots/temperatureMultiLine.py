import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

df['date'] = pd.to_datetime(df['date'])
new_df = df.groupby(['month',]).agg({"actual_max_temp": 'max', "actual_min_temp": 'min', "actual_mean_temp": 'mean'}).reset_index()
# Preparing data
trace1 = go.Scatter(x=new_df['month'], y=new_df['actual_max_temp'], mode='lines', name='max')
trace2 = go.Scatter(x=new_df['month'], y=new_df['actual_min_temp'], mode='lines',
name='min')
trace3 = go.Scatter(x=new_df['month'], y=new_df['actual_mean_temp'], mode='lines',
name='mean')
data = [trace1,trace2,trace3]

# Preparing layout
layout = go.Layout(title='Actual Max, Min, and Mean Temperature of Each Month', xaxis_title="Month",
                    yaxis_title="Temperature")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='temperatureMultiLine.html')