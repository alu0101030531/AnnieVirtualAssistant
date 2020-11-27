#import libraries
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random 
import wikipedia
import 

warnings.filterwarnings('ignore')

# Principalmente tiene dos funciones recordAudio que pilla el audio del micro una vez pasa un treshold deja de pilar audio y lo devuelve como un string este string lo analizamos y en función de la consulta realizamos una acción
class Annie:
    def recordAudio(self):

    def assistantResponse(self, text):
        myobj = gTTS(text=text, lang='en', slow=False)
        myobj.save('assistant_response.mp3')
        os.system('ffplay assistant_response.mp3')

