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
import webbrowser as web
import requests
from lxml import html

warnings.filterwarnings('ignore')

commands_key_words = {"WEATHER": ["temperature", "raining", "weather", "snowing"], "YOUTUBE": ["play", "youtube"],
                      "GOOGLE": ["search", "google", "Google"], "WIKIPEDIA": ["look", "summarize", "for", "Wikipedia", "wikipedia"],
                      "LOCATION": ["location", "what"],
                      "HOUR": ["hour", "time"]}
weatherGrammar = r"""
    WEATHER: {<NN><IN>?<GPE>+}
             {<VBG><GPE>+}
"""
youtubeGrammar = r"""
    YOUTUBE: {<NN><ORGANIZATION | NNP><.*>*}
             {<NN><.*>*<ORGANIZATION | NNP>}
             
"""

# Search in google something
googleGrammar = r"""
    GOOGLE: {<NN.*><.*>*<NNP>}
"""

wikipediaGrammar = r"""
    WIKIPEDIA: {<NN.*><.*>*<NNP>}
               {<VB.*><.*>*<NNP>}
"""

locationGrammar = r"""
    LOCATION: {<NN.*><.*>*<NNP|NN>}
"""

hourGrammar = r"""
    HOUR: {<NN><GPE>}
"""

class Annie:
    def __init__(self):
        self.foundCommand = False
        self.engine = pyttsx3.init()
        self.__setEngine()
        self.name = 'user'
        self.commands = {"WEATHER": self.weather, "YOUTUBE": self.youtube, "GOOGLE": self.google, "WIKIPEDIA": self.wikipedia, "LOCATION": self.location, "HOUR": self.hour}
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
            recognizer.adjust_for_ambient_noise(source)
            self.assistantResponse('Say something')
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
        return str(phrase[0].lower() + phrase[1:])

    # Play Annie response
    def assistantResponse(self, text):
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def youtube(self, chunk, keywords):
        self.assistantResponse("Opening video on Youtube")
        video = []
        for word in chunk:
            if type(word) is tuple and word[0] not in commands_key_words["YOUTUBE"]:
                video.append(word[0])
        separator = ' '
        pywhatkit.playonyt(separator.join(video))

    def google(self, chunk, keywords):
        print("Buscando en google")
        toSearch = []
        for word in chunk:
            if word[0] not in commands_key_words["GOOGLE"]:
                toSearch.append(word[0])
        separator = ' '
        pywhatkit.search(separator.join(toSearch))

    def googleDefault(self, phrase):
        pywhatkit.search(phrase)

    def wikipedia(self, chunk, keywords):
        wikipedia.set_lang("en")
        print("Buscando en wikipedia")
        url = 'https://es.wikipedia.org/wiki/'
        toSearch = []
        for word in chunk:
            if word[0] not in commands_key_words["WIKIPEDIA"]:
                toSearch.append(word[0])
        newsearch = " ".join(toSearch)
        listofelements = wikipedia.search(newsearch)
        page = wikipedia.page(listofelements[0]).url
        web.open(page)

    def location(self, chunk, keywords):
        location = []
        for word in chunk:
            if word[0] not in commands_key_words["LOCATION"]:
                location.append(word[0])
        finalLocationsString = " ".join(location)
        url = 'https://google.es/maps/place/' + finalLocationsString + '/&amp'
        web.open(url)

    # Access the TimeZone API and request the hour in a location
    def hour(self, chunk, keywords):
        country = ''
        for word in chunk.subtrees(filter=lambda tagged: tagged.label() == 'GPE'):
            for location in word:
                country = location[0]
        page_content = requests.get(
            'https://www.timeanddate.com/worldclock/' + country
        )
        tree = html.fromstring(page_content.content)
        variable = tree.xpath("/html/body/main/article/section[1]/div[1]/div/span[1]/text()")
        self.assistantResponse(" ".join(variable).replace(':', ' '))

    # Access weather API and request the weather for a location
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
    def checkChunks(self, tagged_tree, label, pos_keywords):
        if not self.foundCommand:
            for subtree in tagged_tree.subtrees(filter=lambda t: t.label() == label):
                keywords = []
                print(subtree)
                for word in subtree:
                    if type(word) is tuple:
                        if word[1] in pos_keywords and word[0].lower() in commands_key_words[label]:
                            keywords.append(word[0])
                    else:
                        for sub_chunk_word in word:
                            if sub_chunk_word[1] in pos_keywords and sub_chunk_word[0].lower() in commands_key_words[label]:
                                keywords.append(sub_chunk_word[0])

                if keywords:
                    self.commands[label](subtree, keywords)
                    self.foundCommand = True

    def parseInput(self, phrase):
        self.foundCommand = False
        clean_tagged = self.tokenize(phrase)
        print(clean_tagged)
        weather_chunked = self.__chunk(self.ne_chunk(clean_tagged), weatherGrammar)
        self.checkChunks(weather_chunked, 'WEATHER', ['NN', 'VBG'])
        youtube_chunked = self.__chunk(clean_tagged, youtubeGrammar)
        self.checkChunks(youtube_chunked, 'YOUTUBE', ['NN', 'NNP', 'VB'])
        google_chunked = self.__chunk(clean_tagged, googleGrammar)
        self.checkChunks(google_chunked, 'GOOGLE', ['NN', 'NNP', 'NNP'])
        wiki_chunked = self.__chunk(clean_tagged, wikipediaGrammar)
        self.checkChunks(wiki_chunked, 'WIKIPEDIA', ['NN', 'NNP', 'VB'])
        location_chunked = self.__chunk(clean_tagged, locationGrammar)
        self.checkChunks(location_chunked, 'LOCATION', ['NN', 'NNP'])
        hour_chunked = self.__chunk(self.ne_chunk(clean_tagged), hourGrammar)
        self.checkChunks(hour_chunked, 'HOUR', ['NN'])
        if not self.foundCommand:
            if phrase == "are you okay" or phrase == "annie are you okay":
                self.assistantResponse("I've been hit by, I've been struck by, a smooth criminal")
            else:
                self.googleDefault(phrase)

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

