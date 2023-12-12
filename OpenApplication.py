import os
from Speak import speak

def open_application(application_name : str):
	"""_summary_ : The function `open_application` opens a specified application and provides feedback on whether it
	was successful or not.

	Args:
		application_name (String): The parameter `application_name` is a string that represents the name or
	path of the application you want to open. It can be the name of a program installed on your computer
	or the path to the executable file of the application

	**Since : 0.2.1
	"""
	try:
		os.startfile(application_name)
		print(f"{application_name} opened")
		speak(f"{application_name} opened")
	except Exception as e:
		print("Error:", e)
		speak(f"Sorry, I couldn't open {application_name}")