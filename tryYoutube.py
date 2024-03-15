__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2023, Jarvis-AI" 
__credits__ = ["Harris Ali Khan"] 
__license__ = "MIT Licensing"  
__version__ = "1.0.1"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "GPT is here, Bard and sending email is coming soon..." 

import pywhatkit as kit
import time

def playMusicFromYouTube(search_query : str) -> None:
    """
        This Function plays video from youtube.com using search query provided by the user.
        ----------------
        Args:
            search_query (str): Name of the Video
        
        ---------------
        Returns:
            None
    """
    try:
        # Use pywhatkit to open the YouTube video in the default web browser
        kit.playonyt(search_query)

        # Wait for a few seconds to let the browser open
        time.sleep(5)
        print("Now playing" , search_query , "from YouTube.")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":

    # Example usage:
    search_query = "Despacito"
    playMusicFromYouTube(search_query)