import pyttsx3 #for text to speech
# import datetime #for getting time
import speech_recognition as sr  #speech recognizing
import wikipedia #for accessing wikipedia pages and fetching the summary according to the query
import webbrowser #for accessing sites using web browser
import os
import pyaudio
import struct
import math
import requests
import pywhatkit #for whatsapp and youtube automation
import wolframalpha #for fetching weather and facts
import time
from chatGPT_debugger.chatGPT_debugger import debug
import pyjokes #for fetching jokes
import pyautogui #to take ss
import keyboard #to control keyboard
from Bard import Chatbot
import playsound


engine = pyttsx3.init('sapi5') #using sapi5 for voice recognition
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[2].id) #using the male voice 
engine.setProperty('rate', 175) #changed the default speech rate from 200 to 180


def speak(audio):  #function to speak
    engine.say(audio)
    engine.runAndWait()

@debug
def wishme():
    # hr = int(datetime.datetime.now().hour)
    # if hr >= 0 and hr < 12:
    #     speak("good morning boss")
    # elif hr >= 12 and hr < 18:
    #     speak("good afternoon boss")
    # else:
    #     speak('good evening boss')
    speak('hello sir. i am ben. always at your service')

@debug
def takecommand():  #function which let ben listen to me and take command
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        r.pause_threshold = 1
        audio = r.listen(source, 0, 7)

    try:
        print('recognizing...')
        query = r.recognize_google(audio, language='en')
        print('user said ', query)

    except Exception as e:
        
       # speak("i'm not getting it clearly, can you say that again sir!")
        print('say that again please')
        return "None"
    query = str(query).lower()
    print(query)
    return query



def googlebard():
    token = "Wwjv3sPMUnDWRqsT_yjUuOvP9kuyhZLTLnwIw2FWCuujtx2WSA5fWC2OYKG3qWj1oVFyOg."
    while True:
        bot = Chatbot(token)
        tt = takecommand()
        res = bot.ask(tt)
        speak(res['content'])
        if 'write' in tt:
            speak('i saved this in a text file sir.')
            with open('anotherbardcode.txt', 'w') as f:
                f.write(res['content'])
                speak('here is the file.')
                os.startfile('anotherbardcode.txt')

        if 'stop' in tt:
            speak("and i will shut up now")
            break



#to start ben with clap

INITIAL_TAP_THRESHOLD = 0.1
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 2
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
OVERSENSITIVE = 15.0/INPUT_BLOCK_TIME                    
UNDERSENSITIVE = 120.0/INPUT_BLOCK_TIME 
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

def get_rms( block ):
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):

    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None            
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            # print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    # print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream
    
    @debug
    def listen(self):
        
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)

        except IOError as e:
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        
        if amplitude > self.tap_threshold:
            self.quietcount = 0
            self.noisycount += 1
            if self.noisycount > OVERSENSITIVE:

                self.tap_threshold *= 1.1
        else:            

            if 1 <= self.noisycount <= MAX_TAP_BLOCKS:
                return "True-Mic"
            self.noisycount = 0
            self.quietcount += 1
            if self.quietcount > UNDERSENSITIVE:
                self.tap_threshold *= 2

@debug
def Tester():

    tt = TapTester()

    while True:
        kk = tt.listen()
        if "True-Mic" == kk:
            print("")
            print('clap detected: waking up Ben')
            print("")
            break








if __name__ == "__main__":
    Tester()
    playsound.playsound('s.wav')
    wishme()
   
   
   
    while True:
        query = takecommand().lower()
 

        if 'friday' in query:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            speak('hello sir! im friday and im online.')
        
        if 'call ben' in query:
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[2].id)
            speak('hello boss! im back')

        if 'talk' in query:
            speak("okay lets talk, but wait for a few seconds")
            googlebard()



        #logic for executing tasks based on query
        if 'shutdown' in query: #to shutdown pc
            speak("shutting down boss")
            os.system("shutdown /s /t 1")
        if 'restart' in query: #to restart pc
            speak('restarting system')
            os.system("shutdown /r /t 1")



        if 'joke' in query:
            joke = pyjokes.get_joke(language='en', category='all')
            speak(joke)

        if 'jokes' in query:
            jukes = pyjokes.get_jokes(language='en', category='all')
            speak(jukes)

        if  'play' in query:  #to play music on youtube
            q = query.replace("play", "")
            pywhatkit.playonyt(q)
        

        if 'screenshot' in query:
            ss = pyautogui.screenshot(r"E:\ben\ss.png")
            speak("done sir! here is your screenshot")
            os.startfile("E:\ben\ss.png")

        if 'repeat my word' in query:
            speak("speak sir!")
            tt = takecommand()
            speak(f"you said: {tt}")


        if 'weather' in query:
            client= wolframalpha.Client('2E8LHA-3Q57WJGGKT')
            res = str(query)
            qu = client.query(query)
            out = next(qu.results).text
            speak('fetching weather')
            time.sleep(0.5)
            speak(out)
            print(out)
        
        if 'search youtube' in query: #to search anything on youtube
            speak("this is what i have found on youtube")
            query = query.replace("ben", "")
            query = query.replace("search youtube", "")
            yt = "https://www.youtube.com/results?search_query=" + query
            webbrowser.open(yt)

        if 'launch' in query:  #to launch any website
            speak('which website to open')
            query = takecommand().lower()
            speak("opening the site")
            ww = "https://www." + query + ".com"
            webbrowser.open(ww)

        #to google anything
        if 'google' in query:
            import wikipedia as googlescrap
            query = query.replace("ben", "")
            query = query.replace("google search", "")
            query = query.replace("google", "")
            speak("this is what i have found on web")
            pywhatkit.search(query)

            try:
                result = googlescrap.summary(query, sentences=3)
                speak(result)
                print(result)
            
            except:
                speak("sorry boss! but i couldn't find anything more relevant to your search.")

        

        if 'wiki' in query:
            speak('searching wikipedia')
            q = query.replace('wiki','')
            output = wikipedia.summary(q, sentences=2)
            speak('according to wikipedia')
            speak(output)
        
        if 'bye' in query:
            speak('ok boss. See you soon')
            break
            quit()
          
        elif 'whatsapp' in query: #to open whatsapp
            webbrowser.open("https://web.whatsapp.com/")
