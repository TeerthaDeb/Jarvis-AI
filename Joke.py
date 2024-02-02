import pyjokes
from Speak import speak

import pyjokes
import random

def tell_joke(topic=None) -> None:
    """
    _summary_: This function tells a random joke.
    _return_: None
    Since: 0.4.92
    Updated : 0.4.93
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
    the_joke = container[random.randint(0 , len(container) - 1)]
    print(the_joke)
    speak(the_joke)
        

if __name__ == "__main__":
    tell_joke("Python")