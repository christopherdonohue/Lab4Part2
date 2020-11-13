import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

df3 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df4 = pd.read_csv('../Datasets/Weather2014-15.csv')

app2 = dash.Dash()



# Olympic Bar Chart Data
obc_df = df3.sort_values(by='Total', ascending=[False]).head(20)
data_obc = [go.Bar(x=obc_df['NOC'], y=obc_df['Total'])]

# Olympic Stack Bar Chart Data
nosbc_df = df3.sort_values(by=['Total'], ascending=[False]).head(20)
trace1 = go.Bar(x=nosbc_df['NOC'], y=nosbc_df['Gold'], name='Gold',
marker={'color': '#FFD700'})
trace2 = go.Bar(x=nosbc_df['NOC'], y=nosbc_df['Silver'], name='Silver',
marker={'color': '#C0C0C0'})
trace3 = go.Bar(x=nosbc_df['NOC'], y=nosbc_df['Bronze'], name='Bronze',
marker={'color': '#8C7853'})
data = [trace1, trace2, trace3]
data_olympicstackbarchart = [trace1, trace2, trace3]

# Temperature Line Graph
df4['date'] = pd.to_datetime(df4['date'])
new_df4 = df4.groupby(['month',]).agg({"actual_max_temp": 'max'}).reset_index()
data_templinechart = [go.Scatter(x=new_df4['month'], y=new_df4['actual_max_temp'], mode='lines', name='max_temp')]

# Temperature Multi-Line Graph
df4['date'] = pd.to_datetime(df4['date'])
new_df = df4.groupby(['month',]).agg({"actual_max_temp": 'max', "actual_min_temp": 'min', "actual_mean_temp": 'mean'}).reset_index()
# Preparing data
trace1_tempmultiline = go.Scatter(x=new_df['month'], y=new_df['actual_max_temp'], mode='lines', name='max')
trace2_tempmultiline = go.Scatter(x=new_df['month'], y=new_df['actual_min_temp'], mode='lines',
name='min')
trace3_tempmultiline = go.Scatter(x=new_df['month'], y=new_df['actual_mean_temp'], mode='lines',
name='mean')
data_tempmultiline = [trace1_tempmultiline,trace2_tempmultiline,trace3_tempmultiline]

# Temperature Bubble Chart
bubble_df = df4.groupby(['month']).agg({"average_min_temp": 'mean', "average_max_temp": 'mean'}).reset_index()
data_tempbubble = [
go.Scatter(x=bubble_df['average_min_temp'], y=bubble_df['average_max_temp'], text=bubble_df['month'], mode='markers',
marker=dict(size=bubble_df['average_min_temp'], color=bubble_df['average_min_temp'], showscale=True))
]

# Temperature Heatmap
tempheatmap_df = df4.groupby(['month','day']).agg({'month': 'min', 'day': 'min', 'record_max_temp': 'max'})
data_tempheatmap = [go.Heatmap(x=tempheatmap_df['day'],
y=tempheatmap_df['month'],
z=tempheatmap_df['record_max_temp'].values.tolist(),
colorscale='Jet')]

app2.layout = html.Div(children=[
    html.H1(children='Python Dash Weather / Olympics',
            style={
                'textAlign': 'center',
                'color': '#006400',

            }
            ),

    html.Div('Web dashboard for 2016 Rio Olympics and 2014-2015 Weather Data', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
  html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#006400'}),
    html.Div('This bar chart represent the number of medals won by the top 20 countries in the 2016 Rio Olympics'),
    dcc.Graph(id='graph8',
              figure={
                  'data': data_obc,
                  'layout': go.Layout(title='Most Medals Per Country Olympics 2016',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'})

              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#006400'}),
    html.Div(
        'This stack bar chart represent the Types of medals won by each country and how many'),
    dcc.Graph(id='graph9',
              figure={
                  'data': data_olympicstackbarchart,
                  'layout': go.Layout(title='Medals won by top 20 countries 2016 Olympics Rio',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#006400'}),
    html.Div('This line chart represent the Max Temperature for every month from 2014-2015'),
    dcc.Graph(id='graph10',
              figure={
                  'data': data_templinechart,
                  'layout': go.Layout(title='Max Temperatures every month',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#006400'}),
    html.Div(
        'This line chart represent the Max, Min, and Mean Temperatures from 2014-2015'),
    dcc.Graph(id='graph11',
              figure={
                  'data': data_tempmultiline,
                  'layout': go.Layout(
                      title='Max, Min, Mean of Temperatures every month for 2 years',
                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#006400'}),
    html.Div(
        'This bubble chart represents Max and Min Temperatures per month from 2014-2015 (hover over bubble for month)'),
    dcc.Graph(id='graph12',
              figure={
                  'data': data_tempbubble,
                  'layout': go.Layout(title='Max and Min Temperatures per Month',
                                      xaxis={'title': 'Min Temp'}, yaxis={'title': 'Max Temp'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#006400'}),
    html.Div(
        'This heat map represent the recorded max temperatures for days of the week in each month of the years 2014-2015.'),
    dcc.Graph(id='graph13',
              figure={
                  'data': data_tempheatmap,
                  'layout': go.Layout(title='recoreded max temperatures',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month of Year'})
              }
              )
])

if __name__ == '__main__':
    app2.run_server()

