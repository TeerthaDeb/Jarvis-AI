import os, requests, json
import torch
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from ollama import Client
from Jarvis2 import UserManager
from functools import wraps
import re
from datetime import datetime
from pytube import YouTube, Search
from urllib.parse import quote_plus
import threading
from queue import Queue
import time
import traceback

# Configure Ollama Host - Read from environment variable or use default
OLLAMA_HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
print(f"Using Ollama host: {OLLAMA_HOST}")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")


if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.backends.cudnn.benchmark = True
    print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
    print(f"CUDA Memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")


app = Flask(__name__)
MODEL_NAME = "llama2"
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


client = Client(host=OLLAMA_HOST)

# Set system instructions for the model
SYSTEM_INSTRUCTIONS = """You are Jarvis, a professional AI assistant, made by Maharaj Teertha Deb. 
Respond directly and professionally in plain text. 
Do not use roleplay actions like *adjusts turban*, *smiling* or *chuckles* or nothing like this.
Do not use emojis, decorative symbols, or any special characters.
Focus on providing clear, helpful information, if possible keep it short answer. 
If you don't know just say you don't know or you are not confident."""

# Initialize model with system instructions
try:
    client.pull(MODEL_NAME)  # Ensure model is pulled
    client.create(
        model=MODEL_NAME,
        system=SYSTEM_INSTRUCTIONS,
        options={
            "num_gpu": 1 if torch.cuda.is_available() else 0,
            "num_thread": 6,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "repeat_penalty": 1.1,
            "stop": ["</s>", "Human:", "Assistant:"]
        }
    )
    print(f"Model {MODEL_NAME} initialized with system instructions")
except Exception as e:
    print(f"Error initializing model: {str(e)}")
    print(traceback.format_exc())

# Initialize user manager
try:
    user_manager = UserManager()
    print("User manager initialized successfully")
except Exception as e:
    print(f"Error initializing user manager: {str(e)}")
    print(traceback.format_exc())
    user_manager = None

# Constants
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL_NAME = "llama2"
MAX_CONCURRENT_REQUESTS = 1  
REQUEST_TIMEOUT = 30  

# Request queue and semaphore for rate limiting
request_queue = Queue()
request_semaphore = threading.Semaphore(MAX_CONCURRENT_REQUESTS)

# Response cache and chat history
response_cache = {}
chat_history = {}  # Store chat history per user
CACHE_DURATION = 300

def get_chat_history(user_id: str = 'default', max_history: int = 5) -> str:
    """Get formatted chat history for the user"""
    if user_id not in chat_history:
        chat_history[user_id] = []
    return "\n".join(chat_history[user_id][-max_history:])



def add_to_history(user_id: str, query: str, response: str):
    """Add a conversation turn to history"""
    if user_id not in chat_history:
        chat_history[user_id] = []
    chat_history[user_id].append(f"User: {query}\nAssistant: {response}")



def get_cached_response(prompt: str) -> str:
    """_summary_

    Args:
        prompt (str): _description_

    Returns:
        str: _description_
    """
    if prompt in response_cache:
        timestamp, response = response_cache[prompt]
        if time.time() - timestamp < CACHE_DURATION:
            return response
        del response_cache[prompt]
    return None



def cache_response(prompt: str, response: str):
    """_summary_

    Args:
        prompt (str): _description_
        response (str): _description_
    """
    response_cache[prompt] = (time.time(), response)




def get_ollama_response_stream(prompt: str):
    """Stream response from Ollama"""
    try:
        cached_response = get_cached_response(prompt)
        if cached_response:
            yield f"data: {json.dumps({'token': cached_response, 'done': True})}\n\n"
            return

        with request_semaphore:
            full_response = ""
            
            # Streaming reply
            for chunk in client.generate(
                model=MODEL_NAME,
                prompt=prompt,
                stream=True  #
            ):
                if 'response' in chunk:
                    token = chunk['response']
                    full_response += token
                    
                    # Send each token as Server-Sent Event
                    yield f"data: {json.dumps({'token': token, 'done': False})}\n\n"
                
                if chunk.get('done', False):
                    yield f"data: {json.dumps({'token': '', 'done': True})}\n\n"
                    break
            
            # Cache the complete response
            cache_response(prompt, full_response)

    except Exception as e:
        print(f"Streaming error: {str(e)}")
        error_msg = f"Error: {str(e)}"
        yield f"data: {json.dumps({'token': error_msg, 'done': True, 'error': True})}\n\n"




@app.route('/user/status', methods=['GET'])
def check_user_status():
    """Check if user setup is complete."""
    try:
        if user_manager is None:
            return jsonify({
                "error": "User manager not initialized",
                "status": "error"
            }), 500

        user = user_manager.get_user()
        if user:
            return jsonify({
                "status": "setup_complete",
                "user": user,
                "greeting": user_manager.get_greeting()
            })
        return jsonify({
            "status": "setup_required",
            "message": "User setup is required"
        })
    except Exception as e:
        print(f"Error in check_user_status: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": "Internal server error",
            "details": str(e),
            "status": "error"
        }), 500





@app.route('/user/setup', methods=['POST'])
def setup_user():
    """Handle user setup."""
    try:
        if user_manager is None:
            return jsonify({
                "error": "User manager not initialized",
                "status": "error"
            }), 500

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required_fields = ['name', 'pronunciation', 'birth_date']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create user data dictionary
        user_data = {
            'name': data['name'],
            'pronunciation': data['pronunciation'],
            'birth_date': data['birth_date'],
            'created_at': datetime.now().isoformat()
        }

        # Create new user with the dictionary
        user = user_manager.create_new_user(user_data)
        return jsonify({"status": "success", "user": user})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error during user setup: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500





@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "No query provided"}), 400

        query = data['query'].lower()
        speech_mode = data.get('speech_mode', False)
        stream = data.get('stream', False)

        # Handle YouTube requests (non-streaming)
        if any(phrase in query for phrase in ['play', 'youtube']):
            search_query = extract_youtube_query(query)
            video_id, video_title = search_youtube_video(search_query)
            
            if video_id:
                response = f"Playing '{video_title}' on YouTube"
                return jsonify({
                    "type": "youtube",
                    "videoId": video_id,
                    "response": response
                })
            else:
                return jsonify({
                    "type": "text",
                    "response": f"Sorry, I couldn't find a video for '{search_query}'. Please try a more specific search term."
                })

        print("Going to ask LLM")
        user = user_manager.get_user()
        user_id = user['name'] if user else 'default'

        # Get chat history
        history = get_chat_history(user_id)

        if user:
            prompt = f"""{history}
            User: {user['name']} ({user['pronunciation']}).
            Query: {query}
            Assistant:"""
        else:
            prompt = f"""{history}
            User: {query}
            Assistant:"""

        # Return streaming response if requested
        if stream:
            def generate_stream():
                yield "data: {\"start\": true}\n\n"
                full_response = ""
                for chunk in get_ollama_response_stream(prompt):
                    if isinstance(chunk, str) and chunk.startswith('data: '):
                        try:
                            data = json.loads(chunk[6:])
                            if data.get('token'):
                                full_response += data['token']
                            if data.get('done'):
                                add_to_history(user_id, query, full_response)
                        except json.JSONDecodeError:
                            pass
                    yield chunk
            
            return Response(
                generate_stream(),
                mimetype='text/plain',
                headers={
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Access-Control-Allow-Origin': 'http://localhost:5173',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            )
        else:
            # Non-streaming response (existing behavior)
            full_response = ""
            for chunk in get_ollama_response_stream(prompt):
                if isinstance(chunk, str):
                    try:
                        data = json.loads(chunk.replace('data: ', ''))
                        if 'token' in data:
                            full_response += data['token']
                    except json.JSONDecodeError:
                        continue
            
            return jsonify({
                "type": "text",
                "response": full_response
            })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500
    




def check_user_setup(f : callable) -> callable:
    """Check if user setup is complete.
    Args:
        f (callable): The function to decorate.

    Returns:
        callable: The decorated function.

    Updated on : 2.0.0
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not UserManager.get_user():
            return jsonify({
                "error": "User setup required",
                "message": "Please complete user setup before using this endpoint",
                "requires_setup": True
            }), 403
        return f(*args, **kwargs)
    return decorated_function




def extract_youtube_query(query: str) -> str:
    """_summary_

    Args:
        query (str): _description_

    Returns:
        str: _description_
    """
    
    query = query.lower()
    query = re.sub(r'play\s+', '', query)
    query = re.sub(r'\s+from\s+youtube', '', query)
    query = re.sub(r'on\s+youtube', '', query)
    query = re.sub(r'a\s+video', '', query) 
    query = query.strip()
    
    if not query:
        return "music"
    return query





def search_youtube_video(query: str) -> tuple[str, str]:
    """_summary_ 

    Args:
        query (str): _description_

    Returns:
        tuple[str, str]: _description_
    """
    try:
        # Format the search query
        search_query = quote_plus(query)
        search_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        # Get the search results page
        response = requests.get(search_url)
        response.raise_for_status()
        
        # Extract video ID from the response
        video_id_match = re.search(r"videoId\":\"(.+?)\"", response.text)
        if not video_id_match:
            return None, None
            
        video_id = video_id_match.group(1)
        
        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            return video_id, yt.title
        except Exception as e:
            print(f"Error getting video details: {str(e)}")
            return video_id, "YouTube Video"  # Return generic title if we can't get the actual one
            
    except Exception as e:
        print(f"Error searching YouTube: {str(e)}")
        return None, None




if __name__ == '__main__':
    print(f"Starting Flask server with Ollama model: {MODEL_NAME}")
    print(f"Using device: {device}")

    if torch.cuda.is_available():
        print(f"CUDA Device: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
    print("Make sure Ollama is running on http://localhost:11434")
    

    if user_manager is not None:
        try:
            user_status = user_manager.get_user()
            if not user_status:
                print("WARNING: No user setup found. User setup will be required before using the chat features.")
            else:
                print(f"User setup found for: {user_status.get('name', 'Unknown user')}")
        except Exception as e:
            print(f"Error checking user status at startup: {str(e)}")
    else:
        print("WARNING: User manager not initialized. User features will not be available.")
    
    app.run(debug=True, port=5000, threaded=True) 