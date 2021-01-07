from builtins import float

from django.shortcuts import render
from django.http import HttpResponse

import os, folium
import numpy as np
from accounts import places # To get current place address

### ---------------------- Connect 2nd server ------------------
import pymysql
import mysql.connector
import paramiko
import pandas as pd
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder
from os.path import expanduser

#home = expanduser('~')
#mypkey = paramiko.RSAKey.from_private_key_file("C:/RSAkey/test.pem")
# if you want to use ssh password use - ssh_password='your ssh password', bellow

sql_hostname = '127.0.0.1'
sql_username = 'root'
sql_password = 'Admin1234@@'
sql_main_database = 'pets'
sql_port = 3306
ssh_host = '23.99.115.137'
ssh_user = 'thanhhuy98'
ssh_port = 22
sql_ip = '10.0.0.4'

with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username = ssh_user,
        #ssh_pkey=mypkey,
        ssh_password = 'thanhhuy98',
        remote_bind_address = (sql_hostname, sql_port)) as tunnel:
    # conn = pymysql.connect(host='127.0.0.1', user=sql_username,
    #       passwd=sql_password, db=sql_main_database,
    #      port=tunnel.local_bind_port)
    # Khuong : hello

    conn = mysql.connector.connect(
        user = sql_username,
        password = sql_password,
        host = '127.0.0.1',
        port = tunnel.local_bind_port,
        database = sql_main_database,
    )
    mycursor = conn.cursor()
    query = ''' SELECT DISTINCT Longitude FROM TRACKINGDATA WHERE Time > '15:45:00' AND Time <'15:46:00';'''
    query2 = '' 'SELECT * FROM TRACKINGDATA' ''
    mycursor.execute(query2)

    results = mycursor.fetchall()

    numpy_array = np.array(results)
    # trans = numpy_array.transpose()
    # results = trans.tolist()

my_coord = []
for item in numpy_array:
    a = item[2]/1000000
    b = item[3]/1000000

    my_coord.append([b, a])
### --------------------------------------------------------------------

# Create your views here.
def createMap():
    m = folium.Map(
        location = my_coord[0],
        zoom_start = 16)
    
    return m

def home(request):

    return location(request)



def location(request):

    # read real time data
    map = createMap()
    
    my_pos = [106.8051841, 10.87015844]
    my_address = places.locate((my_pos[0], my_pos[1]))
    
    folium.Marker(location = [my_pos[1], my_pos[0]], 
    popup="My location: "+ str(my_address),
    icon=folium.Icon(icon="globe")
    ).add_to(map)

    map = map._repr_html_()
    context = {"my_map": map}

    # threading.Timer(WAIT_SECONDS, location(request)).start()

    return render( request, "accounts/location.html", context)


def history(request):
    # coordinates=[(10.869372, 106.802441),(10.870220, 106.802323),(10.870531, 106.802017),(10.871734, 106.802795),(10.873451, 106.802814)]
    coordinates = my_coord
    map = createMap()
    folium.Marker(coordinates[0], popup="Starting point", icon=folium.Icon(color="green", icon="star")).add_to(map)
    folium.Marker(coordinates[-1], popup="Destination", icon=folium.Icon(color="red", icon="globe")).add_to(map)


    for i in range(len(coordinates)):
        t = results[i][4].strftime('%d/%m/%y')
        seconds = results[i][5].total_seconds()
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        h = "%d:%02d:%02d" % (hour, minutes, seconds)

        my_address = places.locate((coordinates[i][1], coordinates[i][0]))
        folium.CircleMarker(location = coordinates[i], radius=10, popup = (h, t, my_address), fill=True, fill_color="Blue").add_to(map)

    folium.PolyLine(coordinates, color="red", weight=2.5, opacity=1).add_to(map)

    map = map._repr_html_()
    context = {"my_map": map}

    return render( request, "accounts/navbar.html", context)

