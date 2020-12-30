import speech_recognition as sr

def recordAudio():
    recognizer = sr.Recognizer();
    with sr.Microphone() as source:
        print('Say something')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        data = ''
        list = recognizer.recognize_google(audio,show_all=False, language='es-ES')                  # generate a list of possible transcriptions
        #list.popitem()
        data = list
        ################### Recorrer todas las transcripciones ###############
        #print("Possible transcriptions:")
        #for prediction, value in list.items():
        #     print(prediction, value)
        #     data = value
        #     for transciption in value:
        #         print(transciption["transcript"])
        ######################################################################
    except KeyError:
        print('I could not understand')
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand')
    except sr.RequestError as e:
        print('Request error from google speech recognition' + format(e))
    return data

text = recordAudio()
print(text)
