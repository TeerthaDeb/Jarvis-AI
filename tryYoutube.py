import pywhatkit as kit
import webbrowser
import time

def playMusicFromYouTube(search_query):
    try:
        # Use pywhatkit to open the YouTube video in the default web browser
        kit.playonyt(search_query)

        # Wait for a few seconds to let the browser open
        time.sleep(5)

        # Get the URL from the webbrowser module
        url = webbrowser.open('about:blank')

        # Simulate clicking the play button (this won't interact with the webpage)
        print("Simulating click on the play button for URL:", url)

    except Exception as e:
        print("Error:", e)
