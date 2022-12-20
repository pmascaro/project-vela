import dash
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# importing the requests library
import requests
from requests.auth import HTTPBasicAuth

# datatime
from datetime import datetime

# json it will come in handy when parsing the JSON output of the API
import json

# to add new lines to f-strings
newline = '\n'

# st.title('Vela AI: Data-driven journeys harnessed by AI')
# reference: https://dash.plotly.com/layout
# https://dash.plotly.com/dash-core-components/store

# input boxes: https://www.youtube.com/watch?v=VZ6IdRMc0RI
# outputs with many inputs: https://dash.plotly.com/basic-callbacks


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

#----
# getting postcode information for each of the airports
#----
lhr_postcode = "TW6 2GA"
lcy_postcode = "E16 2PX"
lgw_postcode = "RH6 0NP"
ltn_postcode = "LU2 9QT"
stn_postcode = "CM24 1RW"
sen_postcode = "SS2 6YF"

list_airports_code = ['LHR','LCY','LGW','LTN','STN','SEN'] # 
list_airports_postcode = [lhr_postcode,lcy_postcode,lgw_postcode,ltn_postcode,stn_postcode,sen_postcode] # ,lgw_postcode,ltn_postcode,stn_postcode,sen_postcode

# initialise empty list
list_postcode_latlon = [] 

# for each postcode, return postcode information (including lat and lon)
for postcode in list_airports_postcode:
    
    # print(postcode)
    list_postcode_latlon.append( get_direction(postcode) )

# testing

# list_text_info = []
# list_text_info.append( f"Your departure time from origin is: and your arrival time to destination is:" )



##########
##########
##########

# as per https://forum.switchdoc.com/thread/1698/dash-app-standard-error-message
# 200 level errors are not really errors but informational. 400 & 500 level are bad
# import logging

# logging.getLogger('werkzeug').setLevel(logging.ERROR)


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

    #----
    #
    # dest postcode
    #
    #----

    # html.Div(
    #     [
    #     html.Label('Input your dest postcode here:'),

    #     dcc.Input(
    #         id = 'dest-postcode-input',
    #         placeholder = 'example postcode: N1 1SY',
    #         debounce = True, #  If True, changes to input will be sent back to the Dash server only on enter or when losing focus. If it's False, it will sent the value back on every change. IMPORTANT: debounce=True will trigger on <enter>
    #         type = 'text',
    #         value = ''
    #     )
    # ]
    # ),

    # print origin lat,lon
    # html.Br(),
    # html.Div(id='orig-postcode-output'),

    # print dest lat lon
    # html.Br(),
    # html.Div(id='dest-postcode-output')

    # print LHR info message
    html.Br(),
    html.Div(id='lhr-information-output'),

    # print LCY info message
    html.Br(),
    html.Div(id='lcy-information-output'),

    # print LGW info message
    html.Br(),
    html.Div(id='lgw-information-output'),

    # print LTN info message
    html.Br(),
    html.Div(id='ltn-information-output'),
    # print STN info message
    html.Br(),
    html.Div(id='stn-information-output'),

    # print SEN info message
    html.Br(),
    html.Div(id='sen-information-output')


]) # , className="container"

#----
#
# Getting lat,lon in the app
#
#-----


@app.callback(
    
    [Output(component_id='lhr-information-output', component_property='children'),
    Output(component_id='lcy-information-output', component_property='children'),
    Output(component_id='lgw-information-output', component_property='children'),
    Output(component_id='ltn-information-output', component_property='children'),
    Output(component_id='stn-information-output', component_property='children'),
    Output(component_id='sen-information-output', component_property='children')],

    Input(component_id='orig-postcode-input', component_property='value'),
    
    prevent_initial_call=True)
def update_output_div(input_orig_postcode):
    
    # if len(input_dest_postcode) != 0:
    
    # print(len(input_orig_postcode))
    # print(len(input_dest_postcode))

    # else:
    # printing the postcode in the TERMINAL
    print(f"orig postcode is: {input_orig_postcode}")
    # print(f"dest postcode is: {input_dest_postcode}")

    # getting postcode information (including lat, lon) for origin
    # postcode_dir_origin = postcode_data[ postcode_data['postcode'] == input_orig_postcode ].values[0]

    # getting postcode information for dest
    # postcode_dir_dest = [] # initialise empty list
    # for postcode in list_airports_postcode:
        # postcode_dir_dest.append( aux_postcode ) # append list 

    # print latitude longitude from origin in the TERMINAL
    # print('origin postcode lat, lon: {},{}'.format(postcode_dir_origin[2],postcode_dir_origin[3]) )
    # print('origin postcode lat, lon: {},{}'.format(postcode_dir_dest[2],postcode_dir_dest[3]) )

    # 1) Accessing HERE url
    # 2) Requesting a location with two postcodes
    # 3) Geting the response from HERE api

    # HERE url
    my_url = "https://transit.router.hereapi.com/v8/routes"

    # HERE token
    token = 'eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJlMWVaQXRheTZaZFdBdU9vZmt1RSIsImlhdCI6MTY3MTU0MDM1OCwiZXhwIjoxNjcxNjI2NzU4LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLi1EN3ZUZHBmLVlnTjlYcEltUEVpMXcueFB4eUduMFppVF9QWkp6RGdLRkprcEkzRUVsRk1xOXhfc2ozNWpFZmt2U24zam9mdnJWU2JJSDZDNi1PU1Zmb1lBRWxaNnVPM056dnVQTnZHTTBTUmxaU1hTYTQyLVV2dlc0U0JDeVVwQkg1U2Y5c24wZmlUY0ZabHBVUU9OLVBROGNiLUdEcmtzRGtNZEw2UmYwWHMyMUEtUXVCMGpib3ltX3dWQTAwRlY4LjFhc1RydW9kMnlWa0RtVlBwOURfdllCMlpLYjNMTThnTVZBT182RDEtTG8.ZMxtl4OcIhieNPISqlAq8Vxqh9Sz4mnATzjoDFaIeMC5xWB1KEAcWacqL1LKNsanF5oLkQsdqHOyBuLKd7qDN7i2mbPnDqnmI02JIAnk1deq1CBBabcSdh6JDbxNA35AvWlv2emxB5ajv6milB4YHRh7ZyzqrMegNw07iR8zZ6MDCa6zM48QlH3S72e9j_xKkeEiVOuPNFIJqB4q8pWuR67N6rcphIlCOJn7Nfd52nVIZgOEuITvnNjS8oXZf967jWoaUm4nUkwzGeWlkX4FnSdKF2nFN_ZFi0Ee6zVxDThyE12R1nqc6N3gcS6wNJA0EMhA9Y_T6-F6AIKlCrlEQw'

    # headers parameter
    my_headers = {'Authorization' : 'Bearer '+token } 

    # requesting a location - user input
    origin=get_direction(input_orig_postcode)

    #----
    # loop through each destination
    #----

    # initialise an empty list where we will save each of the information texts
    list_text_info = []

    # loop through each destination
    for destination_latlon, airport_cd in zip(list_postcode_latlon, list_airports_code):
    
        query = {
                    'origin':origin,
                    'destination':destination_latlon
                }
            
        # request a response
        response =requests.get(url=my_url, headers=my_headers, params=query) 

        # Use the json module to load CKAN's (Comprehensive Knowledge Archive Network) response into a dictionary.
        data = response.json()

        # getting journey information and time to destination
        # dep_time =  data['routes'][0]['sections'][0]['departure']['time']
        dep_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        arr_time = data['routes'][0]['sections'][len(data['routes'][0]['sections'])-1]['arrival']['time']

        dep_datetime = datetime.strptime(dep_time, '%Y-%m-%dT%H:%M:%SZ')
        arr_datetime = datetime.strptime(arr_time, '%Y-%m-%dT%H:%M:%SZ')

        diff = arr_datetime - dep_datetime 

        print( f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to destination to the airport is: {arr_datetime.time()}" )
        print(f"Time to destination: {diff} \n")

        list_text_info.append( f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to {airport_cd} is: {arr_datetime.time()}. Time to destination: {diff}" )

        # return f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to destination is: {arr_datetime.time()}. \n Time to destination: {diff}"

    # else:
        # return dash.no_update, dash.no_update
    
    #,  'Output: {}'.format(input_orig_postcode)

    #return 'origin postcode lat, lon: {},{}'.format(postcode_dir_origin[2],postcode_dir_origin[3]), 'dest postcode lat, lon: {},{}'.format(postcode_dir_dest[2],postcode_dir_dest[3]) 

    return list_text_info[0], list_text_info[1], list_text_info[2], list_text_info[3], list_text_info[4], list_text_info[5]
    # return f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to destination is: {arr_datetime.time()}. \n Time to destination: {diff}"

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
    app.run_server(port = 30080)


