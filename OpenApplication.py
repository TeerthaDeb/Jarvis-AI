__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["Jarvis-AI , itself."] 
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 

import os
from Speak import speak

def open_application(application_name : str) -> bool:
	"""_summary_ : The function `open_application` opens a specified application and provides feedback on whether it
					was successful or not.

	Args:
		application_name (String): The parameter `application_name` is a string that represents the name or
		path of the application you want to open. It can be the name of a program installed on your computer
		or the path to the executable file of the application

	Returns:
		True(boolean) : if the application was successfully opened.
		False(boolean) : If there were any errors while opening the application.

	** Since : 0.2.1
	** Updated on : 1.0.2
	
	"""
	try:
		os.startfile(application_name)
		print(f"{application_name} opened")
		speak(f"{application_name} opened")
		return True
	

	except Exception as e:
		print("Error:", e)
		speak(f"Sorry, I couldn't open {application_name}")
		return False
	

