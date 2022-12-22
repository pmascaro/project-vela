#---
# set development mode
# flask has its own built test server, we'll use it to see what we are doing
# to do that in the terminal we use:
#
# set FLASK_DEBUG=1
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
# lcy_postcode = "E16 2PX"
# lgw_postcode = "RH6 0NP"
# ltn_postcode = "LU2 9QT"
# stn_postcode = "CM24 1RW"
# sen_postcode = "SS2 6YF"

list_airports_code = ['LHR'] #  ,'LCY','LGW','LTN','STN','SEN'
list_airports_postcode = [lhr_postcode] # ,lcy_postcode,lgw_postcode,ltn_postcode,stn_postcode,sen_postcode

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
# token = "eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJlMWVaQXRheTZaZFdBdU9vZmt1RSIsImlhdCI6MTY3MTcyNzYxOSwiZXhwIjoxNjcxODE0MDE5LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLkF2bkg2MGFmdVZJRzlDOTlRMEtmVncuUlNsRjVCMHdVMEtfbG9lWERLTmNadGxBb3NOTHZSUnhyNXIzX0MweTVTbHNucjlKU1U0ckhRTTN6bWV6TlJVcm5ETmRXdlg0WXB6NElpRlluSV9YSmhicGo3bWNfOFZUTkdRUV9zYXZnQXUzRkVna1VoOGNBMmJfS09TdU5OcURUT1F2aTRFTGpLUFJENWs2LUVGM29DZ1F5ZTgxVm5TVXd3YzItNU0yZVdzLjJaTDhRYy1WYkZTM0J5SGVfUVRnXy1qTTFVTVBxUUNDb0FDV1EzdEhpSFU.k066p2aSBrnP7HXBiL6vSnaYkMxXbwBELuu1ME6WMr1GT_RvefiWSnmSotimn1Twm4mf9JGRi7xswfojXtDFQGhbcYAbWmlGGoutGMlyO3ChRaAD-nH90em3Eh2MwrBVaML5Z76pjVK75DiI0BlHdJIg0m6oeYX1sj5V_itZ7gFU-NsuqbuKULZv9ygH3g3Fzp2TSMYZIs2_DjyZ4WgkHnbCPQFQUYkQgLpBKLjEaYKbxGt8a0ftYE9QHy2ebyy5Xt-8NHTXFBFQBviMc8P28pewLj1ubfueZ5h0G9tDvXwde-GkKp6GDfqDMA_9W2csxuiiGauNiP5cW9OrZ7lTkw"
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

    # get postcode direction
    # print("\n")
    # print(get_direction(lhr_postcode))
    # print(get_direction(lcy_postcode))
    # print("\n")

    # airports_info = {
    #     'airport_cd' : list_airports_code,
    #     'airport_postcode' : list_airports_postcode
    # }
    # print(f"{airports_info} \n")

    ####
    # Accessing HERE API
    ####
    
    # 1) Accessing HERE url
    # 2) Requesting a location with two postcodes
    # 3) Geting the response from HERE api

    # HERE url
    my_url = "https://transit.router.hereapi.com/v8/routes"

    # HERE token
    token = "eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJlMWVaQXRheTZaZFdBdU9vZmt1RSIsImlhdCI6MTY3MTcyNzYxOSwiZXhwIjoxNjcxODE0MDE5LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLkF2bkg2MGFmdVZJRzlDOTlRMEtmVncuUlNsRjVCMHdVMEtfbG9lWERLTmNadGxBb3NOTHZSUnhyNXIzX0MweTVTbHNucjlKU1U0ckhRTTN6bWV6TlJVcm5ETmRXdlg0WXB6NElpRlluSV9YSmhicGo3bWNfOFZUTkdRUV9zYXZnQXUzRkVna1VoOGNBMmJfS09TdU5OcURUT1F2aTRFTGpLUFJENWs2LUVGM29DZ1F5ZTgxVm5TVXd3YzItNU0yZVdzLjJaTDhRYy1WYkZTM0J5SGVfUVRnXy1qTTFVTVBxUUNDb0FDV1EzdEhpSFU.k066p2aSBrnP7HXBiL6vSnaYkMxXbwBELuu1ME6WMr1GT_RvefiWSnmSotimn1Twm4mf9JGRi7xswfojXtDFQGhbcYAbWmlGGoutGMlyO3ChRaAD-nH90em3Eh2MwrBVaML5Z76pjVK75DiI0BlHdJIg0m6oeYX1sj5V_itZ7gFU-NsuqbuKULZv9ygH3g3Fzp2TSMYZIs2_DjyZ4WgkHnbCPQFQUYkQgLpBKLjEaYKbxGt8a0ftYE9QHy2ebyy5Xt-8NHTXFBFQBviMc8P28pewLj1ubfueZ5h0G9tDvXwde-GkKp6GDfqDMA_9W2csxuiiGauNiP5cW9OrZ7lTkw"
    # headers parameter
    my_headers = {'Authorization' : 'Bearer '+token }

    # requesting a location - user input
    origin=get_direction("N1 1SY")

    # focusing in getting information from one origin to LHR - TODO: loop through all airports
    destination_latlon = list_postcode_latlon[0] # LHR only

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

    text = f"Your departure time from origin is: {dep_datetime.time()} and your arrival time to {list_airports_code[0]} is: {arr_datetime.time()}.{os.linesep} Time to destination: {diff}"

    return render_template('index.html', text = text)

#----
#
# Run app
#
#----

# if __name__ == '__main__': 

#     # visit http://127.0.0.exi1:8050/ 
#     # if running from here: Press CTRL+C to quit
#     # change parameter port if needed
#     app.run()