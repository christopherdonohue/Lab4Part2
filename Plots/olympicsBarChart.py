import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Olympic2016Rio.csv')

# Sorting values and select top 20 countries
new_df = df.sort_values(by='Total', ascending=[False]).head(20)

# Preparing data
data = [go.Bar(x=new_df['NOC'], y=new_df['Total'])]

# Preparing layout
layout = go.Layout(title='2016 Rio Olympics Total Medals', xaxis_title="Countries",
                   yaxis_title="Total Medals")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='olympicsBarChart.html')