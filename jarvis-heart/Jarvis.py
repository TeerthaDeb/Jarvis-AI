__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["Harris Ali Khan"]
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 


'''
	Changes on Beta 0.2.1 
		* User can Type and Speak to command Jarvis
		* Opens some application using "Open Application function"
		* Very good at searching youtube Videos

	Changes on Beta 0.4.9
		* Able to Play Music
		* Issue on sending emails
		* GPT integration (Trial Mode)

	Changes on Beta 0.4.91
		* Better Weather using web scrapping.
		* Some features are still in development.
		* ChatGPT is Uniavailable in this version as it requires premium subscription.
		* Google Bard is being introduced.

	Changes on Beta 0.4.92
		* Modules are on different files so easy to debug.
		* Playing song from youtube is perfect now.
		* It can now tell a joke.
		* Next version will be dedicated on Google Bard or User Based design.

	Changes on 1.00:
		* Personalized Assistant.
		* GPT 3.5 : powered.
		* Improved Search Engine.
		* More Features.

	Changes on 1.0.1:
		* improved Joke,
		* improved User Class,

	Changes on 1.0.2:
		* Clean Code so it's easier to maintain and debug.
		* Better Weather Visual.
		* Able to tell location.
		* Able to open / close applicaitons.

	Changes on 1.0.21:
		* Nice format for weather visuals.
		* dependencies provided.

	Changes on 1.2:
		* Google Bard introduced.
        	- Can answer any question based on the user input.
		* Chat Gpt would be used at first, then Google Bard if not available.
'''

# These are prebuilt modules
import datetime 
from datetime import datetime
import wikipedia
import os
import webbrowser
import smtplib
from bs4 import BeautifulSoup
import requests
import urllib.parse
from googlesearch import search


# These are designed modules:
from tryGPT import ask_gpt
from Speak import speak
from TakeCommand import takeCommand
from OpenApplication import open_application
from GoogleSearch import googleSearch
from tryYoutube import playMusicFromYouTube
from WeatherVisual import Gen_report
from getLocation import get_city_details
import User
import Joke
from OpenApplicaiton2 import open_app
from OpenApplicaiton2 import close_app
from tryBard import ask_gemini

# Jarvis Starts here:
boss = None

os.system('cls' if 'nt' in os.name else 'clear') # Clearing the terminal screen

def User_Set_UP() -> None:
	"""
		This function creates the user object with all necessary information for interaction, such as name, email address
		This function creates the user object for personalization of responses, takes user's name and
		asks if they want to continue with previous data (if any) or create new one.
		---------------
		Args:
			None
		---------------
		Returns:
			None
		---------------
		Since : 1.00
		updated : 1.0.1 , 1.0.2
	"""
	global boss
	boss = User.return_user()

	if boss == None:
		print("Welcome to Jarvis AI Assistant! I will be your personal assistant. Before you continue, let's setup your personal assistant at first. \nIt is a one time setup and next time you will just click and run it.")
		speak("Welcome to Jarvis AI Assistant! I will be your personal assistant. Before you continue, let's setup your personal assistant at first. It is a one time setup and next time you will just click and run it.")
		speak("So let's get started.")
		boss = User.User()
		os.system('cls' if 'nt' in os.name else 'clear')
	
	User.save_user_to_file(boss)


def wish_User() -> None:
	"""
		---------------
		Args:
			None
		---------------
		Returns:
			None
		---------------
		updated : 1.0.1 , 1.0.2
	"""
	hour = int(datetime.now().hour)

	call_them = boss.pronunciation
	
	if boss.is_birthday_today():
		age = datetime.datetime.now().year - boss.birth_date.year
		print(f"{call_them},  Happy Birthday! You are {age} years old today.")
		speak(f"Happy {age} th Birthday")

	if hour >= 0 and hour <12:
		speak(f'Good Morning ! {call_them}')
	
	elif hour>=12 and hour<18:
		speak(f'Good AfterNoon ! {call_them}')
	
	else:
		speak(f'Good Evening ! {call_them}')

	speak("I am your personal assistant, Jarvis. Please tell me how may I help you?")



#-------------------------Main Function Calling--------------------------
if __name__ == "__main__":
	"""
		This is the main function of this module. It will be called when you run Jarvis.

		---------------
		Args:
			None
		---------------
		Returns:
			None
		---------------

		updated : 1.0.1 , 1.0.2
	"""
	User_Set_UP() # Set up user if not set yet.

	wish_User() # Wish user.

	user_wants_to_type = True ### Check this , By default, it should be false.

	print("If you want to command me by typing , speak : I want to type")
	# speak("Just to let you know that, you can command me by typing. If you want to command by typing, speak so")

	try :
		while True: # The main loop starts...

			if user_wants_to_type :
				'''
					This section of code checks if user wants to type or not.
					If they do, they will be asked to enter their command via keyboard,
					otherwise, they will speak.
				'''
				speak("Enter your command: ")
				query = input("\nEnter your command : ")
				query = query.lower()
			

			else :
				'''
					When User wants to speak...
				'''
				print("Listening...")
				query = takeCommand().lower()

			# Done checking how user wants to command me.
				
			if "wikipedia" in query:
				'''
					The code block is checking if the word "wikipedia" is present in the user's query. If
					it is, the code removes the word "wikipedia" from the query and uses the `wikipedia` library to
					search for a summary of the remaining query on Wikipedia. It retrieves the summary of the query
					and stores it in the `results` variable. The `sentences` parameter specifies the number of
					sentences to include in the summary, in this case, it is set to 2. The code then prints the
					results and speaks it using the `speak` function.
					
					Updated on : 1.0.2
				'''
				speak("Searching Wikipedia...")
				query = query.replace("wikipedia" , "")
				results = wikipedia.summary(query , sentences = 2)
				print(f"According to Wikipedia, {results}")
				speak(f"According to Wikipedia, {results}")




			elif "play" in query and "from youtube" in query:
				'''
					The code is checking if the query contains the words "play" and "from youtube". If it does,
					it extracts the music query by removing the words "play" and "from youtube" from the query and
					then calls the function `playMusicFromYouTube` with the extracted music query as an argument.
					
					Updated on : 1.0.2
				'''
				music_query = query.replace("play", "").replace("from youtube", "").strip()
				playMusicFromYouTube(music_query)
				print("Played" , music_query , "on YouTube.")
				speak("Played")
			



			elif "open youtube" in query:
				'''
					this  part of the condition checks whether the user wants to open YouTube or not. If yes, then
					the function `openYoutube()` is called which opens the default browser page for YouTube.

					updated on : 1.0.2
				'''
				try:
					webbrowser.open("https://www.youtube.com")

					print("Youtube opened via your default browser")
					
					speak("Do you want me to play anymusic?")
					query = takeCommand.lower()
					
					if "y" in query:
						
						speak("ask me the song to play: ")
						
						query = takeCommand().lower()
						music_query = query.replace("play", "").replace("from youtube", "").strip()
						
						playMusicFromYouTube(music_query)
					
					elif "play" in query and "from youtube" in query:
						music_query = query.replace("play", "").replace("from youtube", "").strip()
						playMusicFromYouTube(music_query)
					
					else:
						speak("Aborting playing music and Waiting on the next command...")
						print("Aborting playing music.")

				except Exception as e:
						print("An error occurred:", e)
						speak("An error occured while opening youtube from your browser.")




			elif "open google" in query:
				'''
					This Block of Code, opens google.
				'''
				webbrowser.open("https://www.google.com")
				print("Google opened via your default browser")
				speak("Opened Google homepage")




			elif "open facebook" in query:
				'''
					This block of code is used to open Facebook page using web-browser.
				'''
				webbrowser.open("https://www.facebook.com")
				print("Facebook opened via your default browser")
				speak("Opened Facebook Home Page")




			elif "open gmail" in query:
				'''
					This block of code is used to open GMAIL page using web-
				'''
				webbrowser.open("https://www.gmail.com")
				print("Gmail opened via your default browser")
				speak("Opened gmail")

			

			elif "open linkedin" in query:
				'''
					This block of code is used to open LinkedIn page using web-broser.
				'''
				webbrowser.open("https://www.linkedin.com")
				print("LinkedIN opened via your default browser")
				speak("Opened Linkedin")




			elif "open chat gpt" in query or "open gpt" in query:
				'''
					This block of code will open a conversation with
				'''
				webbrowser.open("https://www.chat.openai.com")
				print("ChatGPT opened via your default browser")
				speak("Opened Chat GPT")




			elif "play" in query and ("music" in query or "song" in query):
				'''
					Functionality:
						- Checks if user has already a music directory
						- if not , asks uers to enter it
						- if the directory is valid, saves it, otherwise asks to make this directory
						- either cases it saves update to user file.
						- Finally tries to play music from the directory.

						Updated on:	1.00 , 1.0.1
									1.2 : logics updated.
				'''

				if boss.check_music_directory() :
					music_dir = boss.get_music_directory()
					
				else:
					music_dir = input("Please enter your music directory full-path: ")

				if not os.path.exists(music_dir):
					speak("That is an invalid Path. Do you want me to make this path?")
					choice = input("That is an invalid Path. Do you want me to make this path? (Yes / No) : ")

					if choice.lower().startswith("y"):
						os.makedirs(music_dir)
						print("Directory created. Now you can paste your songs in that directory.")
						speak("Directory created. Now you can paste your songs in that directory.")
						boss.set_music_directory(music_dir)
						User.save_user_to_file(boss)
					else:
						print("Operation aborted to play music.")
						speak("Operation aborted to play music.")
						continue
				else:
					boss.set_music_directory(music_dir)
					User.save_user_to_file(boss)

				try:
					songs = os.listdir(music_dir)
					if len(songs) == 0:
						speak("No songs found in the music directory.")
						print("No songs found in the music directory.")
					else:
						speak("Playing songs.")
						print("Playing Songs:", songs)
						os.startfile(os.path.join(music_dir, songs[0]))
				except Exception as e:
					print("Error:", e)
					speak(f"Sorry {boss.pronunciation}, I couldn't play music.")


			
			elif "what" in query and "time" in query and ("it" in query or "now" in query):
				'''
					This block tells the current time.

					Updated on : 1.2: better logic

				'''
				strTIme = datetime.now().strftime("%H:%M:%S")
				print("The time is : ", strTIme)
				speak("It is {} right now".format(strTIme))

				
			


			elif "google" in query:
				'''
					This block helps user to search something on google.

					Updated on : 1.0.2
				'''
				search_query = query.replace("google" , "").strip()

				if "for" in query:
					search_query = search_query.replace("for" , "").strip()
				
				googleSearch(search_query)
				speak("Search result is on your screen.")





			elif "weather" in query  or "temparature" in query:
				'''
					This block gives weather information of a particular city.

					Updated on : 1.0.2
				'''

				if "in" in query:
					city = query.split("in")[1].strip()
				
				else:
					city = get_city_details()['city']


				try:
					Gen_report(city)
					speak("Weather visuals on your screen")
					
				except Exception as e:
					print("An error occurred while processing your request.")
					print("Error: " , e)
					speak("There was an error processing your request.")



			

			elif "what is" in query or "search" in query:
				'''
					This block searches something on google

					Updated on : 
					Mofied on : 1.0.2
								1.2 : Added not found on wikipedia logic
				'''

				search_query = query.replace("what is", "").strip()
				# First, try searching on Wikipedia
				try:
					wikipedia_results = wikipedia.summary(search_query , sentences = 3)
					try:
						print(wikipedia_results)
						speak("According to Wikipedia,")
						speak(wikipedia_results)
					except Exception as e:
						print("Error while searching in wikipedia. Error : " , e)
					# If not found on Wikipedia, search on Google
				except Exception as e:
					speak("As I don't know and did not find this on wikipedia, I am")
					googleSearch(search_query)
			



			elif "who is" in query:
				'''
					This block of code handles the 'Who is' queries by calling the function getPersonFromName from people.py file which
					
					Since : 0.4.92
					Modified On : 1.0.2

				'''
				person_to_search = query.replace("who is", "").strip()

				# Attempt to find information on Wikipedia
				try:
					wikipedia_results = wikipedia.summary(person_to_search, sentences=3)
					print(wikipedia_results)
					speak(f"According to Wikipedia, {wikipedia_results}")
				
				# If not found on Wikipedia, search on Google
				except wikipedia.exceptions.DisambiguationError as e:
					print(f"DisambiguationError: {e}")
					speak(f"Searching for {person_to_search} on Google.")
					
					# You can implement your Google search logic here
					googleSearch(person_to_search)
				
				except Exception as e:
					print(f"Error while searching for {person_to_search} on Wikipedia: {e}")
					speak(f"Sorry, I couldn't find information about {person_to_search} on Wikipedia.")
					speak(f"Please ensure that {person_to_search} is on Wikipedia for accurate results.")



			elif "joke" in query:
				'''
					This block tells joke.

					Since : 0.4.92
					Modified On : 1.0.2
				'''
				# Extracting the topic from the query
				split_query = query.split("joke", 1)  # Split the query at the word "joke"
				
				if len(split_query) > 1 and split_query[1].strip():  # Check if there's content after "joke"
					topic = split_query[1].strip().split()  # Extract the topic after "joke"
					if len(topic) > 1:
						print("Topic:", topic[1])
						Joke.tell_joke(boss , topic[1])
					else:
						Joke.tell_joke(boss , topic[0])  # If there's only one word after "joke", treat it as the topic
				else:
					Joke.tell_joke(boss)  # No specific topic mentioned, tell a random joke



			elif("thank you" in query):
				'''
					This block Responses on Thank you.
				'''
				speak("You are welcome. I am designed to help you by all means, any time.")
			
			
			elif("how do you work" in query):
				'''
					This  block gives an overview of how my AI works. ; - )
				'''
				speak("let that be a secret , but you can explore me")
				print(":)")
			



			elif "where am i" in query:
				'''
				If the user asks where they are, this part will tell them their locaiton.
				'''
				location = get_city_details()
				print(format(location))

				speak(f"You're currently located at {location['region']}. That is in {location['country']}.")



			
			elif "where" in query:
				'''
					This block responses the query "where is"
				'''
				search_query = query.replace("where", "").strip()
				encoded_query = urllib.parse.quote(search_query)
				search_url = f"https://www.google.com/search?q=where+{encoded_query}"

				try:
					webbrowser.open(search_url)
					speak("Here is the result:")
					try:
						response = requests.get(search_url)
						soup = BeautifulSoup(response.text, "html.parser")
						# Find and extract the main search result description
						search_result = soup.find(class_="BBwThe")
						print(search_result.get_text())
						if search_result:
							speak(search_result.get_text())
						else:
							speak("I'm sorry, I couldn't find the information you requested.")
						
					except Exception as e:
						print("Error:", e)
						speak("Sorry, I could not find what you were looking for. Please try again later.")
						
				except Exception as e:
					print("Error:", e)
					speak("Sorry, I couldn't open the website.")

			
			
			
			elif "who made you" in query:
				'''
					The code is checking if the string "who made you" is present in the variable "query". If it
					is, it will print a message and a link to the LinkedIn profile of Mr. Maharaj Teertha Deb.
				'''
				speak("Mr. Maharaj Teertha Deb made me. visit his linkedIN profile typed below")
				print("https://www.linkedin.com/in/maharaj-teertha-deb/")

			


			elif ("quite" in query or "exit" in query):
				speak("Thank you for using me. Talk to you later. Bye")
				print("Thank you.")
				break

			


			elif ("i" in query and "type" in query):
				'''
					This part of the code checks if the user wants to type. 
				'''
				user_wants_to_type = True
				speak("You will be typing to command me now. If you want to speak instead, write I want to speak")



			
			elif ("i" in query and "speak" in query):
				'''
					This part of the code checks if the user wants to speak.
				'''
				user_wants_to_type = False
				speak("You can command me by saying anything. And you know how to type to command me")



			elif "open" in query:
				'''
					This part of the code opens whatever app the user asks to open.

					Since : 1.0.2
				'''
				query = query.split("open")
				open_app(query[1])



			elif "close" in query:
				'''
					This part of the code closes whatever app the user asks to close.

					Since : 1.0.2
				'''
				query = query.split("close")
				close_app(query[1])


			
			elif "ask" in query and ("bard" in query or "bird" in query or "gemini" in query):
				'''
					since : 1.2
					functionality:
						- asks google bard
				'''
				try:
					ask_gemini(query , boss.bard_api)
				
				except Exception as e:
					print(f"\n\nError Occured while asking Gemini as well.\n{str(e)}\n\n")
					speak("Also encountered error while asking bard. Please try again later.")



			else:
				'''
					since : 1.00
					functionality:
						- checks user's gpt api
						- if they have it,  generates response based on user's input from gpt.
					
					modified On : 	1.0.2,
									1.2 : Added Google Bard.
				'''
				if boss.gpt_api != None:
					try:
						ask_gpt(query , boss.gpt_api , boss.name , int(datetime.now().year - boss.birth_date.year))
					
					except Exception as e:

						if ("insufficient_quota" in str(e)):
							print("Your Api key is expired now. You need to get a new api key. I am opening the webbrowser you can get a new api key.")
							speak("Your Api key is expired now. You need to get a new api key. I am opening the webbrowser you can get a new api key")
							boss.set_gpt_api(None)
							User.save_user_to_file(boss)
							
							speak("Asking Bard now.")
							try:
								ask_gemini(query , boss.bard_api)
							
							except Exception as e:
								print(f"\n\nError Occured while asking Gemini.\n{str(e)}\n\n")
								speak("Also encountered error while asking bard. Please try again later.")

						elif ("invalid_api_key" in str(e)):
							print("Gpt says that is an invalid api key.")
							speak("Opps!  It seems like your GPT API Key is not valid.")
							boss.set_gpt_api(None)
							User.save_user_to_file(boss)

							speak("Asking Bard now.")
							try:
								ask_gemini(query , boss.bard_api)
							
							except Exception as e:
								print(f"\n\nError Occured while asking Gemini.\n{str(e)}\n\n")
								speak("Also encountered error while asking bard. Please try again later.")

						else:
							print("I tried GPT, but failed to response due to :" , e)
							speak("I tried GPT, but failed to response")

							speak("Asking Bard now.")
							try:
								ask_gemini(query , boss.bard_api)
							
							except Exception as e:
								print(f"\n\nError Occured while asking Gemini as well.\n{str(e)}\n\n")
								speak("Also encountered error while asking bard. Please try again later.")




	except Exception as e:
		print("Uff, my system broke down due to:", e)
		speak("Uff, I broke doewn. Run me again.")