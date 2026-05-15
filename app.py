import sounddevice as sd 
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import time

#configuracion
sample_rate= 44100
duration = 4

#variable control
score= 0
errors= 0
max_errors= 3

words_by_level = {
    "easy": ["gato", "perro", "manzana", "leche", "sol"],
    "medium": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "hard": ["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}

#dificultad

print('welcome!!')
print('choose a difficulty level: easy, medium, hard')
level= input('-> ').strip().lower()
while level not in words_by_level:
    print('invalid level. please choose: easy, medium, hard')
    level= input('-> ').strip().lower()

word_list= words_by_level[level]
random.shuffle(word_list)
print('you will see a word in spanish, try pronouncing it correctly in english!')

#inicializacion de herramientas
recognizer = sr.Recognizer()
translator = Translator()

for word in word_list:
    print('-----------------------------')
    print(f'word: {word}')
    print('recording... pronounce the word in english')
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write('output.wav', sample_rate, recording)
    print('we have successfully recorded your pronunciation, now we will analyze it...')

    try:
        with sr.AudioFile('output.wav') as source:
            audio = recognizer.record(source)
            recognized = recognizer.recognize_google(audio, language='en').lower()

            time.sleep(2)
            print(f'you said: {recognized}')

            #translation
            translation = translator.translate(word, src='es', dest='en').text.lower()
            print('translation: ', translation)

            if recognized.lower() == translation:
                print('correct!')
                score += 1
            else:
                errors += 1
                print('incorrect!')
            if errors >= max_errors:
                print('you have reached the maximum number of errors. game over!')
                break
    except:
        print('an error occurred while processing the audio.')
        errors += 1
        if errors >= max_errors:
            print('you have reached the maximum number of errors. game over!')
            break

