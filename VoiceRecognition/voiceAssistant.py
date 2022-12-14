# ----------------- REQUISITOS ---------------------------

## DEPENDENCIAS NECESARIAS
## pip install speechrecognition
## pip install pyaudio
## pip install pyttsx3

import speech_recognition as sr
import pyttsx3 as tts
import webbrowser

# ------------------ FUNCIONES -------------------------

# rate: velocidad al hablar
def speak(text):
    engine.setProperty('rate', 140) 
    engine.say(text)
    engine.runAndWait()

# Calibrar detalles
def calibrar():
    r.adjust_for_ambient_noise(source, duration=0.8) # Calibra el umbral de energía (sensibilidad del reconocedor) segun el ruido ambiental detectado.
    r.pause_threshold = 0.8 # Mínima cantidad de silencio que registrará como final de la frase.

# Pasar el audio en texto
def audioToText(sound):
    texto = r.recognize_google(sound, language='es-ES')
    texto = texto.lower()
    return texto

# crear archivo de texto
def createFile():
    fileName = useMic('Nombre el documento: ')
    if fileName[0] == 0:
        with open(f"{fileName[1]}.txt", "w") as f:
            fileContent = useMic('Díctame el contenido del documento: ')
            if fileContent[0] == 0:
                f.write(f"{fileContent[1]}")
                speak('Archivo de texto creado.')
            else:
                speak(f'{fileContent[1]}. Se ha creado un archivo de texto sin contenido.')
    else:
        speak(f'{fileContent[1]}. Inténtalo nuevamente.')

# leer contenido de un documento
def readFile():
    fileName = useMic('Nombre del documento a leer: ')
    if fileName[0] == 0:
        try:
            textInFile = open(f'{fileName[1]}.txt', "r")
            lines = textInFile.readlines()
            for line in lines:
                speak(line)
        except:
            speak(f'No exite un documento txt con el nombre {fileName[1]}')
    else:
        speak(f'{fileName[1]}. Inténtalo nuevamente.')

# abrir navegador
def openBrowser():
    url='https://www.google.co'
    webbrowser.open(url)
    speak('Se ha abierto el navegador y se ha redireccionado a la página de Google.')
    
# validar audio para las funciones anteriores
def useMic(line):
    with sr.Microphone() as source:
        calibrar()
        speak(f'{line}')
        audio = r.listen(source)
        try:
            text = audioToText(audio)
            print("Dijiste: {}".format(text))
            flag = 0
        except:
            text = "Lo siento, no pude entenderte."
            flag = 1
        return flag, text

# ----------- INICIAR PROGRAMA ---------------------

# Configurar voz
engine = tts.init()
voices = engine.getProperty('voices') # Información sobre la voz de un sintetizador de voz
engine.setProperty('voice', voices[2].id) # Cambiar voz
r = sr.Recognizer() # Iniciar reconocimiento

intro = 0 # para confirmar al usuario el inicio del programa

with sr.Microphone(device_index=1) as source:
    while True:
        calibrar()
        if intro == 0:
            speak('Programa cargado')
            intro = 1
        audio = r.listen(source)
        try:
            text = audioToText(audio)
            print("Dijiste: {}".format(text))
            if "sol" in text:
                calibrar()
                speak('Hola, ¿cómo puedo ayudarte?')
                audio = r.listen(source)
                try:
                    text = audioToText(audio)
                    print("Dijiste: {}".format(text))
                    if text == "crear texto":
                        createFile()
                    elif text == "leer texto":
                        readFile()
                    elif text == "abrir navegador":
                        openBrowser()
                    elif text == "detente":
                        speak('Adios...')
                        break
                    else:
                        speak('Lo siento, no puedo ayudarte con eso.')
                except:
                    speak('Lo siento, no puedo entenderte')
                intro = 0
                speak('Espere a que el programa se cargue nuevamente.')
        except:
            continue