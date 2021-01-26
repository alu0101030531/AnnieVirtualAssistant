# import libraries
import datetime
import warnings
import calendar
import random
import wikipedia
import geocoder
import speech_recognition as sr
import requests, json
import pyttsx3
import nltk, re, pprint
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk.stem import SnowballStemmer
import spacy
# nltk.download('words') # Descomenta esto para que se descargue
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('wordnet')
import input_manager as parser

warnings.filterwarnings('ignore')


class Annie:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.__setEngine()
        self.parser = parser.InputManager()
        self.name = 'user'
        self.weatherKey = 'de2411c4d0cdca5f3f257bc5bf135675'
        self.weatherUrl = "http://api.openweathermap.org/data/2.5/weather?"

    # Sets the gtts voice and run the engine
    def __setEngine(self):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.runAndWait()

    # Starts the recording of audio and return the phrase the user said
    def recordAudio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say something')
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            phrase = ''
            phrase = recognizer.recognize_google(audio, show_all=False)  # generate a list of possible transcriptions
        except KeyError:
            print('I could not understand')
        except sr.UnknownValueError:
            print('I could not understand')
        except sr.RequestError as e:
            print('Request error from google speech recognition' + format(e))
        return str(phrase)

    # Play Annie response
    def assistantResponse(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def parseInput(self):
        audio = self.audio.recordAudio()
        # Todo esto habría que cambiarlo para que se haga con el nltk
        # while self.parser.parse(self.regexFunction["exit"], audio) is None:
        #    if self.parser.parse(self.regexFunction["good morning"], audio):
        #        self.assistantResponse('Good morning ' + self.name)
        #    elif self.parser.parse(self.regexFunction["my name"], audio):
        #        self.name = audio.split()[-1]
        #        self.assistantResponse('Hi ' + self.name)
        #    elif self.parser.parse(self.regexFunction["weather"], audio):
        #        location = geocoder.ip('me')
        #        self.weather(location.city)
        #    audio = self.audio.recordAudio()

    # We remove the stopwords of the sentence
    def __cleanInput(self, tokens):
        stop_words = set(stopwords.words('english'))
        return [w for w in tokens if not w in stop_words]

    # We obtain the lemma of each word
    def __lemmatisation(self, tokens):
        lemma = WordNetLemmatizer()
        return [lemma.lemmatize(w) for w in tokens]

    def __chunk(self, tokens):
        grammar = "WEATHER: {<NN><IN>?<GPE>}"
        cp = nltk.RegexpParser(grammar)
        return cp.parse(tokens)

    def filt(self, x):
        return x.label() == 'WEATHER'


    def tokenizeAndChunk(self, phrase):
        tokens = nltk.word_tokenize(phrase)
        clean_tokens = self.__cleanInput(tokens)
        lemmatisation = self.__lemmatisation(clean_tokens)
        tagged = nltk.pos_tag(lemmatisation)  # las clasificamos por verbo, sustantivo...
        # print(tagged)
        test = nltk.ne_chunk(tagged)  # Comprueba si hay nombres propios, de ciudades...
        test = self.__chunk(test)
        for subtree in test.subtrees(filter=self.filt):  # Generate all subtrees
            for word in subtree:
                print(word)

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
