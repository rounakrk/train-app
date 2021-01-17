import numpy as np
import pandas as pd
import json
import requests
import streamlit as st
import datetime
import PIL
from PIL import Image

def train_info():
    # "http://indianrailapi.com/api/v2/TrainInformation/apikey/<apikey>/TrainNumber/<TrainNumber>/"
    #Output
    # "{"ResponseCode":"200","Status":"SUCCESS","TrainNo":"12565","TrainName":"BIHAR SAMPAR","Source":{"Code":"DBG","Arrival":"08:35:00"},"Destination":{"Code":"NDLS","Arrival":"05:30:00"},"Message":null}"
    pass

def train_between_station():
    # "http://indianrailapi.com/api/v2/TrainBetweenStation/apikey/<apikey>/From/<From>/To/<To>"
    pass

def live_station():
    # "http://indianrailapi.com/api/v2/LiveStation/apikey/<apikey>/StationCode/<StationCode>/hours/<Hours>/"
    # hours should be either 2 or 4.
    pass

def tain_fare():
    # "http://indianrailapi.com/api/v2/TrainFare/apikey/<apikey>/TrainNumber/<trainNumber>/From/<stationFrom>/To/<stationTo>/Quota/<quota>"
    '''
    apikey : Your API key.
    trainNumber : Train Number.
    stationFrom : Source Station Code.
    stationTo : Destination Station Code.
    quota : GN/CK
    '''
    pass

def reading_json():
    df = pd.DataFrame(columns=["SerialNo","StationName","StationCode","Day","ScheduleArrival","ActualArrival","DelayInArrival","ScheduleDeparture","ActualDeparture","DelayInDeparture"])
    f = open('myfile.json',)
    data = json.load(f) 
    for i in data['TrainRoute']:
        df = df.append(i,ignore_index = True) 
        print(i) 
    # print(df.shape)
    f.close() 

    train_data = df.to_csv('train_current.csv', index = False) 
    # print('\nCSV String:\n', train_data)
    st.write(df)

def train(number,a):
    #http://indianrailapi.com/api/v2/livetrainstatus/apikey/<apikey>/trainnumber/<train_number>/date/<yyyymmdd>/
    api_key = "559ac2f3c195a6ab70770cde1eb18c97"
    # train_number = str(63513)
    train_number = number
    # date = "20210117"
    date = a
    url = "http://indianrailapi.com/api/v2/livetrainstatus/apikey/559ac2f3c195a6ab70770cde1eb18c97/trainnumber/"+train_number+"/date/"+date+"/"
    response = requests.get(url)
    status_get = response.content
    status_get = status_get.decode('utf-8')
    status_json = json.loads(status_get)
    # print(status_get)
    print(type(status_json))

    out_file = open("myfile.json", "w")    
    json.dump(status_json, out_file, indent = 6)      
    out_file.close() 

    print("Saving done ......")
    reading_json()



def gui():
    st.title("Indian Railway Train Current Status")

    train_url = "https://www.travelnewsdigest.in/wp-content/uploads/2013/11/indian-railways.jpg"
    im = Image.open(requests.get(train_url, stream=True).raw)
    im = im.resize((800,200))
    st.image(im, width = 700, )

    number = st.number_input('Train number')
    number = int(number)
    number = "0"*(5-len(str(number)))+str(number)
    st.write('Train number is ', number)

    d = st.date_input(
        "Journey Date",
        datetime.date(2021, 1, 17))
    d=str(d)
    a = ''.join(d.split('-'))
    # print(a)
    st.write('Journey Date :', a)

    left_column, right_column = st.beta_columns(2)
    pressed = left_column.button('Press me?')
    if pressed:
        right_column.write("Woohoo!")
        train(str(number),a)
    

if __name__=="__main__": 
    gui()