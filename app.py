#---
# set development mode
# flask has its own built test server, we'll use it to see what we are doing
# to do that in the terminal we use:
#
# set FLAS_DEBUG=1
# flask run
# http://127.0.0.1:5000/
#
# it dissapears when you close the session
#---



#---
# key libraries
#---

from flask import Flask, render_template
import requests
from requests.auth import HTTPBasicAuth
import json # json it will come in handy when parsing the JSON output of an API

import pandas as pd
import os
from datetime import datetime

#-----
#
# References
#
#-----
# st.title('Vela AI: Data-driven journeys harnessed by AI')
# reference: https://dash.plotly.com/layout
# https://dash.plotly.com/dash-core-components/store

# input boxes: https://www.youtube.com/watch?v=VZ6IdRMc0RI
# outputs with many inputs: https://dash.plotly.com/basic-callbacks

# flask app (text preprocessing):https://realpython.com/flask-by-example-part-3-text-processing-with-requests-beautifulsoup-nltk/


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
list_airports_postcode = [lhr_postcode,lcy_postcode,lgw_postcode,ltn_postcode,stn_postcode,sen_postcode] # 

# initialise empty list
list_postcode_latlon = [] 

# for each postcode, return postcode information (including lat and lon)
for postcode in list_airports_postcode:
    
    # print(postcode)
    list_postcode_latlon.append( get_direction(postcode) )

####
# testing
####
####
# Accessing HERE API
####

# 1) Accessing HERE url
# 2) Requesting a location with two postcodes
# 3) Geting the response from HERE api

# HERE url
# my_url = "https://transit.router.hereapi.com/v8/routes"

# # HERE token
# token = "eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJlMWVaQXRheTZaZFdBdU9vZmt1RSIsImlhdCI6MTY3MTgzODc0NiwiZXhwIjoxNjcxOTI1MTQ2LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLlpCVTluMGh5ai1hYjU1Q2YwSlU2bkEuYWtuMUFYaU1SMlhTMVBvaFRDcHkxRnVsNHNTNFA5aGJOcHNUUkQ5aTFOMG9GMUxzd3pCNXlhNHBISHVtNWlsbzJTdnllOUtQNi05QXZrTDlhUzhWQ3BFWE9ZeGVtNzhtaTNTbm5RRWNna0FmdzllSWJqcWVVZ183NkNYdW9USUxyaWY2azVIN2swY1JhcU1hYncyV01YaGhvNWRJUXZjd3ZrdzNmRUlfUWdnLlNnczZaM1lQTHBZdnBSQkd6dkxGNVN3TFQ5RS1yN2EzUjEwQnBXRDZSbTg.EBNNd5LudRq9IAS6COxYfIjYRCq5fWXUXx3Yp85CAu1hXF1032VS53xaTDm1CaJLyq8p_u7iR9vk0-fPTzKJ0oemx_wYX1SnXOuVJj_SqkqQdT7BTTyzjQ7ufo14im8YI-o5EnXwSmXiK1JQUOGroDc8Qyu_l3PNwTScTVeayij_QFCW8gT_wGWOmj35vZm_h2A5MyB6ICI-Is0-g4h6hS3DgFYK1LWwnOOBUb5KGGbj4VGFawc2neuWIZgllDVnEF-PKgTZN0zNPHl-9b-H7m_PaijcYpUQqA9frnkfqwCt_qeOAWwQIR1Bfa1-d96tEp5fFMAyC1nPNt56MRBr5g"

# # headers parameter
# my_headers = {'Authorization' : 'Bearer '+token }

# # requesting a location - user input
# origin=get_direction("N1 1SY")

# # focusing in getting information from one origin to LHR - TODO: loop through all airports
# destination_latlon = list_postcode_latlon[0] # LHR only

# my_query = {
#                 'origin':origin,
#                 'destination':destination_latlon
#             }
        
# # request a response
# response =requests.get(url=my_url, headers=my_headers, params=my_query) 

# # Use the json module to load CKAN's (Comprehensive Knowledge Archive Network) response into a dictionary.
# data = response.json()

# # getting journey information and time to destination
# # dep_time =  data['routes'][0]['sections'][0]['departure']['time']
# dep_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
# arr_time = data['routes'][0]['sections'][len(data['routes'][0]['sections'])-1]['arrival']['time']

# dep_datetime = datetime.strptime(dep_time, '%Y-%m-%dT%H:%M:%SZ')
# arr_datetime = datetime.strptime(arr_time, '%Y-%m-%dT%H:%M:%SZ')

# diff = arr_datetime - dep_datetime 

# print( f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to destination to the airport is: {arr_datetime.time()}" )
# print(f"Time to destination: {diff} \n")

####
####
####


##########
# flask app
##########
# http://127.0.0.1:5000/


app = Flask(__name__) # 

@app.route("/")
def test():
    ####
    # Accessing HERE API
    ####
    
    # 1) Accessing HERE url
    # 2) Requesting a location with two postcodes
    # 3) Geting the response from HERE api

    # HERE url
    my_url = "https://transit.router.hereapi.com/v8/routes"

    # HERE token
    token = "eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJlMWVaQXRheTZaZFdBdU9vZmt1RSIsImlhdCI6MTY3MTgzODQ1MywiZXhwIjoxNjcxOTI0ODUzLCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLk54WEJPU1lOcGdnRWZCZ09PcFMzZmcuWXVVR1BCSkhiUXFYNjBVcDdhQ1FVREVLM2dhX3dyOGRzTm5TV3kwZnFwMGlTZHFWRjBjT3Y2YWpScGZsTGMweXpRQkVPRllmaXJtSEZudUs4VWJhMXJKbV9lUXhvS2ExRGQxTkU0MXBBTlAxeUFFZUY4Tm1lOWlLV0NEWGtIdU9YQ0JJRHBhNVV6Y1ExQV8yZUVhWDhLUzhvVWpTM0E0ajF5M3FwcFFBb1hFLl9YOTJ1eHJfSk1jUGtUYUtPelNoZGpXSXJXUFF2OW8weXFLRFotOVpMYU0.V7JwYSR_tqJ2iFoQPU31X9QsgA-71-QTjYl0Mq7UOAFPYpvBPoLebIuPEO5zWi5D1w6odS8au6O59DYyLDsgdWvsGxDxZdfw1urMsUjug8f_RK8-EJfBTSP0V3kvdjtPqrr7dYUEvDi3GQKbGnB_HdPs-AScuJMCWGiOPaCTt1CIs59SDp5IgQdjppAl34a7KdI6hbrFEcpRmWmAENu-PjdDRua3FLEz0reK1wkEZWUX7GvFA8vn8e4B2spkBdyWtBHnRYPAhbtBTdyOFJ1ErREaGxfoI0buaw7AgdUXJ-UI3vCcOrWluLnXLbmgHo38MSNKquqXOk91F2CntNdhwQ"

    # headers parameter
    my_headers = {'Authorization' : 'Bearer '+token }

    # requesting a location - user input. 
    # TODO use flask app (text preprocessing):https://realpython.com/flask-by-example-part-3-text-processing-with-requests-beautifulsoup-nltk/ 
    # and https://www.youtube.com/watch?v=9MHYHgh4jYc to get user input
    origin=get_direction("N1 1SY")

    # initialise an empty list where we will save each of the information texts
    list_text_info = []

    # loop through each destination
    for destination_latlon, airport_cd in zip(list_postcode_latlon, list_airports_code):
    

        my_query = {
                        'origin':origin,
                        'destination':destination_latlon
                    }
                
        # request a response
        response =requests.get(url=my_url, headers=my_headers, params=my_query) 

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

        list_text_info.append( f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to {airport_cd} is: {arr_datetime.time()}.{os.linesep} Time to destination: {diff}")

    return render_template('index.html', list_text_info = list_text_info)

#----
#
# Run app
#
#----

# if __name__ == '__main__': 

#     # visit http://127.0.0.exi1:8050/ 
#     # if running from here: Press CTRL+C to quit
#     # change parameter port if needed
#     app.run(debug=True)