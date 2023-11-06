from bardapi import Bard
import os

os.environ['_BARD_API_KEY'] = "bwgr6BvNaJJcIt1cvZ_uyp6T9R_iAbFcZDUTll51uh9uwjRhERe3l0Z_-t2qZ0c9OXp-ew."

try :
    # Set your input text
  input_text = "what is the easy way to integrate Python with Bard?"

  # Send an API request and get a response
  bard_output = Bard().get_answer(input_text)['content']
  print(bard_output)
except Exception as e:
  print("Error occurred: ", str(e))