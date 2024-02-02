import datetime
import json
import os
import re
import webbrowser
from Speak import speak

user_directory_location = "C:\\Users\\Public\\Documents\\TDsoftwares\\JarvisAI"
user_file_path = os.path.join(user_directory_location, "User.MTD")


class User:

    def __init__(self, name=None, gender=None, pronunciation=None, bard_api=None, gpt_api=None, birth_date=None,
                 email=None, email_password=None):

        # Constructor calls methods to set attributes
        self.set_name(name)
        self.set_gender(gender)
        self.set_pronunciation(pronunciation)
        self.set_bard_api(bard_api)
        self.set_gpt_api(gpt_api)
        self.set_birth_date(birth_date)
        self.set_email(email)
        self.set_email_password(email_password)

    def validate_user_input(self, attribute, value):
        speak("Please check if the input is correct.")
        confirmation = input(f"You entered your {attribute} as {value}. Is this correct? (Yes/No): ").lower()
        if confirmation.startswith('y'):
            return value
        else:
            return self.get_user_input(attribute)

    def get_user_input(self, attribute):
        user_input = input(f"Enter your {attribute.replace('_', ' ')}: ")
        return self.validate_user_input(attribute, user_input)

    def set_name(self, name):
        
        if name is None:
            speak("Enter your name")
            name = self.get_user_input('name')

        while not re.match('^[a-zA-Z\s]*$', name):
            speak("Sorry, I didn't get that. Please enter a valid name.")
            name = self.get_user_input('name')

        self.name = name

    def set_gender(self, gender):
        if gender is None:
            speak("Now enter your gender")
            gender = self.get_user_input('gender')

        self.gender = "Male" if gender[0].lower() == 'm' else "Female"

    def set_pronunciation(self, pronunciation):
        if pronunciation is None:
            speak("What is your pronunciation")
            pronunciation = self.get_user_input('pronunciation')

        self.pronunciation = pronunciation

    def set_bard_api(self, bard_api):
        if bard_api is None:
            speak("Would you like to set up your Google Bard api? Only consider it if you are residing in the US. or You can use a vpn to connect your computer to the US server.")
            choice = input("Would you like to set up your bard_api? Only consider it if you are residing in the US. or You can use a vpn to connect your computer to the US server : ")
            

            if choice.lower()[0] == "y":
                print("I am suggesting you a website that helps you get your bard api key")
                speak("I am suggesting you a website that helps you get your bard api key")

                webbrowser.open("https://aibard.online/bard-api-key/")
                speak("When you have your key, paste it here and press enter")
                bard_api = input("Please copy and paste your BARD API Key here (or enter \"no key\" if you don't have it): ")

                if "no key" in bard_api.lower():
                    print("You can set it later.")
                    speak("You can set it later.")
                    self.bard_api = None

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
                    self.gpt_api = None
                
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
                                    print("I can't set your birth date with that value. Please try again.")
                                    speak("I can't set your birth date with that value. Please try again.")
                                    pass  # Handle the case where the input is still not a valid date format
        self.birth_date = birth_date

    def set_email(self, email):
        if email is None:
            while not email:
                speak("Enter your Email Address")
                email = self.get_user_input('email')

        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.email = email
        else:
            while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                speak("Enter your valid Email Address")
                email = self.get_user_input('email')
            self.email = email

    def set_email_password(self, password):
        if password is None:
            speak(f"{self.pronunciation}, please enter your email password. Only enter if you really want to send mail "
                  "and you trust me. Or skip it by pressing Enter or return")
            password = input(f"{self.pronunciation}, please enter your email password. Or skip it by pressing "
                             "\"Enter\" or \"return\": ")

            if password not in [None, '']:
                self.email_password = password
                speak("Thank you for the trust. Your password is safe with me, and nobody will know about it.")
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

def save_user_to_file(user):
    # Check if the directory exists, if not, create it
    if not os.path.exists(user_directory_location):
        os.makedirs(user_directory_location)

    user_dict = {
        'name': user.name,
        'gender': user.gender,
        'pronunciation': user.pronunciation,
        'bard_api': user.bard_api,
        'gpt_api': user.gpt_api,
        'birth_date': user.birth_date.strftime("%Y-%m-%d") if user.birth_date else None,
        'email': user.email,
        'email_password': user.email_password
    }

    with open(user_file_path, 'w') as json_file:
        json.dump(user_dict, json_file, indent=4)
        
def display_existing_user():
    # Check if the user file exists
    if os.path.exists(user_directory_location) and os.path.exists(user_file_path):
        with open(user_file_path, 'r') as json_file:
            user_dict = json.load(json_file)

        # Display the user information in a formatted way
        print("Existing User Information:")
        print("==========================")
        print(f"Name: {user_dict.get('name', '')}")
        print(f"Gender: {user_dict.get('gender', '')}")
        print(f"Pronunciation: {user_dict.get('pronunciation', '')}")
        print(f"BARD API Key: {user_dict.get('bard_api', '')}")
        print(f"Chat GPT API Key: {user_dict.get('gpt_api', '')}")
        birth_date_str = user_dict.get('birth_date', '')
        print(f"Birth Date: {datetime.datetime.strptime(birth_date_str, '%Y-%m-%d').strftime('%B %d, %Y')}" if birth_date_str else "Not provided")
        print(f"Email: {user_dict.get('email', '')}")
        print(f"Email Password: {user_dict.get('email_password', '')}")

        return False
    else:
        print("No existing user found.")
        return True

# Usage:
        

if __name__ == "__main__":
    if display_existing_user():
        user = User()
        print("\nUser Information:")
        print("=================")
        print(user.get_user_info())

        if user.is_birthday_today():
            age = datetime.datetime.now().year - user.birth_date.year
            print(f"\n{user.pronunciation}, Today is your {age}th birthday.")
            speak(f"{user.pronunciation}, Today is your {age}th birthday.")
        else:
            print("\nToday is not your birthday.")

        save_user_to_file(user=user)
