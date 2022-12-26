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

from flask import Flask, render_template, request
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
    # converting to uppercase in case it's postcode inserted in lowercase
    if postcode.islower() == True:
        postcode = postcode.upper()

    # slice dataframe, selecing postcode from function parameter
    mask = postcode_data['postcode'] == postcode

    # getting lat, lon from postcode
    try: 
        postcode_dir = postcode_data[ mask ].values[0]
        return '{},{}'.format(postcode_dir[2],postcode_dir[3])

    except IndexError:
        return None 
        
        # break
        # print('Postcode not found in database.')

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

# # focusing in getting information from one origin to LHR 
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

@app.route("/", methods=['GET', 'POST'])
def home():
    ####
    # Accessing HERE API
    ####
    
    # 1) Accessing HERE url
    # 2) Requesting a location with two postcodes
    # 3) Geting the response from HERE api

    # HERE url
    my_url = "https://transit.router.hereapi.com/v8/routes"

    # HERE token
    token = "eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJlMWVaQXRheTZaZFdBdU9vZmt1RSIsImlhdCI6MTY3MjA0MzgxOSwiZXhwIjoxNjcyMTMwMjE5LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLjdBU0xiU0F5dWpKZHhIM0tBTTZDUHcueG05Q3RoRmFRT05CandBZWlkX1o0ZjQ0dE9jRklSWlktVlNrQmRldmctR1NiWTZzejdFSGQzYUR5TEgtVFBKUXJhM2Z2V0ZlbU1ZTHc1VllUd0RsdWRSbk1iTW1WMjRIY2N1OFJZVTRGSHVyU1ctVVoyQy1jdXBEeUR4d1lORm5FU1ZrUkpnQjh4dGRsU3BZbW5OSGx6eWFCNC11blAwQTk2a0VIOVRKMVg0Lk5pTmpQZ0l4UGV5ZnBSeHdiUlg5QTJMb1VwNGV6cEQwZGUxMFV5TUswX0k.MS5-7CGLItdbPv9gdlwpaGGoKyA50FTDToHWiVhJraPrnRnEOQRTdfekA3KbU29g9y3x8S-7mqa2T3oRTQ9621pqPI2mkB7AXLw27_VqhraPRz48d7t7RHoMwL9fiVsfSSNZRMkf1e0I41d3tbdekd2d-2QI1ArlXmdt-dhAeG_netE5WhhzjZJcXp5r9ijGLtp5zzd7p4kqhRTUOgH5vMW_dfUI6oICefe4C3hT6FqWDKkPnMkkxe8Knfr16L7_Qr1jd2oReJrXRriKbZwvtR8lTPq5_bMlTeq6vOszmi2YLqWYVbbMLmbKiHz5LZorISlKxHFy9X9TntQaeNrQ8g"

    # headers parameter
    my_headers = {'Authorization' : 'Bearer '+token }

    # error_statement = [] # initialise empty list to be filled with possible errors from user's input
    # results = {} # initialise empty dictionary

    # initialise an empty list where we will save each of the information texts
    list_text_info = []

    if request.method == "POST":
        # get postcode that the user has entered
        print(request.form['postcode'])
        print( type(request.form['postcode']) )
        # try: # TODO - deal with errors in postcode!
            # postcode = request.form['postcode']
            # r = requests.get(postcode)
            # print(r.text)
        # except:
            # errors.append("Unable to get postcode. Please make sure it's valid and try again.")
            # return render_template('index.html', errors= errors)

        # if r: # if we get a valid postcode

        #----
        #
        # Get info for that specific postcode
        #
        #----

        # setting origin postcode - origin comes from user input box
        origin_postcode = request.form['postcode']
        
        # get lat and lon from formated postcode
        origin_latlon=get_direction(origin_postcode)
        
        # TODO - handle any error to make sure app doesn't break if it for example get direction doesn't work
        if origin_latlon is None:
            error_statement = "Please enter a correct postcode. Here is an example: W5 3NH"
            return render_template('index.html', error_statement=error_statement)

        # printing output of user form
        print(f"origin: {origin_latlon}")

        # loop through each destination
        for destination_latlon, airport_cd in zip(list_postcode_latlon, list_airports_code):
        

            my_query = {
                            'origin':origin_latlon,
                            'destination':destination_latlon
                        }

            print(my_query)            
            # request a response
            try:
                response = requests.get(url=my_url, headers=my_headers, params=my_query, timeout=6) 
            except ConnectTimeout:
                print(f'Request has timed out for {airport_cd} airport')
                break # terminates current loop and resumes execution at the next loop

            # Use the json module to load CKAN's (Comprehensive Knowledge Archive Network) response into a dictionary.
            data = response.json()
            # print(data)
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

        return render_template('index.html', list_text_info=list_text_info) #
    
    return render_template('index.html', list_text_info=list_text_info) #

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