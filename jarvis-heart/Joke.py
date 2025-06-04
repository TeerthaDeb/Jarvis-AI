__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = [] 
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 


import pyjokes
from Speak import speak
import User
from tryGPT import ask_gpt
from tryBard import ask_gemini



import datetime
import pyjokes
import random

def tell_joke(boss : User , topic=None) -> None:
    """
    _summary_: This function tells a random joke.
    _return_: None
    
    Since: 0.4.92
    
    Updated : 1.0.1 , 
    			1.2 : Added gemini support.
    """

    if topic is None:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)
        return

    jokes = pyjokes.get_jokes(language='en')

    container = []

    for joke in jokes:
        if topic.lower() in joke.lower():
            container.append(joke)

    ## tell a random joke from the container
    if len(container) != 0:
        the_joke = container[random.randint(0 , len(container) - 1)]
        print(the_joke)
        speak(the_joke)
    
    else:
        try:
            ask_gpt(f"tell me a joke on {topic}" , boss.gpt_api , boss.name , int(datetime.datetime.now().year - boss.birth_date.year))
        except Exception as e:
            ask_gemini(f"tell me a joke on {topic}" , boss.bard_api)
             

        

if __name__ == "__main__":
    tell_joke(boss = None , topic = "Google Bard")