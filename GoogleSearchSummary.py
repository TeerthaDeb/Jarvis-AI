import webbrowser
import wikipediaapi
from urllib.parse import quote
from Speak import speak

def get_president_info(country):
    """Get information about the current president of the specified country."""
    try:
        wiki_wiki = wikipediaapi.Wikipedia("en", user_agent="your_user_agent_here")
        page_py = wiki_wiki.page(f"List_of_current_heads_of_state_and_government#Current_heads_of_state")

        if not page_py.exists():
            return f"Information about the president of {country} not found."

        content = page_py.text
        start_index = content.find(f"{country}:")
        if start_index == -1:
            return f"Information about the president of {country} not found."

        end_index = content.find("\n", start_index)
        president_info = content[start_index:end_index].strip()
        return president_info

    except Exception as e:
        print("Error while fetching information from Wikipedia:", e)
        return "Error occurred while fetching information from Wikipedia."

def googleSearch(contentToSearch: str):
    """_summary_ : This function takes a content to search as input, opens a Google search page with the
    given content in the browser and prints information about the current president.

    Args:
        contentToSearch (string): the content to be searched 
    """
    try:
        # Create the Google search URL for the given query
        search_url = f"https://www.google.com/search?q={quote(contentToSearch)}&ie=UTF-8"

        # Open the Google search page in the default web browser
        webbrowser.open(search_url)

        speak(f"Searching Google for: {contentToSearch}")

        # Get information about the current president from Wikipedia
        president_info = get_president_info("United States")
        print(f"Information about the current president of the USA:\n{president_info}")
        speak(f"Information about the current president of the USA: {president_info}")

    except Exception as e:
        print("Error:", e)
        speak("Error occurred during Google search.")

# Test the function
googleSearch("who is the president of USA")
