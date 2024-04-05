__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["Harris Ali Khan"] 
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 

import speech_recognition as sr


def takeCommand() -> str:
	"""
	The `takeCommand` function uses the `speech_recognition` library to convert audio input from the
	user into text.
	return [str]: The function `takeCommand()` returns the user's speech input as a string. If the speech
	input is successfully recognized, it returns the recognized text. If there is an exception or error
	during the speech recognition process, it returns the string "None".
	"""

	# The code block is using the `speech_recognition` library to capture audio input from
	# the user using the microphone.
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)
	
	# The code block you provided is using the `recognize_google` function from the `speech_recognition`
	# library to convert the audio input from the user into text.
	try:
		
		print("Recongnizing...")
		query = r.recognize_google(audio , language = 'en-us')
		print(f"User Said: {query}\n")
		
	# The code block you provided is handling exceptions that may occur during the speech recognition
	# process.
	except sr.UnknownValueError:
		print("Sorry, I didn't understand that.")
		query = "None"

	except sr.RequestError:
		print("I'm having trouble connecting to the internet.")
		query = "None"
	
	except Exception as e:
		print("Exception : " , e)
		print("Say that again please....")
		return "None"

	return query


# Example Usage:
if  __name__ == "__main__":
	command = takeCommand()
	print(f"You said: {command}")