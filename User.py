import datetime
import json
import os
import re
import webbrowser


from Speak import speak

user_directory_location = "C:\\Users\\Public\\Documents\\TDsoftwares\\JarvisAI"
user_file_path = os.path.join(user_directory_location, "User.MTD")


class User:

    def __init__(self , name = None ,  gender = None ,  pronunciation = None , bard_api = None , gpt_api = None , birth_date = None , email = None , email_password = None):

        # Constructor calls methods to set attributes
        self.set_name(name)
        self.set_gender(gender)
        self.set_pronunciation(pronunciation)
        self.set_bard_api(bard_api)
        self.set_gpt_api(gpt_api)
        self.set_birth_date(birth_date)
        self.set_email(email)
        self.set_email_password(email_password)

    def set_name(self ,  name):
        
        if (name == None):
            speak("Enter your name")
            name  = input("What is your name? ")
        
        while not re.match('^[a-zA-Z\s]*$', name):
            speak("Sorry I didn't get that. Please enter a valid name.")
            name = input("What is your name? ")
            print("Invalid characters in the username.")
        
        self.name = name

    def set_gender(self , gender):
        if gender  == None :
            speak("Now enter your gender")
            gender = input(f"Hello, {self.name}, Enter your gender (Male/Female): ")
                    
        self.gender = "Male" if gender[0].lower() == 'm' else "Female"

    def set_pronunciation(self , pronunciation):
        if pronunciation == None:
            speak("what is your pronounciation")
            pronounciation = input(f"{self.name} what is your pronounciation (Sir/Madam)?: ")
        
        self.pronunciation =  pronounciation

    def set_bard_api(self , bard_api):
        if bard_api == None:
            speak("Would you like to set up your Google Bard api? Only consider it if you are residing in the US. or You can use a vpn to connect your computer to the US server.")
            choice = input("Would you like to set up your bard_api? Only consider it if you are residing in the US. or You can use a vpn to connect your computer to the US server : ")
            
            if choice[0] == "y" or  choice[0] == "Y":
                print("I am suggesting you a website which helps you to get your bard api key")
                speak("I am suggesting you a website which helps you to get your bard api key")
                
                webbrowser.open("https://aibard.online/bard-api-key/")
                speak("When you have your key, paste it  here and press enter")
                bard_api = input("Please copy and paste your BARD API Key here (or enter \"no key\" if you don't have it): ")
                
                if("no key" in bard_api):
                    print("You can set it later.")
                    speak("You can set it later.")
                    return
        self.bard_api = bard_api
                
                


    def set_gpt_api(self, gpt_api):
        if gpt_api is None:
            speak("Would you like to set up your GPT API? Consider it only if you have a valid API key.")
            choice = input("Would you like to set up your GPT API? Consider it only if you have a valid API key (yes / no): ")
            
            
            if choice[0].lower() == "y":
                print("You can obtain your Chat GPT API key from the OpenAI website.")
                speak("You can obtain your Chat GPT API key from the OpenAI website.")
                
                webbrowser.open("https://platform.openai.com/api-keys")
                speak("When you have your key, paste it here and press enter.")
                gpt_api = input("Please copy and paste your Chat GPT API Key here (or enter \"no key\" if you don't have it): ")
                
                
                if "no key" in gpt_api.lower():
                    print("You can set it later.")
                    speak("You can set it later.")
                    return

        self.gpt_api = gpt_api

    def set_birth_date(self, birth_date):
        if birth_date is None:
            while not birth_date:
                speak("Please enter your birth date")
                user_input = input("Enter your birth date (in any format, e.g., MM/DD/YYYY): ")
                
                try:
                    birth_date = datetime.datetime.strptime(user_input, "%m/%d/%Y").date()
                except ValueError:
                    try:
                        birth_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()
                    except ValueError:
                        while not birth_date:
                            speak("Please enter your birth date in a valid format")
                            user_input = input("Enter your birth date (in any format, e.g., MM/DD/YYYY): ")
                            try:
                                birth_date = datetime.datetime.strptime(user_input, "%m/%d/%Y").date()
                            except ValueError:
                                try:
                                    birth_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()
                                except ValueError:
                                 print("I can't set you'r  birth date with that value. Please try again.")
                                 speak("I can't set you'r  birth date with that value. Please try again.")
                                 pass  # Handle the case where the input is still not a valid date format
        self.birth_date = birth_date


    def set_email(self , email):
        if email == None:
            while not email:
                speak("Enter your Email Addres")
                email = input('What\'s your email: ')
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.email = email
        else:
            while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                speak("Enter your valid Email Addres")
                email = input('What\'s your email: ')
            self.email = email

    def set_email_password(self , password):
        if password == None:
            speak(f"{self.pronunciation}, please enter your email password. Only Enter if you really want to send mail and you trust me. Or skip it by pressing Enter or return")
            password = input(f"{self.pronunciation}, please enter your email password. Or skip it by pressing \"Enter\" or \"return\" : ")
            if password not  in [None,''] :
                self.email_password=password
                speak("Thank you for the trust. Your password is safe with me and no body will know about it.")
            else:
                self.email_password = " "
		

    def get_user_info(self) -> dict:
        return {
            "Name": self.name,
            "Gender": self.gender,
            "Pronunciation": self.pronunciation,
            "BARD API Key": self.bard_api,
            "Chat GPT API Key": self.gpt_api,
            "Birth Date": self.birth_date.strftime("%Y-%m-%d") if self.birth_date else "Not provided",
            "Email": self.email,
            "Email Password": self.email_password
        }

    def is_birthday_today(self) -> bool:
        if self.birth_date:
            today = datetime.date.today()
            return today.month == self.birth_date.month and today.day == self.birth_date.day
        return False


# Usage:
if __name__ == "__main__":
    user = User()
    print(user.get_user_info())
    if user.is_birthday_today():
        print("Happy Birthday!")
    else:
        print("Today is not your birthday.")
