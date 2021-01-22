#import libraries
import os
import datetime
import warnings
import calendar
import random 
import wikipedia
import geocoder
import requests, json
import pyttsx3
import audio_manager as Audio
import input_manager as Parser

warnings.filterwarnings('ignore')


class Annie:


    def __init__(self):
        self.engine = pyttsx3.init()
        self.audio = Audio.AudioManager()
        self.parser = Parser.InputManager()
        self.name = 'user'
        self.weatherKey = 'de2411c4d0cdca5f3f257bc5bf135675'
        self.weatherUrl = "http://api.openweathermap.org/data/2.5/weather?"
        self.regexFunction = {
            'greet' : "(hello|hi|hey) (Annie|any)",
            'good morning' : 'good morning (Annie|any)|good morning',
            'my name' : 'my name is [A-Za-z]+$',
            'exit' : 'exit.*|bye.*|bye bye.*|see you.*',
            'weather': '.*weather.*'

        }

    def assistantResponse(self, text):
        self.engine.say("la pinga mia pal pussy tuyo")
        #myobj = gTTS(text=text, lang='en', slow=False)
        #myobj.save('response.mp3')
        #os.system('ffplay response.mp3')

    def parseInput(self):
        self.engine.say("la pinga mia pal pussy tuyo")
        audio = self.audio.recordAudio()
        while self.parser.parse(self.regexFunction["exit"], audio) == None:
            if self.parser.parse(self.regexFunction["good morning"], audio):
                self.assistantResponse('Good morning ' + self.name)
            elif self.parser.parse(self.regexFunction["my name"], audio):
                self.name = audio.split()[-1]
                self.assistantResponse('Hi ' + self.name)
            elif self.parser.parse(self.regexFunction["weather"], audio):
                location = geocoder.ip('me')
                self.weather(location.city)
            audio = self.audio.recordAudio() 

    def weather(self, city):
        # complete url address 
        complete_url = self.weatherUrl + "appid=" + self.weatherKey + "&q=" + city 
  
        # get method of requests module 
        # return response object 
        response = requests.get(complete_url) 
  
        # json method of response object  
        # convert json format data into 
        # python format data 
        jsonResponse = response.json() 
  
        # Now x contains list of nested dictionaries 
        # Check the value of "cod" key is equal to 
        # "404", means city is found otherwise, 
        # city is not found 
        if jsonResponse["cod"] != "404": 
  
            # store the value of "main" 
            # key in variable y 
            weatherInfo = jsonResponse["main"] 
  
            # store the value corresponding 
            # to the "temp" key of y 
            current_temperature = weatherInfo["temp"] 
            current_temperature = int(current_temperature - 273.15)
  
            # store the value corresponding 
            # to the "pressure" key of y 
            current_pressure = weatherInfo["pressure"] 
  
            # store the value corresponding 
            # to the "humidity" key of y 
            current_humidiy = weatherInfo["humidity"] 
      
            # store the value of "weather" 
            # key in variable z 
            descriptionDict = jsonResponse["weather"] 
              
            # store the value corresponding  
            # to the "description" key at  
            # the 0th index of z 
            weather_description = descriptionDict[0]["description"] 
      
            # print following values 
            self.assistantResponse(" Temperature is " +
                            str(current_temperature) + 
                  "\n atmospheric pressure is " +
                            str(current_pressure) +
                  "\n humidity is " +
                            str(current_humidiy) +
                  "\n Today the weather is " +
                            str(weather_description)) 
          
        else: 
            self.assistantResponse(" City Not Found ") 
