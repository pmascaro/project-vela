import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px

# st.title('Vela AI: Data-driven journeys harnessed by AI')
# reference: https://dash.plotly.com/layout


app = dash.Dash()   #initialising dash app

# testing
# app.layout = html.Div([
#     html.H1('Stock Tickers'),
#     dcc.Dropdown(
#         id='my-dropdown',
#         options=[
#             {'label': 'Tesla', 'value': 'TSLA'},
#             {'label': 'Apple', 'value': 'AAPL'},
#             {'label': 'Coke', 'value': 'COKE'}
#         ],
#         value='TSLA'
#     ),
#     dcc.Graph(id='my-graph')
# ], className="container")



# creating user input
app.layout = html.Div([
    html.H1('Vela AI: Data-driven journeys harnessed by AI'),

    html.Br(),
    html.Br(),

    html.Label('Input your origin postcode here:'),

    dcc.Input(
        id = 'orig-postcode-input'
        placeholder = 'example postcode: N1 1SY',
        type = 'text',
        value = ''
    )


], className="container")

@app.callback(
    Output(component_id='orig-postcode-input', component_property='children'),
    Input(component_id='orig-postcode-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'

if __name__ == '__main__': 

    # Run this app with `python dash_app_vega_AI.py`
    # 
    # visit http://127.0.0.1:8050/ 
    app.run_server()