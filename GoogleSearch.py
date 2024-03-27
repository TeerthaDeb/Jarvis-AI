__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["Harris Ali Khan"] 
__license__ = "MIT Licensing"  
__version__ = "1.0.1"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "GPT is here, Bard and sending email is coming soon..."  

import webbrowser
from urllib.parse import quote
from Speak import speak

def googleSearch(contentToSearch: str):
    """_summary_ : This function takes a content to search as input, opens a Google search page with the
    given content in the browser.

    Args:
        contentToSearch (string): the content to be searched 
    """
    try:
        # Create the Google search URL for the given query
        search_url = f"https://www.google.com/search?q={quote(contentToSearch)}&ie=UTF-8"

        # Open the Google search page in the default web browser
        webbrowser.open(search_url)

        speak(f"Searching Google for: {contentToSearch}")

    except Exception as e:
        print("Error:", e)
        speak("Error occurred during Google search.")

# Test the function
if __name__ == "__main__":
    googleSearch("what are the 7 wonders of the world")
