# Chat API
```
### Technical Challenge
#### Overview 
In this technical challenge, you are going to use what you have learned about the Jetson Orin to build a simple LLM API. 
The API is going to be used to provide real-time chat to a user, with a caveat — it is voice based. 
This means that you are going to have to integrate whisper within your API, to parse user commands, and successfully generate a response back. The response can be one of two types: 
1. The AI responding back via voice 
2. A simple textual response 
To do this, you will need the following: 
1. Whisper, running on the Jetson locally itself: 
2. MLC AI running the core API on the Orin:  
3. Jetson containers 
4. Text to speech model → This will allow the AI to respond as voice instead of text.
   
#### Requirements 
1. The API should have a endpoint that I can send a POST request to, in order to generate a completion 
2. This endpoint should accept a prompt in either text, or WAV file format
3. This endpoint should also allow the user to specify whether they want to receive back voice, or text 
a. If user wants to receive text, process the prompt with a model, and return text 
b. If the user wants to receive voice, process the prompt with a model, convert the processed text into voice using Coqui, and then return back the WAV file
 
To summarize, there will be 4 possible cases: 
* User sends text, wants to receive back text 
* User sends voice, wants to receive back text 
* User sends text, wants to receive back voice 
* User sends voice wants to receive back voice 
Your API should handle each of these cases gracefully. You must also think of possible edge cases where the input is out-of-format, or handle any associated errors without crashing. 
For the LLM running on the Jetson, you can use base Mistral-instruct-7B model. This model is built to follow instructions, and so can handle your requests well in most cases.

#### Completion criteria 
A successful implementation will be judge upon the following criteria:
1. Correctness: Does your code work for all 4 cases? 
2. Code quality: Is your code documented, easy to understand, and clean?
3. Efficiency: Is your code performant?
```
i'll try logging my problems & progress here.
