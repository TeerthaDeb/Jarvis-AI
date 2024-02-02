import pywhatkit as kit
import time

def playMusicFromYouTube(search_query):
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
    search_query = "Despacito"  # Replace with the desired search query
    playMusicFromYouTube(search_query)
