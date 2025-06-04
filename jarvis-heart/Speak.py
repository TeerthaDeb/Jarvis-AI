__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["Harris Ali Khan"] 
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 


import pyttsx3
import re

# The code is initializing the pyttsx3 text-to-speech engine using the 'sapi5' speech synthesis API. 
# It then retrieves the available voices and sets the voice to be used as the second voice in the list (Zira).
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[1].id) ## [0] : david , [1] : Zira


def speak(audio : str) -> None:
	"""
		The function "speak" takes an audio input and uses a text-to-speech engine to speak the audio.
		
		param audio [string] : The audio parameter represents the text or speech that you want the
		computer to say or speak out loud

		updated: 1.2: does not speak '*'
	"""
	audio = re.sub(r'\*', '', audio)  # Remove '*' characters
	engine.say(audio)
	engine.runAndWait()


# Example usage:
if __name__ == "__main__":
	print("Hello World")
	speak("Hello, world! **This is a sample voice output**.")