# import pyttsx3

# engine = pyttsx3.init()

# # rate = engine.getProperty('rate')   # getting details of current speaking rate
# # print (rate)                        #printing current voice rate
# # engine.setProperty('rate', 300)     # setting up new voice rate

# """VOLUME"""
# # volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# # print (volume)                          #printing current volume level
# # engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1


# # """VOICE"""
# # voices = engine.getProperty('voices')       #getting details of current voice
# # #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# # engine.setProperty('voice', voices[17].id)   #changing index, changes voices. 1 for female
# # for i, voice in enumerate(voices):
# #     print("Voice %d" % i)
# #     print(voice.age, voice.gender, voice.languages, voice.name)
# #     print()

# # engine.setProperty('voice', 'english+f1')
# # engine.setProperty('voice', 'english+f2')
# # engine.setProperty('voice', 'english+f3')
# # engine.setProperty('voice', 'english+f4')
# engine.setProperty('voice', 'english_rp+f3') #my preference
# #engine.setProperty('voice', 'english_rp+f4')




# #engine.say("Good morning. It's 7 A.M. The weather in Malibu is 72 degrees with scattered clouds. The surf conditions are fair with waist to shoulder highlines, high tide will be at 10:52 a.m.")
# #engine.runAndWait()

# """Saving Voice to a file"""
# # On linux make sure that 'espeak' and 'ffmpeg' are installed
# engine.save_to_file('Hello World', 'test.mp3')
# engine.runAndWait()


# # import the module
# import python_weather
# import asyncio

# async def getweather():
#   # declare the client. format defaults to the metric system (celcius, km/h, etc.)
#   async with python_weather.Client(format=python_weather.IMPERIAL) as client:

#     # fetch a weather forecast from a city
#     weather = await client.get("Washington DC")
  
#     for forecast in weather.forecasts:
#       print(forecast.date, forecast.astronomy)
#       print(dir(forecast))
  

# if __name__ == "__main__":
#   asyncio.run(getweather())



from gtts import gTTS
import os    

tts = gTTS(text="Hello emely, my love ", lang='en')#, tld='com.au')
tts.save("pcvoice.mp3")
# to start the file from python
os.system("nvlc pcvoice.mp3")