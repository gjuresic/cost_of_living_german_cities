import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from src.cost_of_living_dashboard.preprocessing import get_df, merge_dfs, get_selected_properties, get_overall_costs, \
    get_difference_of_overall_costs, prepare_data_for_piechart, get_overall_monthly_cost_income

df = get_df()
df_merged = merge_dfs(df)
selected_properties = get_selected_properties()
df_all_costs = get_overall_costs(df_merged)
df_diff_in_costs = get_difference_of_overall_costs(df_merged)
df_pie_chart_one = prepare_data_for_piechart(df_merged)
df_pie_chart_two = prepare_data_for_piechart(df_merged)
df_all_cost_income = get_overall_monthly_cost_income(df_merged)

colors = ['#FF00FF', '#00FFFF', '#FFA500', '#FF1493', '#00FF7F', '#FFC0CB', '#00FF00', '#FFFF00', '#FF4500', '#9400D3',
          '#8A2BE2', '#00CED1', '#FF00FF', '#FF69B4', '#00FA9A', '#00BFFF', '#FF6347', '#32CD32', '#FFD700', '#BA55D3']

fig_income_cost = go.Figure(data=[go.Scatter(
    x=df_all_cost_income['Gross Income'],
    y=df_all_cost_income['Overall Monthly Costs'],
    mode='markers',
    text=df_all_cost_income['City'],
    name='Cities',
    marker=dict(
        size=10,
        color=colors
    )
)])

fig_income_cost.update_layout(
    font=dict(color='#e5e5e5', family='Poppins, sans-serif'),
    paper_bgcolor='#000000',
    plot_bgcolor='#000000',
    legend={
        'orientation': 'h',
        'bgcolor': '#000000',
        'xanchor': 'right', 'x': 0.6, 'y': 0},
    xaxis=dict(title='Gross Income'),
    yaxis=dict(title='Overall Monthly Costs'),
    margin=dict(t=30)
)
fig_income_cost.update_traces(textposition='top center')

app = Dash(__name__, title="Cost of Living in German Cities 🇩🇪",
           meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
        ],
            className="one-third column",
        ),
        html.Div([
            html.Div([
                html.H3("Cost of Living in German Cities 🇩🇪",
                        style={"margin-bottom": "0px", 'color': 'white',
                               'font-family': 'Poppins, sans-serif', 'font-weight': 'bold', 'font-size': '28px'}, ),
                html.H5("Your Estimator", style={"margin-top": "0px", 'color': 'white',
                                                 'font-family': 'Poppins, sans-serif', 'font-size': '22px'}),
            ])
        ], className="one-half column", id="title"),

        html.Div([
            html.P('Last Updated: ' + str(df['inserted_at'].iloc[-1]),
                   style={'color': 'green', 'fontSize': 10}),

        ], className="one-third column", id='title1'),

    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
            html.P(children='In which city do you currently live?',
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'margin': '0px 0px 30px 0px',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '16px'}
                   ),

            dcc.Dropdown(np.sort(df['city'].unique().tolist()),
                         value="Aachen",
                         id="city_one_dd",
                         clearable=False,
                         className='dcc_compon'),
        ], className="card_container three columns",
        ),
        html.Div([
            html.P(children='Where do you want to move to?',
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'margin': '0px 0px 30px 0px',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '16px'}
                   ),

            dcc.Dropdown(np.sort(df['city'].unique().tolist()),
                         value="Berlin",
                         id="city_two_dd",
                         clearable=False,
                         className='dcc_compon'
                         ),

        ], className="card_container three columns",
        ),
        html.Div([
            html.P(children=f"Total Monthly Costs for {df_all_costs['City'].iloc[-2]}",
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'margin': '0px 0px 30px 0px',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '16px'},
                   id='overall_costs_city_one_title'
                   ),
            html.P(f"{df_all_costs['Overall Monthly Costs'].iloc[-2]}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '26px'},
                   id='overall_costs_city_one'
                   ),

        ], className="card_container three columns",
        ),
        html.Div([
            html.P(children=f"Total Monthly Costs for {df_all_costs['City'].iloc[-1]}",
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'margin': '0px 0px 30px 0px',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '16px'},
                   id='overall_costs_city_two_title'
                   ),
            html.P(f"{df_all_costs['Overall Monthly Costs'].iloc[-1]}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '26px'},
                   id='overall_costs_city_two'
                   ),

        ], className="card_container three columns",
        ),
        html.Div([
            html.P(children=f"Percentage Difference between {df_all_costs['City'].iloc[-2]} and "
                            f"{df_all_costs['City'].iloc[-1]}",
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '16px'},
                   id='overall_percent_diff_title'
                   ),
            html.P(f"{df_diff_in_costs['diff'].iloc[-1]}",
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '26px'},
                   id='overall_costs_diff',
                   ),

        ], className="card_container three columns",
        ),

    ], className="row flex-display"),
    html.Div([
        html.Div(children=[
            html.P(f"Distribution of Total Monthly Costs for {df_all_costs['City'].iloc[-2]}",
                   className='fix_label',
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '20px'},
                   id='distribution_city_one'),
            dcc.Graph(
                id='pie_chart_city_one'),
        ], className="create_container six columns", id="pie_chart"),
        html.Div([
            html.P(f"Distribution of Total Monthly Costs for {df_all_costs['City'].iloc[-1]}",
                   className='fix_label',
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '20px'},
                   id='distribution_city_two'),
            dcc.Graph(
                id='pie_chart_city_two'),
        ], className="create_container six columns", id="pie_chart"),
    ], className="row flex-display"),
    html.Div([
        html.Div(children=[
            html.P("A Comparison of all Cities",
                   className='fix_label',
                   style={
                       'margin-bottom': '0px',
                       'textAlign': 'center',
                       'color': 'white',
                       'font-family': 'Poppins, sans-serif',
                       'font-weight': 'bold',
                       'font-size': '20px'},
                   id='income_vs_cost'),
            html.P("Total Monthly Costs vs. Average Gross Income per Capita (Nov 2021)",
                   className='fix_label',
                   style={
                       'margin-top': '0px',
                       'textAlign': 'center',
                       'color': 'white',
                       'font-family': 'Poppins, sans-serif',
                       'font-size': '20px'},
                   id='income_vs_cost'),
            dcc.Graph(
                figure=fig_income_cost),
        ], className="create_container six columns"),
        html.Div([
            html.Div(children=[
                html.P('I hope you enjoyed it!'),
                html.B(),
                html.P('Let me know what kind of additional information you would expect in such a dashboard. 🙌🏼'),
                html.B(),
                html.P("I'm looking forward hearing from you! 🤓"),
                html.B(),
                html.P("Send me your ideas via email to"),
                html.I("gjuresic[at]gmail.com")
            ],
                className='fix_label',
                style={'margin': '120px',
                       'textAlign': 'center',
                       'color': 'white',
                       'font-family': 'Poppins, sans-serif',
                       'font-size': '20px'},
                id='last_comment'),
        ], className="create_container six columns", ),
    ], className="row flex-display"),

])


@app.callback(
    Output(component_id='overall_costs_city_one', component_property='children'),
    [Input(component_id='city_one_dd', component_property='value'), ]
)
def update_cost_one(city_one):
    if city_one is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-2]
    else:
        selected_properties = get_selected_properties()
        df_copy = df_merged.copy(deep=True)
        df_copy_city_one = df_copy[['property', 'weight', city_one]]
        df_selected_city_one = df_copy_city_one.loc[df_copy_city_one['property'].isin(selected_properties)]
        df_selected_city_one['weighted_price'] = df_selected_city_one[city_one] * df_selected_city_one['weight']
        weighted_sum_city_one = round(df_selected_city_one['weighted_price'].sum(), 0)

        df_all_costs = pd.DataFrame({'City': [city_one],
                                     'Overall Monthly Costs': [weighted_sum_city_one]})
        df_all_costs['Overall Monthly Costs'] = df_all_costs['Overall Monthly Costs'].apply(
            lambda x: "{:.2f}€".format(x))

    return df_all_costs['Overall Monthly Costs'].iloc[-1]


@app.callback(
    Output(component_id='overall_costs_city_two', component_property='children'),
    [Input(component_id='city_two_dd', component_property='value'), ]
)
def update_cost_two(city_two):
    if city_two is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-1]
    else:
        selected_properties = get_selected_properties()
        df_copy = df_merged.copy(deep=True)
        df_copy_city_one = df_copy[['property', 'weight', city_two]]
        df_selected_city_one = df_copy_city_one.loc[df_copy_city_one['property'].isin(selected_properties)]
        df_selected_city_one['weighted_price'] = df_selected_city_one[city_two] * df_selected_city_one['weight']
        weighted_sum_city_one = round(df_selected_city_one['weighted_price'].sum(), 0)

        df_all_costs = pd.DataFrame({'City': [city_two],
                                     'Overall Monthly Costs': [weighted_sum_city_one]})
        df_all_costs['Overall Monthly Costs'] = df_all_costs['Overall Monthly Costs'].apply(
            lambda x: "{:.2f}€".format(x))

    return df_all_costs['Overall Monthly Costs'].iloc[-1]


@app.callback(
    Output(component_id='overall_costs_diff', component_property='children'),
    [Input(component_id='city_one_dd', component_property='value'),
     Input(component_id='city_two_dd', component_property='value')]
)
def update_cost_diff(city_one, city_two):
    if city_one is None or city_two is None:
        cost = df_diff_in_costs['diff'].iloc[-1]
    else:
        selected_properties = get_selected_properties()
        df_copy = df_merged.copy(deep=True)
        df_copy_city_one = df_copy[['property', 'weight', city_one]]
        df_selected_city_one = df_copy_city_one.loc[df_copy_city_one['property'].isin(selected_properties)]
        df_selected_city_one['weighted_price'] = df_selected_city_one[city_one] * df_selected_city_one['weight']
        weighted_sum_city_one = round(df_selected_city_one['weighted_price'].sum(), 0)

        df_copy_city_two = df_copy[['property', 'weight', city_two]]
        df_selected_city_two = df_copy_city_two.loc[df_copy_city_two['property'].isin(selected_properties)]
        df_selected_city_two.fillna(1, inplace=True)
        df_selected_city_two['weighted_price'] = df_selected_city_two[city_two] * df_selected_city_two['weight']
        weighted_sum_city_two = round(df_selected_city_two['weighted_price'].sum(), 0)

        diff_in_costs = round(((weighted_sum_city_one - weighted_sum_city_two) / weighted_sum_city_one) * 100, 2)
        df_diff_in_costs = pd.DataFrame({f'Percentage Difference between {city_one} and {city_two}': [diff_in_costs]})
        df_diff_in_costs['diff'] = df_diff_in_costs[f'Percentage Difference between {city_one} and ' \
                                                    f'{city_two}'].apply(lambda x: "{:.2f}%".format(x))

    return df_diff_in_costs['diff'].iloc[-1]


@app.callback(
    Output(component_id='overall_costs_city_one_title', component_property='children'),
    [Input(component_id='city_one_dd', component_property='value'), ]
)
def update_cost_one_title(city_one):
    if city_one is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-2]
    else:
        df_copy = df_merged.copy(deep=True)
        df_copy_city_one = df_copy[[city_one]]

        df_all_costs = pd.DataFrame({'City': [city_one]})

    return f"Total Monthly Costs for {df_all_costs['City'].iloc[-1]}"


@app.callback(
    Output(component_id='overall_costs_city_two_title', component_property='children'),
    [Input(component_id='city_two_dd', component_property='value'), ]
)
def update_cost_one_title(city_one):
    if city_one is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-2]
    else:
        df_all_costs = pd.DataFrame({'City': [city_one]})

    return f"Total Monthly Costs for {df_all_costs['City'].iloc[-1]}"


@app.callback(
    Output(component_id='distribution_city_one', component_property='children'),
    [Input(component_id='city_one_dd', component_property='value'), ]
)
def update_cost_one_title(city_one):
    if city_one is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-2]
    else:
        df_all_costs = pd.DataFrame({'City': [city_one]})

    return f"Distribution of Total Monthly Costs for {df_all_costs['City'].iloc[-1]}"


@app.callback(
    Output(component_id='distribution_city_two', component_property='children'),
    [Input(component_id='city_two_dd', component_property='value'), ]
)
def update_cost_one_title(city_one):
    if city_one is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-2]
    else:
        df_all_costs = pd.DataFrame({'City': [city_one]})

    return f"Distribution of Total Monthly Costs for {df_all_costs['City'].iloc[-1]}"


@app.callback(
    Output(component_id='overall_percent_diff_title', component_property='children'),
    [Input(component_id='city_one_dd', component_property='value'),
     Input(component_id='city_two_dd', component_property='value'), ]
)
def update_percent_diff_title(city_one, city_two):
    if city_one is None or city_two is None:
        cost = df_all_costs['Overall Monthly Costs'].iloc[-2]
    else:
        df_all_costs = pd.DataFrame({'City': [city_one, city_two]})

    return f"Percentage Difference between {df_all_costs['City'].iloc[-2]} and {df_all_costs['City'].iloc[-1]}"


@app.callback(
    Output(component_id='pie_chart_city_one', component_property='figure'),
    [Input(component_id='city_one_dd', component_property='value'), ]
)
def update_pie_chart1(city_one):
    if city_one is None:
        df_copy = df_pie_chart_one.copy(deep=True)
    else:
        df_copy = df_pie_chart_one.copy(deep=True)

        df_copy_city_one = df_copy[['category', 'weight', city_one]]
        df_copy_city_one['weighted_price'] = df_copy_city_one[city_one] * df_copy_city_one['weight']
        city_one_grouped = df_copy_city_one.groupby('category')['weighted_price'].sum().reset_index()

        accom = city_one_grouped[city_one_grouped['category'] ==
                                 'Accommodation (1 Bedroom in City Centre)']['weighted_price'].iloc[-1]
        food = city_one_grouped[city_one_grouped['category'] ==
                                'Food']['weighted_price'].iloc[-1]
        leisure = city_one_grouped[city_one_grouped['category'] ==
                                   'Leisure (Sports, Cinema, Restaurants)']['weighted_price'].iloc[-1]
        transport = city_one_grouped[city_one_grouped['category'] ==
                                     'Transportation']['weighted_price'].iloc[-1]
        internet = city_one_grouped[city_one_grouped['category'] ==
                                    'Wifi and Mobile Phone']['weighted_price'].iloc[-1]

        colors = ['#FFC107', '#4CAF50', '#03A9F4', '#9C27B0', '#E91E63']

        fig = go.Figure(data=[go.Pie(labels=['Accommodation (1 Bedroom in City Centre)', 'Food',
                                             'Leisure (Fitness Club, 1 x Cinema, 2 x Restaurants)',
                                             'Public Transportation', 'WiFi and Mobile Phone Contract'],
                                     values=[accom, food, leisure, transport, internet],
                                     marker=dict(colors=colors),
                                     hoverinfo='label+value+percent',
                                     textfont=dict(size=13, family='Poppins, sans-serif'),
                                     hole=.5,
                                     rotation=0
                                     )])

        fig.update_layout(
            font=dict(color='#e5e5e5', family='Poppins, sans-serif'),
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            legend={
                'orientation': 'h',
                'bgcolor': '#000000',
                'xanchor': 'right', 'x': 0.6, 'y': 0},
            margin=dict(t=30)
        )

    return fig


@app.callback(
    Output(component_id='pie_chart_city_two', component_property='figure'),
    [Input(component_id='city_two_dd', component_property='value'), ]
)
def update_pie_chart2(city_one):
    if city_one is None:
        df_copy = df_pie_chart_one.copy(deep=True)
    else:
        df_copy = df_pie_chart_one.copy(deep=True)

        df_copy_city_one = df_copy[['category', 'weight', city_one]]
        df_copy_city_one['weighted_price'] = df_copy_city_one[city_one] * df_copy_city_one['weight']
        city_one_grouped = df_copy_city_one.groupby('category')['weighted_price'].sum().reset_index()

        accom = city_one_grouped[city_one_grouped['category'] ==
                                 'Accommodation (1 Bedroom in City Centre)']['weighted_price'].iloc[-1]
        food = city_one_grouped[city_one_grouped['category'] ==
                                'Food']['weighted_price'].iloc[-1]
        leisure = city_one_grouped[city_one_grouped['category'] ==
                                   'Leisure (Sports, Cinema, Restaurants)']['weighted_price'].iloc[-1]
        transport = city_one_grouped[city_one_grouped['category'] ==
                                     'Transportation']['weighted_price'].iloc[-1]
        internet = city_one_grouped[city_one_grouped['category'] ==
                                    'Wifi and Mobile Phone']['weighted_price'].iloc[-1]

        colors = ['#FFC107', '#4CAF50', '#03A9F4', '#9C27B0', '#E91E63']

        fig = go.Figure(data=[go.Pie(labels=['Accommodation (1 Bedroom in City Centre)', 'Food',
                                             'Leisure (Fitness Club, 1 x Cinema, 2 x Restaurants)',
                                             'Public Transportation', 'WiFi and Mobile Phone Contract'],
                                     values=[accom, food, leisure, transport, internet],
                                     marker=dict(colors=colors),
                                     hoverinfo='label+value+percent',
                                     textfont=dict(size=13, family='Poppins, sans-serif'),
                                     hole=.5,
                                     rotation=0
                                     )])

        fig.update_layout(
            font=dict(color='#e5e5e5', family='Poppins, sans-serif'),
            paper_bgcolor='#000000',
            plot_bgcolor='#000000',
            legend={
                'orientation': 'h',
                'bgcolor': '#000000',
                'xanchor': 'right', 'x': 0.6, 'y': 0},
            margin=dict(t=30)
        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')
