# Jarvis-AI 2.0 on June 3, 2024

## Your Personal Assistant

Jarvis is a Python-based personal assistant that efficiently performs a variety of tasks, from answering questions to opening websites and even playing music directly from YouTube.

![Jarvis](https://static.wikia.nocookie.net/robotsupremacy/images/b/b0/JuARaVeInSy.png/revision/latest?cb=20150505043606)

### Features

- Seamlessly handles voice-based commands for diverse tasks.
- Searches information on Wikipedia and Google for quick insights.
- Opens popular websites like YouTube, Google, Facebook, and LinkedIn.
- Enables music playback from YouTube.
- Facilitates sending emails effortlessly.
- Provides real-time weather information.
- Can Play Music if you provide correct directory. <0.4.9>
- Has web Face. <2.0.0-beta>
- Uses local LLM via Ollama, also supports GPU acceleration. <2.0.0-beta>
- And more...

### Requirements:
- Python 3.8 or higher
- Node.js 20 or higher
- Ollama running
- Model llama 2 installed in ollama
- Docker and K8S running to follow 2.1 (but it takes around 10 minutes to install)
- (optional) GPU acceleration for faster performance only NVIDIA GPUs are supported this time 


### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/TeerthaDeb/Jarvis-AI.git
   ```

follow either 2.1 or 2.2

2.1 write 
   ```
   docker-compose up --build
   ```
   in your cli and it should build the docker image and then run Jarvis locally.

2.2 If you don't want dockerized version, you can install the requirements by running the following command in your terminal:
   ```
   cd Jarvis-AI
   cd jarvis-ui
   npm install
   ```
   and then run the following command in your terminal:
   ```
   cd Jarvis-AI
   cd jarvis-heart
   pip install -r requirements.txt
   ```
   all the requirements installed.
   now you can run the following command in your terminal:
   ```
   cd Jarvis-AI
   cd jarvis-heart
   python app.py
   ```
   in another terminal window, run the following command to run the UI:
   ```
   cd Jarvis-AI
   cd jarvis-ui
   npm run dev
   ```

3. Interact with Jarvis using voice commands. Some example commands:
   * At first it will ask your name and DOB for personalized response.
   * As long as you keep interacting with Jarvis, Jarvis will be more personal.

   * Ask some questions to Jarvis:
      - "What is the weather today?"
      - "Open YouTube"
      - "Play 'Calm Down' from YouTube"
      - "Tell me about Albert Einstein"
      - "Tell me a joke about python"
      - "what is the weather in my_city"
      - "I have some tomatoes and a can of tuna fish. What would be the best recipie". 
      - "Exit" or "Quit"

6. Change Log:

	## Version Beta : 0.2.1:
      * User can Type and Speak to command Jarvis
      * Opens some application using "Open Application function"
      * Better at playing youtube videos
		
	## Version Beta 0.4.9:
      * Able to Play Music
      * Issue on sending emails
      * GPT integration (Trial Mode)
      
   	## Version Beta 0.4.91
      * Better Weather using web scrapping.
      * Some features are still in development.
      * ChatGPT is Uniavailable in this version as it requires premium subscription.
      * Google Bard is being introduced.
   
	## Version Beta 0.4.92
      * Modules are on different files so easy to debug.
      * Playing song from youtube is perfect now.
      * It can now tell a joke.
      * Next version will be dedicated on Google Bard or User Based design.

	## Version Stable 1.00
      * Personalized Assistant.
      * GPT 3.5 : powered.
      * Improved Search Engine.
      * More Features.

   	## Version Stable 1.0.1
      * Some minor fixes on Joke and User class.
	  
	## Version 1.0.2:
      * Clean Code so it's easier to maintain and debug.
      * Better Weather Visual.
      * Able to tell location.
      * Able to open / close applicaitons.
      * ultimate requirements added for those who are not able to run it.

   	## Version 1.0.21:
      * Nice format for weather visuals.
      * Dependencies provided.

   	## Version 1.2:
      * Google Bard introduced.
        - Can answer any question based on the user input.
	  * Logic Improvements.

   ## Version 2.0.0-beta:
      * Uses Local LLM via Ollama to responds
      * Has a good UI to chat with,
      * Can play youtube video directly on your UI.
      * More features coming soon.


### Contributing

Contributions are highly encouraged! If you have improvements or new features to add, please create an issue or submit a pull request.

### Credits

Created by Maharaj Teertha Deb  
LinkedIn: [https://www.linkedin.com/in/maharaj-teertha-deb/](https://www.linkedin.com/in/maharaj-teertha-deb/)  
Portfolio: [https://teerthadeb.github.io/Portfolio/](https://teerthadeb.github.io/Portfolio/)


### Privacy
No data is sent to anywhere, all it is using is local LLM via Ollama. So your data is in your hand.


1st Released on: August 31, 2023

### Warning

This project is currently in Beta version. I am actively working on refining it and addressing any exceptions. As a solo developer, I appreciate your patience while I continue to enhance it. Feel free to use, contribute, and provide suggestions through email or direct messages.

Thank you for your interest and support!