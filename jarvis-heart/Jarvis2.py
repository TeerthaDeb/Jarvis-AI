import os
import json
from datetime import datetime
from typing import Optional, Dict, Any

class UserManager:
    USER_FILE = "user_data.json"

    @staticmethod
    def get_user() -> Optional[Dict[str, Any]]:
        """Get user data from JSON file if it exists"""
        try:
            if os.path.exists(UserManager.USER_FILE):
                with open(UserManager.USER_FILE, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error reading user data: {str(e)}")
            return None

    @staticmethod
    def save_user(user_data: Dict[str, Any]) -> bool:
        """Save user data to JSON file"""
        try:
            with open(UserManager.USER_FILE, 'w') as f:
                json.dump(user_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving user data: {str(e)}")
            return False

    @staticmethod
    def create_new_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user with provided data"""
        # Ensure required fields
        required_fields = ['name', 'pronunciation', 'birth_date']
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field: {field}")

        # Add creation timestamp
        user_data['created_at'] = datetime.now().isoformat()
        
        # Save the user data
        if UserManager.save_user(user_data):
            return user_data
        raise Exception("Failed to save user data")

    @staticmethod
    def is_birthday_today(birth_date: str) -> bool:
        """Check if today is the user's birthday"""
        try:
            birth = datetime.fromisoformat(birth_date)
            today = datetime.now()
            return birth.month == today.month and birth.day == today.day
        except Exception:
            return False

    @staticmethod
    def get_greeting() -> Dict[str, str]:
        """Get appropriate greeting based on time of day and user data"""
        user_data = UserManager.get_user()
        if not user_data:
            return {
                "greeting": "Hello! I am Jarvis, your AI assistant.",
                "is_birthday": False
            }

        hour = datetime.now().hour
        call_them = user_data.get('pronunciation', '')
        greeting = ""

        # Check birthday
        is_birthday = UserManager.is_birthday_today(user_data['birth_date'])
        if is_birthday:
            age = datetime.now().year - datetime.fromisoformat(user_data['birth_date']).year
            greeting = f"Happy {age}th Birthday! "

        # Add time-based greeting
        if 0 <= hour < 12:
            greeting += f"Good Morning! {call_them}"
        elif 12 <= hour < 18:
            greeting += f"Good Afternoon! {call_them}"
        else:
            greeting += f"Good Evening! {call_them}"

        greeting += ". I am your personal assistant, Jarvis. How may I help you?"

        return {
            "greeting": greeting,
            "is_birthday": is_birthday
        }

# Example usage in Flask app:
"""
@app.route('/user/setup', methods=['POST'])
def setup_user():
    try:
        user_data = request.get_json()
        if not user_data:
            return jsonify({"error": "No user data provided"}), 400

        # Check if user already exists
        existing_user = UserManager.get_user()
        if existing_user:
            return jsonify({
                "message": "User already exists",
                "user": existing_user
            }), 200

        # Create new user
        new_user = UserManager.create_new_user(user_data)
        return jsonify({
            "message": "User created successfully",
            "user": new_user
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/greeting', methods=['GET'])
def get_greeting():
    try:
        greeting_data = UserManager.get_greeting()
        return jsonify(greeting_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
""" 