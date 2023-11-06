#jervis 		: Beta 
#created by 	: Maharaj Teertha Deb
#linked IN 		: https://www.linkedin.com/in/maharaj-teertha-deb/
#released on 	: September-21-2023

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
'''


# The code script that imports various libraries and modules to perform different tasks.
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import smtplib
from bs4 import BeautifulSoup
import requests
import urllib.parse
from googlesearch import search
import weather
# import openai
import time



# The code is initializing the pyttsx3 text-to-speech engine using the 'sapi5' speech synthesis API. 
# It then retrieves the available voices and sets the voice to be used as the second voice in the list (Zira).
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices' , voices[1].id) ## [0] : david , [1] : Zira



def speak(audio):
	"""
	The function "speak" takes an audio input and uses a text-to-speech engine to speak the audio.
	
	@param audio [string] : The audio parameter represents the text or speech that you want the
	computer to say or speak out loud
	"""
	engine.say(audio)
	engine.runAndWait()



def wishMe():
	"""
	The function `wishMe()` greets the user based on the current time and introduces itself as a
	personal assistant.
	"""
	hour = int(datetime.datetime.now().hour)
	if hour>=0 and hour<12:
		speak("Good Morning Sir !")
	elif hour>=12 and hour<18:
		speak("Good Afternoon Sir !")
	else:
		speak("Good Evening Sir !")

	speak("I am your personal assistant. Please tell me how may I help you?")




def takeCommand():
	"""
	The `takeCommand` function uses the `speech_recognition` library to convert audio input from the
	user into text.
	return: The function `takeCommand()` returns the user's speech input as a string. If the speech
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




def sendEmail(to , content):
	"""
	!!! THIS FUNCTION IS NOT DONE YET.....
	The function `sendEmail` sends an email to the specified recipient with the given content.
	
	:param to: The "to" parameter is the email address of the recipient to whom you want to send the
	email. It should be a string containing the email address
	:param content: The content parameter is the body of the email that you want to send. It can be a
	string containing the message you want to send to the recipient
	"""
	server = smtplib.SMTP("smtb.gmail.com" , 587)
	server.ehlo()
	server.starttls()
	server.login('yourEmail@gmail.com' , '*****')
	server.sendmail("d_mahar@concordia.ca" , to , content)
	server.close()



def googleSearch(contentToSearch):
	"""_summary_ : This function takes a content to search as input, opens a Google search page with the
	given content, and retrieves the top 3 search results and speaks them out.

	Args:
		contentToSearch (string): the content to be searched 
	"""
	try:
		for i in search(query, tld="co.in", num=1, stop=1, pause=2):
			webDomain = i.replace("https://www." , " ")
			finalWebDomain = ""
			for j in webDomain:
				if (j != '/'):
					finalWebDomain += j
				else:
					break
			speak("According to : " + finalWebDomain)
			print("web address: " + i)
			webbrowser.open(i)
	except Exception as e:
			print("Error : " , e)




def playMusicFromYouTube(search_query):
	""" The above code performing a search query on YouTube using the `search` function. It appends 
		site:youtube.com" to the search query to ensure that the search results are limited to YouTube.

	Args:
		search_query (String): The video to be played.

		** Since 0.2
		** Updated on 0.2.1
	"""
	try:
		search_query = search_query + " site:youtube.com"
		search_results = list(search(search_query, num=1, stop=1, pause=2))
		# The code is checking if there are any search results available. If there are search results,
		# it assigns the first result to the variable `video_url`. It then opens the `video_url` in a web
		# browser. It replaces the string "site:youtube.com" in the `search_query` with an empty string.
		# Finally, it prints a message indicating that the search query is being played from YouTube and
		# speaks the same message.
		if search_results:
			video_url = search_results[0]
			webbrowser.open(video_url)
			search_query = search_query.replace("site:youtube.com" , "")
			print(f"Played {search_query} from YouTube")
			speak(f"Playing {search_query} from YouTube")
		# The code is a snippet of Python code that is handling a condition where there are no search
		# results found on YouTube. It prints a message to the console saying "No search results found on
		# YouTube." and also uses a function called "speak" to speak the message "Sorry, I couldn't find any
		# relevant results on YouTube."
		else:
			print("No search results found on YouTube.")
			speak("Sorry, I couldn't find any relevant results on YouTube.")
	except Exception as e:
		print("Error:", e)
		speak("Sorry, I couldn't play the music from YouTube.")




def open_application(application_name):
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




def send_email_with_selenium(recipient_email, subject, content):
	### !!!!!!!!!!!!!!!! Not Ready Yet........................
	"""This function sends email using your default web browser

	Args:
		recipient_email [string]: xxxx@xxxx.com
		subject (string): The subject of the email
		content (string): Content to send
	"""
	try:
        # Open Gmail in the default web browser
		webbrowser.open("https://www.gmail.com")
        # Initialize the Chrome web driver
		
        # Wait for the Gmail page to load
		time.sleep(5)

        # Compose a new email
		compose_button = driver.find_element_by_xpath("//div[text()='Compose']")
		compose_button.click()
		time.sleep(2)  # Wait for the compose window to load

        # Enter recipient's email address and subject
		to_field = driver.find_element_by_name("to")
		to_field.send_keys(recipient_email)
		subject_field = driver.find_element_by_name("subjectbox")
		subject_field.send_keys(subject)

        # Enter email content
		email_body = driver.find_element_by_xpath("//div[@aria-label='Message Body']")
		email_body.send_keys(content)

        # Send the email or save as draft
		send_button = driver.find_element_by_xpath("//div[text()='Send']")
		send_it = input("Send the email? (yes/no): ").lower()
		if "yes" in send_it:
			send_button.click()
			print("Email sent.")
		else:
            # Save the email as a draft
			driver.find_element_by_xpath("//div[text()='Close']").click()
			print("Email saved as a draft.")
	
	except Exception as e:
		print("Error:", e)
		
	finally:
        # Close the browser window
		driver.quit()




# def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
# 	"""
# 	The function `chat_with_chatgpt` is a Python function that uses the OpenAI GPT-3.5-turbo model to
# 	generate a response to a given prompt.
	
# 	:param prompt: The prompt is the starting point or the initial message that you provide to the
# 	chatbot. It can be a question, a statement, or any text that you want to use as the basis for the
# 	conversation
# 	:param model: The "model" parameter specifies which language model to use for generating the
# 	response. In this case, the model is set to "gpt-3.5-turbo", which is one of the models provided by
# 	OpenAI. This model is known for its fast response times and is suitable for, defaults to
# 	gpt-3.5-turbo (optional)
# 	:return: The function `chat_with_chatgpt` returns the response generated by OpenAI's GPT-3.5-turbo
# 	model based on the given prompt.
# 	"""
# 	response = openai.Completion.create(
#         engine=model,
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.5,
#     )
# 	message = response.choices[0].text.strip()
# 	return message

def chat_with_google_bard():
	query = "What is the meaning of life?"
	response = google_bard.generate_text(query, api_key=API_KEY)
	print("Google Bard Response (Using google_bard Module):")
	speak(response)


################# Main Function Follows ::::::::::::::::::::::::::::::;;;;


if __name__ == "__main__":
	
	user_wants_to_type = False
	wishMe()
	speak("Remember , you can command me by typing. If you want to command by typing, speak so")
	print("If you want to command me by typing , speak : I want to type")
	while (True):
		if(user_wants_to_type) : 
			speak("Enter your command: ")
			query = input("\nEnter your command : ")
			query = query.lower()
		else : 
			query = takeCommand().lower()
		# The code block is checking if the word "wikipedia" is present in the user's query. If
		# it is, the code removes the word "wikipedia" from the query and uses the `wikipedia` library to
		# search for a summary of the remaining query on Wikipedia. It retrieves the summary of the query
		# and stores it in the `results` variable. The `sentences` parameter specifies the number of
		# sentences to include in the summary, in this case, it is set to 2. The code then prints the
		# results and speaks it using the `speak` function.
		if ("wikipedia" in query):
			speak("Searching Wikipedia...")
			query = query.replace("wikipedia" , "")
			# The line `results = wikipedia.summary(query , sentences = 2)` is using the `wikipedia` library to
			# search for a summary of the query on Wikipedia. It retrieves the summary of the query and stores
			# it in the `results` variable. The `sentences` parameter specifies the number of sentences to
			# include in the summary. In this case, it is set to 2, so the summary will contain 2 sentences.
			# then it prints the result and speaks it.
			results = wikipedia.summary(query , sentences = 2)
			print(results)
			speak(f"According to Wikipedia,{results}")
		
		# The code is checking if the query contains the words "play" and "from youtube". If it does,
		# it extracts the music query by removing the words "play" and "from youtube" from the query and
		# then calls the function `playMusicFromYouTube` with the extracted music query as an argument.
		if "play" in query and "from youtube" in query:
			music_query = query.replace("play", "").replace("from youtube", "").strip()
			playMusicFromYouTube(music_query)
			

		# The code block elif ("open youtube" in query): is checking if the
		# user's query contains the phrase "open youtube". If it does, it opens the YouTube website in the
		# default web browser using the `webbrowser.open()` function. This allows the user to easily access
		# the YouTube website by simply saying "open youtube" to the personal assistant.
		elif ("open youtube" in query):
			try:
				webbrowser.open("https://www.youtube.com")
				print("Youtube opened via your default browser")
				speak("Do you want me to play anymusic?")
				query = takeCommand.lower()
				if "yes" in query:
					speak("ask me the song to play: ")
					query = takeCommand().lower()
					music_query = query.replace("play", "").replace("from youtube", "").strip()
					playMusicFromYouTube(music_query)
				elif "play" in query and "from youtube" in query:
					music_query = query.replace("play", "").replace("from youtube", "").strip()
					playMusicFromYouTube(music_query)
				else:
					speak("Aborting playing music and Waiting on the next command...")
					print("User does not want me to play anything from youtube")

			except Exception as e:
					print("An error occurred:", e)

		# The code block elif ("open google" in query):is checking if the user's query contains the phrase "open
		# google". If it does, it opens the Google website in the default web browser using the
		# `webbrowser.open()` function. This allows the user to easily access the Google website by simply
		# saying "open google" to the personal assistant.
		elif ("open google" in query):
			webbrowser.open("https://www.google.com")
			print("Google opened via your default browser")

		# The code block elif ("open facebook" in query): checking if the user's query contains the phrase "open
		# facebook". If it does, it opens the Facebook website in the default web browser using the
		# `webbrowser.open()` function. This allows the user to easily access the Facebook website by simply
		# saying "open facebook" to the personal assistant.
		elif ("open facebook" in query):
			webbrowser.open("https://www.facebook.com")
			print("Facebook opened via your default browser")

		# The code block elif ("open gmail" in query): is checking if the user's query contains the phrase "open gmail".
		# If it does, it opens the Gmail website in the default web browser using the `webbrowser.open()`
		# function. This allows the user to easily access the Gmail website by simply saying "open gmail" to
		# the personal assistant.
		elif ("open gmail" in query):
			webbrowser.open("https://www.gmail.com")
			print("Gmail opened via your default browser")
		
		# The code block elif ("open linkedin" in query): is checking if
		# the user's query contains the phrase "open linkedin". If it does, it opens the LinkedIn website in
		# the default web browser using the `webbrowser.open()` function. This allows the user to easily
		# access the LinkedIn website by simply saying "open linkedin" to the personal assistant.
		elif ("open linkedin" in query):
			webbrowser.open("https://www.linkedin.com")
			print("LinkedIN opened via your default browser")
		
		# The code block elif ("open chatgpt" in query): is checking if
		# the user's query contains the phrase "open chatgpt". If it does, it opens the ChatGPT website
		# (chat.openai.com) in the default web browser using the `webbrowser.open()` function. This allows
		# the user to easily access the ChatGPT website by simply saying "open chatgpt" to the personal
		# assistant.
		elif ("open chat gpt" in query or "open gpt" in query):
			webbrowser.open("https://www.chat.openai.com")
			print("ChatGPT opened via your default browser")

		# This code handles the functionality of playing music. It allows the user to specify a music directory and plays songs from that directory.
		# Updated on : <0.2.2>
		# Functionality:
		# - Checks if the specified music directory exists and creates it if it doesn't.
		# - Checks if a music directory path is already assigned in a file and reads it.
		# - If the music directory path is not assigned, prompts the user to enter it and saves it in the file.
		# - Lists the songs in the music directory and plays the first song.
		# - Provides appropriate messages for scenarios where no songs are found or if there are errors in the process.
		elif "play" in query and ("music" in query or "song" in query):
			try:
				music_dir = "C:\\Users\\Public\\Documents\\TDsoftwares\\JarvisAI\\MusicDirectory"
				# Check if the music directory exists, and create it if it doesn't
				if not os.path.exists(music_dir):
					os.makedirs(music_dir)
				#Check if a music directory path is already assigned
				music_dir_file_path = os.path.join(music_dir, "music_directory.txt")
				if os.path.exists(music_dir_file_path):
					with open(music_dir_file_path, "r") as file_in_directory:
						music_dir = file_in_directory.read().strip()
				else:
					speak("Music Directory is not assigned yet. Please copy and paste the music path to continue listening: ")
					music_dir = input("Music Directory is not assigned yet. Please copy and paste the music path to continue listening: ")
					with open(music_dir_file_path, "w") as file_in_directory:
						file_in_directory.write(music_dir)
				
				songs = os.listdir(music_dir)
				if len(songs) == 0:
					speak("No songs found in the music directory.")
					print("No songs found in the music directory.")
				else:
					speak("Playing songs.")
					print("Playing Songs: ", songs)
					os.startfile(os.path.join(music_dir, songs[0]))
			except Exception as e:
				print("Error:", e)
				speak("Sorry, I couldn't play the music.")

		
		# The code block `elif ("the time" in query)` is checking if the user's query contains the phrase
		# "the time". If it does, it retrieves the current time using the
		# `datetime.datetime.now().strftime("%H:%M:%S")` function and stores it in the `strTime` variable.
		# It then prints the current time and speaks it using the `speak` function. This allows the personal
		# assistant to provide the user with the current time when asked.
		elif ("the time" in query) :
			strTime = datetime.datetime.now().strftime("%H:%M:%S")
			print("The current time is: " , strTime)
			speak(f"The time is, {strTime}")

	
		# The code is checking if the query contains the phrase "open code" or "open visual studio
		# code". If either of these phrases is present, it will call the function "open_application" and
		# pass the argument "Visual Studio Code.exe".
		elif (("open code" in query) or ("open visual studio code" in query)):
			open_application("Visual Studio Code.exe")
			
		# The code is checking if the string "open notepad in query" is present. If it is, it will
		# open the Notepad application.
		elif "open notepad" in query:
			open_application("notepad.exe")

		elif "open chrome" in query:
			open_application("chrome.exe")

		# The code block `elif ("email to me" in query)` is checking if the user's query contains the phrase
		# "email to me". If it does, it prompts the user to provide the content of the email by saying "What
		# should I write?". It then uses the `takeCommand()` function to convert the user's speech input
		# into text and stores it in the `content` variable. After that, it speaks the message "The email
		# has been sent". If there is an error during the process of sending the email, it prints the error
		# message and speaks "Sorry, I was not able to send the email due to [error message]".
		elif ("email" in query):
			try:
				speak("What should i write ?")
				content = input("Write content here: ")
				speak("The content that were written: ")
				print(content)
				speak(content)
				ask_Confirmation = input("Should I send it? (yes/no): ")
				speak("Should I send it?")
				if("e" in ask_Confirmation and "s" in ask_Confirmation):
					speak("Enter the email address to be sent: ")
					receiverEmailAddress = input("enter receivers email: ")
					speak("What is the subject is the email: ")
					subject = takeCommand()
					speak("Trying to send the email")
					send_email_with_selenium(receiverEmailAddress , subject , content)
				else:
					speak("You aborted the operation")
					print("You aborted the operation")
			except Exception as e:
				print("Error :" , e)
				speak("Sorry , I was not able to send the email. due to ")
		
		elif ("google" in query):
			search_query = query.replace("google" , "").strip()
			googleSearch(search_query)
				
		# The code snippet that handles a query related to weather. It first checks
		# if the word "weather" is present in the query. If it is, it extracts the search query by removing
		# the phrase "what is" and any leading or trailing spaces.
		elif "weather" in query or ("temperature" in query and "now" in query):
			
			try:
				temp = weather.find_weather_element()
				print( temp + " degree Celcious")
				speak("The Temerature is :" + temp + " degree celcious")
			except Exception as e:
				print("Error:", e)
	

		elif "what is" in query or "search" in query:
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
				googleSearch(search_query)


		# The code checks if the string "thank you" is
		# present in the variable "query". If it is, then it calls the function "speak" with the message
		# "You are welcome. I am designed to help you by all means any time."
		elif("thank you" in query):
			speak("You are welcome. I am designed to help you by all means any time.")
		
		# The above code is checking if the string "how do you work?" is present in the variable "query". If
		# it is, then it will execute the code inside the if statement, which includes speaking a response.
		elif("how do you work?" in query):
			speak("let that be a secret , but you can explore me")
			print(":)")
		
		# The code snippet that handles a query containing the word "where". It
		# performs search query on google and speaks the result.
		elif "where" in query:
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
		
		# The code is checking if the string "who made you" is present in the variable "query". If it
		# is, it will print a message and a link to the LinkedIn profile of Mr. Maharaj Teertha Deb.
		elif "who made you" in query:
			speak("Mr. Maharaj Teertha Deb made me. visit his linkedIN profile typed below")
			print("https://www.linkedin.com/in/maharaj-teertha-deb/")

		# The cod is checking if the words "quite" or "exit" are present in the variable "query". If
		# either of these words is present, it will execute the code inside the if statement. In this case,
		# it will call the "speak" function to say "Thank you for using me. Talk to you later. Bye" and then
		# exit the program with a status code of 0.
		elif ("quite" in query or "exit" in query):
			speak("Thank you for using me. Talk to you later. Bye")
			print("Thank you.")
			break

		# The code is checking if the string "i" and "type" are present in the variable "query". If
		# both conditions are true, it sets the variable "user_wants_to_type" to True and speaks a message
		# informing the user that they will be typing to command the program.
		elif ("i" in query and "type" in query):
			user_wants_to_type = True
			speak("You will be typing to command me now. If you want to speak instead, write I want to speak")

		# The code is checking if the string "i" is present in the variable "query" and if the string
		# "speak" is present in the variable "query". If both conditions are true, it sets the variable
		# "user_wants_to_type" to False and calls the function "speak" with the argument "You can command me
		# by saying anything. And you know how to type to command me".
		elif ("i" in query and "speak" in query):
			user_wants_to_type = False
			speak("You can command me by saying anything. And you know how to type to command me")

		else:
			try:
				response_from_gpt = chat_with_google_bard(query)
				print(response_from_gpt)
				speak("According to Chat Gpt: ")
				speak(response_from_gpt)
			
			except Exception as e:
				print("I tried GPT, but failed to response due to :" , e)
				speak("I tried GPT, but failed to response")