import pyttsx3

# The code is initializing the pyttsx3 text-to-speech engine using the 'sapi5' speech synthesis API. 
# It then retrieves the available voices and sets the voice to be used as the second voice in the list (Zira).
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[1].id) ## [0] : david , [1] : Zira

def speak(audio : str):
	"""
	The function "speak" takes an audio input and uses a text-to-speech engine to speak the audio.
	
	@param audio [string] : The audio parameter represents the text or speech that you want the
	computer to say or speak out loud
	"""
	engine.say(audio)
	engine.runAndWait()