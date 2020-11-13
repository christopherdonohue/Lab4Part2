import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/CoronavirusTotal.csv')
df2 = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df3 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df4 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
barchart_df = df1[df1['Country'] == 'US']
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['State'])['Confirmed'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['State'], y=barchart_df['Confirmed'])]

# Stack bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df['Unrecovered'] = stackbarchart_df['Confirmed'] - stackbarchart_df['Deaths'] - stackbarchart_df[
    'Recovered']
stackbarchart_df = stackbarchart_df[(stackbarchart_df['Country'] != 'China')]
stackbarchart_df = stackbarchart_df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Confirmed'], ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Unrecovered'], name='Under Treatment',
                              marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Recovered'], name='Recovered',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Deaths'], name='Deaths',
                              marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df2
line_df['Date'] = pd.to_datetime(line_df['Date'])
data_linechart = [go.Scatter(x=line_df['Date'], y=line_df['Confirmed'], mode='lines', name='Death')]

# Line Chart Olympics



# Multi Line Chart
multiline_df = df2
multiline_df['Date'] = pd.to_datetime(multiline_df['Date'])
trace1_multiline = go.Scatter(x=multiline_df['Date'], y=multiline_df['Death'], mode='lines', name='Death')
trace2_multiline = go.Scatter(x=multiline_df['Date'], y=multiline_df['Recovered'], mode='lines', name='Recovered')
trace3_multiline = go.Scatter(x=multiline_df['Date'], y=multiline_df['Unrecovered'], mode='lines', name='Under Treatment')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
bubble_df['Unrecovered'] = bubble_df['Confirmed'] - bubble_df['Deaths'] - bubble_df['Recovered']
bubble_df = bubble_df[(bubble_df['Country'] != 'China')]
bubble_df = bubble_df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['Recovered'],
               y=bubble_df['Unrecovered'],
               text=bubble_df['Country'],
               mode='markers',
               marker=dict(size=bubble_df['Confirmed'] / 200, color=bubble_df['Confirmed'] / 200, showscale=True))
]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['Day'],
                           y=df2['WeekofMonth'],
                           z=df2['Recovered'].values.tolist(),
                           colorscale='Jet')]

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


# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Coronavirus COVID-19 Global Cases -  1/22/2020 to 3/17/2020', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of confirmed cases in the first 20 countries of selected continent.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'Africa', 'value': 'Africa'},
            {'label': 'Europe', 'value': 'Europe'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Oceania', 'value': 'Oceania'},
            {'label': 'South America', 'value': 'South America'}
        ],
        value='Europe'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of confirmed cases in the first 20 states of the US.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases in The US',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Number of confirmed cases'})

              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the CoronaVirus deaths, recovered and under treatment of all reported first 20 countries except China.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Corona Virus Cases in the first 20 country expect China',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Number of cases'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the Corona Virus confirmed cases of all reported cases in the given period.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases From 2020-01-22 to 2020-03-17',
                                      xaxis={'title': 'Date'}, yaxis={'title': 'Number of cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represent the CoronaVirus death, recovered and under treatment cases of all reported cases in the given period.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Corona Virus Death, Recovered and under treatment Cases From 2020-01-22 to 2020-03-17',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Number of cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the Corona Virus recovered and under treatment of all reported countries except China.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases',
                                      xaxis={'title': 'Recovered Cases'}, yaxis={'title': 'under Treatment Cases'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represent the Corona Virus recovered cases of all reported cases per day of week and week of month.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Corona Virus Recovered Cases',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Week of Month'})
              }
              ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of medals won by the top 20 countries in the 2016 Rio Olympics'),
    dcc.Graph(id='graph8',
              figure={
                  'data': data_obc,
                  'layout': go.Layout(title='Most Medals Per Country Olympics 2016',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'})

              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
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
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the Max Temperature for every month from 2014-2015'),
    dcc.Graph(id='graph10',
              figure={
                  'data': data_templinechart,
                  'layout': go.Layout(title='Max Temperatures every month',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
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
    html.H3('Bubble chart', style={'color': '#df1e56'}),
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
    html.H3('Heat map', style={'color': '#df1e56'}),
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


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df1[df1['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['Country'])['Confirmed'].sum().reset_index()
    new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Corona Virus Confirmed Cases in '+selected_continent,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of confirmed cases'})}


if __name__ == '__main__':
    app.run_server()