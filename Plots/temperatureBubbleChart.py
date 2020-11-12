import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

df = pd.read_csv('../Datasets/Weather2014-15.csv')



# Removing empty spaces from State column to avoid errors
#df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Creating unrecovered column
#df['Unrecovered'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

# Removing China and Others from data frame
#df = df[(df['Country'] != 'China') & (df['Country'] != 'Others')]

# Creating sum of number of cases group by Country Column
new_df = df.groupby(['month',]).agg({"average_min_temp": 'mean', "average_max_temp": 'mean'}).reset_index()

#{'average_max_temp': 'sum', 'average_min_temp': 'sum'}).reset_index()

# Preparing data
data = [
go.Scatter(x=new_df['average_min_temp'], y=new_df['average_max_temp'], text=new_df['month'], mode='markers',
marker=dict(size=new_df['average_min_temp'], color=new_df['average_min_temp'], showscale=True))
]

# Preparing layout
layout = go.Layout(title='Temperatures Per Month', xaxis_title="Average Min",
yaxis_title="Average Max", hovermode='closest')

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='temperatureBubbleChart.html')