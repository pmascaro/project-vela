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

# postcode_dir = postcode_data[ postcode_data['postcode'] == "W5 3NH" ].values[0]
# print( '{},{}'.format(postcode_dir[2],postcode_dir[3]) )


##########
##########
##########

# as per https://forum.switchdoc.com/thread/1698/dash-app-standard-error-message
# 200 level errors are not really errors but informational. 400 & 500 level are bad
import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)


app = dash.Dash()   #initialising dash app

# creating user input
app.layout = html.Div(
    [
    html.H1('Vela: Data-driven journeys harnessed by AI'),

    html.Br(),
    html.Br(),

    #----
    #
    # origin postcode
    #
    #----

    html.Div(
        [
        html.Label('Input your origin postcode here:'),

        dcc.Input(
            id = 'orig-postcode-input',
            placeholder = 'example postcode: N1 1SY',
            debounce = True, #  If True, changes to input will be sent back to the Dash server only on enter or when losing focus. If it's False, it will sent the value back on every change. IMPORTANT: debounce=True will trigger on <enter>
            type = 'text',
            value = ''
        )
    ]
    ),


    html.Br(),
    html.Div(id='orig-postcode-output')


]) # , className="container"

#----
#
# Getting lat,lon in the app
#
#-----
@app.callback(
    # getting a postcode and outputting its lat,lon: it will be printed in the app
    Output(component_id='orig-postcode-output', component_property='children'),
    [Input(component_id='orig-postcode-input', component_property='value')]
)
def update_output_div(input_value):
    
    # printing the postcode in the TERMINAL
    print(input_value)

    postcode_dir = postcode_data[ postcode_data['postcode'] == input_value ].values[0]

    # print latitude longitude in the TERMINAL
    print('{},{}'.format(postcode_dir[2],postcode_dir[3]) )

    return '{},{}'.format(postcode_dir[2],postcode_dir[3])


#---
#
# running app
#
#----

if __name__ == '__main__': 

    # Run this app with `python dash_app_vega_AI.py`
    # 
    # visit http://127.0.0.exi1:8050/ 
    # if running from here: Press CTRL+C to quit
    # change parameter port if needed
    app.run_server(port = 30072)