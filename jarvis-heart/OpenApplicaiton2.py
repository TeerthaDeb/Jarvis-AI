__author__ = "Maharaj Teertha Deb" 
__copyright__ = "Copyright 2024, Jarvis-AI" 
__credits__ = ["https://www.geeksforgeeks.org/open-applications-using-python/"]
__license__ = "MIT Licensing"  
__version__ = "1.2"
__maintainer__ = "Maharaj Teertha Deb" 
__email__ = "maharaj.deb@mail.concordia.ca" 
__status__ = "Google Bard Introduced." 

from AppOpener import open, close
from Speak import speak

def main(inp = None):
    print()
    print("1. Open <any_name> TO OPEN APPLICATIONS")
    print("2. Close <any_name> TO CLOSE APPLICATIONS")
    print()
    open("help")
    print("TRY 'OPEN <any_key>'")
    while True:
        inp = input("ENTER APPLICATION TO OPEN / CLOSE: ").lower()
        if "close " in inp:
            app_name = inp.replace("close ","").strip()
            close(app_name, match_closest=True, output=False) # App will be close be it matches little bit too (Without printing context (like CLOSING <app_name>))
        if "open " in inp:
            app_name = inp.replace("open ","")
            open(app_name, match_closest=True) # App will be open be it matches little bit too


def open_app(app_name : str) -> bool:
    
    try:
        open(app_name , match_closest=True , throw_error = True)
        print("Opened" , app_name)
        speak("Opened" + app_name)
        return True
    
    except Exception as e:
        print("\n\tERROR:\n\t",e,"\n")
        speak("Could not open")
        return False
    

def close_app(app_name : str) -> bool:
    try:
        close(app_name , match_closest=True , throw_error = True)
        print("closed" , app_name)
        speak("closed")
        return True
    
    except Exception as e:
        print("\n\tERROR:\n\t",e,"\n")
        speak("Could not close")
        return False


if __name__ == '__main__':
    open_app("chrome")