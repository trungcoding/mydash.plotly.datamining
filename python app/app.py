from datetime import date, datetime
import dash
from dash import Dash, Input, Output, dcc, html, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_csv("tempareture.csv")
mark_values = {2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020',2021:'2021',2022:'2022'}
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sự thay đổi nhiệt độ của Việt Nam giai đoạn 2013-2022", style={'textAlign': 'center'}),
    html.H2("Nhiệt độ của một ngày", style={'textAlign': 'center'}),
    html.H3("Ngày"),
    dcc.DatePickerSingle(
        id='my-date-picker',
        min_date_allowed=date(2013, 9, 1),
        max_date_allowed=date(2022, 9, 30),
        initial_visible_month=date(2013, 9, 1),
        date=date(2013, 9, 1)
    ),
    dcc.Graph(figure={}, id= 'theo_ngay'),

    html.H2("Nhiệt độ ngày tháng", style={'textAlign': 'center'}),
    html.H3("Ngày"),
    dcc.Dropdown(
        options= df['Day'].unique(),
        value=1,
        id='chose_day'),
    html.H3("Tháng"),
    dcc.Dropdown(
        options= df['Month'].unique(),
        value=9,
        id='chose_month1'),
    dcc.Graph(figure={}, id='date_chosen'),

    html.H2("Nhiệt độ theo tháng", style={'textAlign': 'center'}),
    html.H3("Tháng"),
    dcc.Dropdown(
        options= df['Month'].unique(),
        value=9,
        id='chose_month'),
    html.H3("Nhiệt độ"),
    dcc.RadioItems(
        id='chon_temperature',
        options=[{'label': html.Div(['Maximum Temperature'], style={'color': '#6600FF', 'font-size': 15}), 'value': 'Maximum Temperature'},
                {'label': html.Div(['Average Temperature'], style={'color': 'red', 'font-size': 15}), 'value': 'Average Temperature'},
                {'label':  html.Div(['Minimum Temperature'], style={'color': '#00CC00', 'font-size': 15}), 'value': 'Minimum Temperature'},],
        value= 'Average Temperature'),
    dcc.Graph(figure={}, id='theo_thang'),

    html.H2("Nhiệt độ theo năm (Dạng Cột -Bar)", style={'textAlign': 'center'}),
    html.H3("Năm"),
    dcc.Dropdown(
        options= df['Year'].unique(),
        value=2013,
        id='chose_year'),
    dcc.Graph(figure={}, id='theo_nam'),

    html.H2("Nhiệt độ nhiều năm", style={'textAlign': 'center'}),
    html.H3("Nhiệt độ"),
    dcc.Checklist([
        {
            "label": html.Div(['Maximum Temperature'], style={'color': 'Purple', 'font-size': 20}),
            "value": "Maximum Temperature",
        },
        {
            "label": html.Div(['Average Temperature'], style={'color': 'MediumTurqoise', 'font-size': 20}),
            "value": "Average Temperature",
        },
        {
            "label": html.Div(['Minimum Temperature'], style={'color': 'LightGreen', 'font-size': 20}),
            "value": "Minimum Temperature",
        }], value=['Minimum Temperature'],
        id='chose_nhietdo',
    ),
    dcc.Graph(figure={}, id='theo_nhieu_nam'),
    html.H3("Giai đoạn"),
    dcc.RangeSlider(
        id='the_years',
        min=2013,
        max=2022,
        value=[2013, 2022],
        marks=mark_values,
        step=None
    ),
])

@callback(
    Output('theo_ngay', 'figure'),
    Input('my-date-picker', 'date')
)
def update_graph(date_value):
    if date_value:
        date_value = datetime.strptime(date_value, '%Y-%m-%d').strftime('%Y-%m-%d')
        df1 = df[df['Date'] == date_value]
        df5 = df1.loc[:,["Average Temperature","Minimum Temperature","Maximum Temperature"]]
        df5 = df5.transpose()
        mybox = px.box(df5
        )
        mybox['layout'].update(height=800, width=800)
        return mybox
    else:
        dash.no_update()

@app.callback(
    Output('date_chosen', 'figure'),
    Input('chose_day', 'value'),
    Input('chose_month1', 'value')
)
def build_graph(day_chosen, month_chosen):
    df6 = df[(df['Day'] == day_chosen) & (df['Month'] == month_chosen)]
    df6 = df6.loc[:, ["Average Temperature", "Minimum Temperature", "Maximum Temperature"]]
    df6 = df6.transpose()
    mybox = px.box(df6)
    mybox.update_layout(
        xaxis_title="Năm",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    mybox.update_xaxes(visible=False)
    return mybox


@app.callback(
    Output('theo_thang', 'figure'),
    Input('chose_month', 'value'),
    Input('chon_temperature', 'value')
)
def build_graph(month_chosen, temperature_chosen):
    df_2013 = df[(df['Year'] == 2013) & (df['Month'] == month_chosen)]
    df_2014 = df[(df['Year'] == 2014) & (df['Month'] == month_chosen)]
    df_2015 = df[(df['Year'] == 2015) & (df['Month'] == month_chosen)]
    df_2016 = df[(df['Year'] == 2016) & (df['Month'] == month_chosen)]
    df_2017 = df[(df['Year'] == 2017) & (df['Month'] == month_chosen)]
    df_2018 = df[(df['Year'] == 2018) & (df['Month'] == month_chosen)]
    df_2019 = df[(df['Year'] == 2019) & (df['Month'] == month_chosen)]
    df_2020 = df[(df['Year'] == 2020) & (df['Month'] == month_chosen)]
    df_2021 = df[(df['Year'] == 2021) & (df['Month'] == month_chosen)]
    df_2022 = df[(df['Year'] == 2022) & (df['Month'] == month_chosen)]
    fig = make_subplots(rows = 5, cols= 2,
                        subplot_titles=('Năm 2013', 'Năm 2018', 'Năm 2014','Năm 2019', 'Năm 2015', 'Năm 2020','Năm 2016', 'Năm 2021', 'Năm 2017','Năm 2022'))
    fig.add_trace(go.Bar(
        x= df_2013['Date'],
        y= df_2013[temperature_chosen]),1,1)
    fig.add_trace(go.Bar(
        x= df_2014['Date'],
        y= df_2014[temperature_chosen]),2,1)
    fig.add_trace(go.Bar(
        x= df_2015['Date'],
        y= df_2015[temperature_chosen]),3,1)
    fig.add_trace(go.Bar(
        x= df_2016['Date'],
        y= df_2016[temperature_chosen]),4,1)
    fig.add_trace(go.Bar(
        x= df_2017['Date'],
        y= df_2017[temperature_chosen]),5,1)
    fig.add_trace(go.Bar(
        x= df_2018['Date'],
        y= df_2018[temperature_chosen]),1,2)
    fig.add_trace(go.Bar(
        x= df_2019['Date'],
        y= df_2019[temperature_chosen]),2,2)
    fig.add_trace(go.Bar(
        x= df_2020['Date'],
        y= df_2020[temperature_chosen]),3,2)
    fig.add_trace(go.Bar(
        x= df_2021['Date'],
        y= df_2021[temperature_chosen]),4,2)
    fig.add_trace(go.Bar(
        x= df_2022['Date'],
        y= df_2022[temperature_chosen]),5,2)
    fig['layout'].update(height=1000, width=2000, showlegend=False)
    return fig

@app.callback(
    Output(component_id='theo_nam', component_property='figure'),
    [Input(component_id='chose_year', component_property='value')]
)
def build_graph(year_chosen):
    df3 = df[df['Year'] == year_chosen]

    fig = make_subplots(rows=3 , cols=1,
                        # shared_xaxes=True,
                        subplot_titles=('Maximum Temperature', 'Average Temperature', 'Minimum Temperature'))
    fig.add_trace(go.Bar(
        name='Max',
        x=df3['Date'],
        y= df3['Maximum Temperature']), 1, 1)
    fig.add_trace(go.Scatter(
        name='Ave',
        x=df3['Date'],
        y= df3['Average Temperature'],
        mode='markers'), 2, 1)
    fig.add_trace(go.Scatter(
        name='Min',
        x=df3['Date'],
        y= df3['Minimum Temperature']), 3, 1)
    fig['layout'].update(height=1000, width=2000)
    return fig


@app.callback(
    Output('theo_nhieu_nam', 'figure'),
    [Input('the_years', 'value')],
    [Input('chose_nhietdo', 'value')]
)
def update_graph(years_chosen, chon_nhietdo):
    df4 = df[(df['Year'] >= years_chosen[0]) & (df['Year'] <= years_chosen[1])]

    stackplot = px.line(
        data_frame=df4,
        x="Date",
        y= chon_nhietdo,
        height=500
    )
    # stackplot.update_traces(textposition='top left')
    return (stackplot)

if __name__ == '__main__':
    app.run_server(debug=True)