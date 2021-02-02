# import libraries
import datetime
import warnings
import calendar
import random
import wikipedia
import speech_recognition as sr
import requests, json
import pyttsx3
import nltk, re, pprint
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer
from nltk.stem import SnowballStemmer
import pywhatkit
# nltk.download('words') # Descomenta esto para que se descargue
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('wordnet')
from weather_request import WeatherRequest
import input_manager as parser

warnings.filterwarnings('ignore')

weatherKeyWords = ["temperature", "raining", "weather", "snowing"]
wikipediaKeyWords = ["mean", "tell", "know"]
youtubeKeyWords = ["youtube", "play"]

commands_key_words = {"WEATHER": ["temperature", "raining", "weather", "snowing"], "YOUTUBE": ["play", "youtube"]}
weatherGrammar = r"""
    WEATHER: {<NN><IN>?<NNP>}
             {<VBG><NNP>}
"""
youtubeGrammar = r"""
    YOUTUBE: {<NN.*><NNP><.*>*}
             {<NN|VB.*><.*>*<VBP|NN>}
             
"""


class Annie:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.__setEngine()
        self.parser = parser.InputManager()
        self.name = 'user'
        self.commands = {"WEATHER": self.weather, "YOUTUBE": self.youtube}
        self.weather_request = WeatherRequest()

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

    def youtube(self, chunk, keywords):
        print("reproducimos video")
        pywhatkit.playonyt("Xokas Barraquito")

    def weather(self, chunk, keywords):
        locations = []
        for word in chunk.subtrees(filter=lambda t: t.label() == 'GPE'):
            for location in word:
                locations.append(location[0])

        for location in locations:
            self.assistantResponse(self.weather_request.getWeather(location))


    # Search in the tagged tree if the label WEATHER has been set
    # in that case it checks the keywords and if match them it will
    # call the weather API
    def checkChunks(self, tagged_tree, ne_chunked_tree, label, pos_keywords):
        for subtree in tagged_tree.subtrees(filter=lambda t: t.label() == label):
            keywords = []
            print(subtree)
            for word in subtree:
                if type(word) is tuple:
                    if word[1] in pos_keywords and word[0].lower() in commands_key_words[label]:
                        keywords.append(word[0])
            if not keywords:
                print("no keywords found")
            if keywords:
                self.commands[label](subtree, keywords)



    def parseInput(self, phrase):
        clean_tagged = self.tokenize(phrase)
        print(clean_tagged)
        weather_chunked = self.__chunk(clean_tagged, weatherGrammar)
        self.checkChunks(weather_chunked, self.ne_chunk(clean_tagged), 'WEATHER', ['NN', 'VBG'])
        youtube_chunked = self.__chunk(clean_tagged, youtubeGrammar)
        self.checkChunks(youtube_chunked, self.ne_chunk(clean_tagged), 'YOUTUBE', ['NN', 'NNP', 'VB'])

    # We remove the stopwords of the sentence
    def __cleanInput(self, tokens):
        stop_words = set(stopwords.words('english'))
        return [w for w in tokens if not w in stop_words]

    # We obtain the lemma of each word
    def __lemmatisation(self, tokens):
        lemma = WordNetLemmatizer()
        return [lemma.lemmatize(w) for w in tokens]

    def __chunk(self, tokens, grammar):
        cp = nltk.RegexpParser(grammar)
        return cp.parse(tokens)

    def filt(self, x, chunk_word):
        return x.label() == chunk_word

    def ne_chunk(self, tagged):
        return nltk.ne_chunk(tagged)

    def tokenize(self, phrase):
        tokens = nltk.word_tokenize(phrase)
        clean_tokens = self.__cleanInput(tokens)
        lemmatisation = self.__lemmatisation(clean_tokens)
        tagged = nltk.pos_tag(lemmatisation)  # las clasificamos por verbo, sustantivo...
        return tagged  # Comprueba si hay nombres propios, de ciudades...
