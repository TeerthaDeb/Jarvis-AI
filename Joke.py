import pyjokes
from Speak import speak

import pyjokes

def tell_joke(topic=None) -> None:
    """
    _summary_: This function tells a random joke.
    _return_: None
    Since: 0.4.92
    """

    if topic is None:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)
        return

    jokes = pyjokes.get_jokes(language='en')
    for joke in jokes:
        if topic.lower() in joke.lower():
            print(joke)
            speak(joke)
            return
        

# if __name__ == "__main__":
#     tell_joke("Java")