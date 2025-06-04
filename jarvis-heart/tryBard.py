__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["https://ai.google.dev/api/python/google/generativeai"] 
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 


import google.generativeai as genai
from Speak import speak

def ask_gemini(query : str , api : str) -> None:
	"""_summary_ : Asks Gemini AI a question and generates an answer using Google Generative AI API.

	Args:
		query (str): what  you want to ask the gemini ai.
		api (str): your google pi key.

		Since : 1.2
	"""
	genai.configure(api_key = api)

	model = genai.GenerativeModel('gemini-pro')
	response = model.generate_content(query)
	print("According to gemini: ", response.text)
	speak("According to gemini, " + response.text)

if __name__ ==  '__main__':
	ask_gemini("What is the capital of France?", "<YOUR API KEY>")