import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# st.title('Vela AI: Data-driven journeys harnessed by AI')
# reference: https://dash.plotly.com/layout
# https://dash.plotly.com/dash-core-components/store

#-----
#
# Specifics functions for this project
#
#-----

postcode_data = pd.read_csv("ukpostcodes.csv")

def get_direction(postcode):
    """
    given a postcode, this function outputs the latitude and longitude
    """
    postcode_dir = postcode_data[ postcode_data['postcode'] == postcode ].values[0]
    return '{},{}'.format(postcode_dir[2],postcode_dir[3])


##########
##########
##########

app = dash.Dash()   #initialising dash app

# creating user input
app.layout = html.Div(
    [
    html.H1('Vela: Data-driven journeys harnessed by AI'),

    html.Br(),
    html.Br(),

    html.Div(
        [
        html.Label('Input your origin postcode here:'),

        dcc.Input(
            id = 'orig-postcode-input',
            placeholder = 'example postcode: N1 1SY',
            type = 'text',
            value = ''
        )
    ]
    ),


    html.Br(),
    html.Div(id='orig-postcode-output')
    # ,
    
    # dcc.Store(id='orig-lat-long-output')
    # ,

    # html.Br(),
    # html.Div(id='orig-lat-long-output')

]) # , className="container"

@app.callback(
    Output(component_id='orig-postcode-output', component_property='children'),
    [Input(component_id='orig-postcode-input', component_property='value')]
)
def update_output_div(input_value):
    my_orig_postcode = input_value
    return f'Output: {input_value}'

# geting lat, lon from postcode
# @app.callback(
#     Output(component_id='orig-lat-long-output', component_property='children'),
#     [Input(component_id='orig-postcode-output', component_property='value')]
# )
# def get_direction(input_value):
#     """
#     given a postcode, this function outputs the latitude and longitude
#     """
#     postcode_dir = postcode_data[ postcode_data['postcode'] == input_value ].values[0]
#     return '{},{}'.format(postcode_dir[2],postcode_dir[3])


# get_direction(my_orig_postcode)



if __name__ == '__main__': 

    # Run this app with `python dash_app_vega_AI.py`
    # 
    # visit http://127.0.0.exi1:8050/ 
    # if running from here: Press CTRL+C to quit
    # change parameter port if needed
    app.run_server(port = 30052)