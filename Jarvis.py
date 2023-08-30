#jervis Beta 0.2
#created by 	: Maharaj Teertha Deb
#linked IN 		: https://www.linkedin.com/in/maharaj-teertha-deb/
#released on 	: August-26-2023


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
from pytube import YouTube
import pywhatkit as kit

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
		return "N+one"

	return query


def sendEmail(to , content):
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
    """
    Function to search for and play music from YouTube.
    """
    try:
        speak("Searching YouTube for " + search_query)
        kit.playonyt(search_query)
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I couldn't play the music from YouTube.")


################# Main Function Follows ::::::::::::::::::::::::::::::;;;;


if __name__ == "__main__":
	
	wishMe()
	while (True):
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

			except Exception as e:
					print("An error occurred:", e)

		# The code block elif ("open google" in query):is checking if the user's query contains the phrase "open
		# google". If it does, it opens the Google website in the default web browser using the
		# `webbrowser.open()` function. This allows the user to easily access the Google website by simply
		# saying "open google" to the personal assistant.
		elif ("open google" in query):
			webbrowser.open("https://www.google.com")

		# The code block elif ("open facebook" in query): checking if the user's query contains the phrase "open
		# facebook". If it does, it opens the Facebook website in the default web browser using the
		# `webbrowser.open()` function. This allows the user to easily access the Facebook website by simply
		# saying "open facebook" to the personal assistant.
		elif ("open facebook" in query):
			webbrowser.open("https://www.facebook.com")

		# The code block elif ("open gmail" in query): is checking if the user's query contains the phrase "open gmail".
		# If it does, it opens the Gmail website in the default web browser using the `webbrowser.open()`
		# function. This allows the user to easily access the Gmail website by simply saying "open gmail" to
		# the personal assistant.
		elif ("open gmail" in query):
			webbrowser.open("https://www.gmail.com")
		
		# The code block elif ("open linkedin" in query): is checking if
		# the user's query contains the phrase "open linkedin". If it does, it opens the LinkedIn website in
		# the default web browser using the `webbrowser.open()` function. This allows the user to easily
		# access the LinkedIn website by simply saying "open linkedin" to the personal assistant.
		elif ("open linkedin" in query):
			webbrowser.open("https://www.linkedin.com")
		
		# The code block elif ("open chatgpt" in query): is checking if
		# the user's query contains the phrase "open chatgpt". If it does, it opens the ChatGPT website
		# (chat.openai.com) in the default web browser using the `webbrowser.open()` function. This allows
		# the user to easily access the ChatGPT website by simply saying "open chatgpt" to the personal
		# assistant.
		elif ("open chat gpt" in query):
			webbrowser.open("https://www.chat.openai.com")

		# The code block `elif ("play music" in query)` is checking if the user's query contains the phrase
		# "play music". If it does, it tries to access a specified directory where the music files are
		# stored. It then retrieves a list of the music files in that directory using the `os.listdir()`
		# function and stores it in the `songs` variable. Finally, it plays the first song in the list by
		# using the `os.startfile()` function and passing the path of the song file as an argument. If there
		# is an error during this process, it prints the error message.
		elif ("play music" in query):
			try:
				music_dir = "" #Enter your directory here:::::::::::::::
				songs = os.listdir(music_dir)
				print(songs)
				os.startfile(os.path.join(music_dir , songs[0]))
			except Exception as e:
				print("Error :" , e)
		
		# The code block `elif ("the time" in query)` is checking if the user's query contains the phrase
		# "the time". If it does, it retrieves the current time using the
		# `datetime.datetime.now().strftime("%H:%M:%S")` function and stores it in the `strTime` variable.
		# It then prints the current time and speaks it using the `speak` function. This allows the personal
		# assistant to provide the user with the current time when asked.
		elif ("the time" in query) :
			strTime = datetime.datetime.now().strftime("%H:%M:%S")
			print("The current date and time are: " , strTime)
			speak(f"Sir, The time is, {strTime}")

		# The code block elif (("open code" or "visual studio code") in query):  is
		# checking if the user's query contains the phrase "open code" or "visual studio code". If it does,
		# it opens the Visual Studio Code application by using the `os.startfile()` function and passing the
		# path of the application executable file as an argument. This allows the user to easily open Visual
		# Studio Code by simply saying "open code" or "visual studio code" to the personal assistant.
		elif (("open code" or "visual studio code") in query):
			os.startfile("C:\\Users\\Teertha\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

		# The code block `elif ("email to me" in query)` is checking if the user's query contains the phrase
		# "email to me". If it does, it prompts the user to provide the content of the email by saying "What
		# should I write?". It then uses the `takeCommand()` function to convert the user's speech input
		# into text and stores it in the `content` variable. After that, it speaks the message "The email
		# has been sent". If there is an error during the process of sending the email, it prints the error
		# message and speaks "Sorry, I was not able to send the email due to [error message]".
		elif ("email to me" in query):
			try:
				speak("What should i write ?")
				content = takeCommand()
				#
				speak("the email has been sent")
			except Exception as e:
				print("Error :" , e)
				speak("Sorry , I was not able to send the email. dueto " , e)
		
		elif ("google" in query):
			search_query = query.replace("google" , "").strip()
			googleSearch(search_query)
		
		# The code snippet that handles a query related to weather. It first checks
		# if the word "weather" is present in the query. If it is, it extracts the search query by removing
		# the phrase "what is" and any leading or trailing spaces.
		elif "weather" in query:
			search_query = query.replace("what is", "").strip()
			search_url = f"https://www.google.com/search?q={search_query}"
			try:
				webbrowser.open(search_url)
				speak("The temperature is: ")
				try:
					response = requests.get(search_url)
					soup = BeautifulSoup(response.text, "html.parser")
					# Find and extract the main search result description
					search_result = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
					if search_result:
						speak(search_result.get_text())
					else:
						speak("I'm sorry, I couldn't find weather.")
				except Exception as e:
					print("Error:", e)
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
			speak("le that be a secret , but you can explore me ")
		
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
			break

