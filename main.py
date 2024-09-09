import pyttsx3
from datetime import datetime
import speech_recognition as sr
from random import choice
from utils import opening_text # type: ignore
from functions.online_ops import search_on_google, search_on_wikidata, search_on_wikipedia
import httpx


USERNAME = 'Usuario'
BOTNAME = 'Prometeo'


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 100.0)

# Set Voice (male)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

"""Usado para decir cualquier texto que le sea entregado"""
def speak(text):
    engine.say(text) # type: ignore
    engine.runAndWait() # type: ignore


"""Saluda al usuario de acuerdo al horario"""
def greet_user():    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Buenos días {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Buenas tardes {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Buenas noches {USERNAME}")
    speak(f"Yo soy {BOTNAME}. ¿Cómo puedo asistirle?")

"""Toma las entradas del usuario, las reconoce utilizando el módulo de reconocimiento de voz y lo transforma a texto"""
def take_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escuchando....')
        
        audio = r.listen(source)

    try:
        print('Reconociendo...')
        query = r.recognize_google(audio, language='es-MX')
        print(query)
        if 'para' in query or 'detente' in query:
            speak('¡Tenga un buen día señor!')
            exit()
    except Exception:
        speak('Disculpe, no he podido entender. ¿Podría decirlo de nuevo?')
        query = 'None'
    return query

if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()
        """ Busca la informacion  """
        #results = search_on_wikidata(query)
        #speak(f"De acuerdo con Wikidata, {results}")
        
        # Busca la información en Wikipedia
        wikipedia_results = search_on_wikipedia(query)
        speak(f"De acuerdo con la base de datos, {wikipedia_results}")
