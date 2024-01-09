import json
from transcriber import Transcriber
from chatbot import ChatBot
import os
from server import Server
from tokenizer import Tokenizer

def chatContext():
    tokenizer = Tokenizer()

    # Read the chat history
    with open('chat_history.txt', 'r') as f:
        chat_history = f.read()

    # Get the number of tokens in the chat history
    num_tokens = tokenizer.get_num_tokens(chat_history)

    # If the chat history is too long, trim it
    if num_tokens > 4096: # taking 8k as full context len, the chat context chosen is 4096 tokens
        tokens = tokenizer.tokenizer.encode(chat_history)
        # Remove tokens from the start until we have 4096 left
        while len(tokens) > 4096:
            tokens.pop(0)
        # Decode the tokens back into text
        chat_history = tokenizer.tokenizer.decode(tokens)

    # Add the chat history to the prompt
    return f"### Here's some context. Read this carefully, reason strongly and use this context to answer queries.\n{chat_history}"


def main():
    # Load the configuration
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Initialize the modules
    transcriber = Transcriber(config['transcribe']['main_path'], config['transcribe']['audio_folder'])
    chatbot = ChatBot(config['chat']['model'], config['chat']['url'])
    server = Server(config['server']['command'], config['server']['cwd'])

    # Start the server
    mlc_rest = server.start_server()
#    print(mlc_rest.stdout.decode('utf-8'))

    # Main interaction
    while True:
        print("1. send text, receive text (Text2Text)")
        print("2. send voice, receive text (Voice2Text)")
        print("3. send text, receive voice (Text2Voice)")
        print("4. send voice, receive voice (Voice2Voice)")
        print("5. Exit")
        choice = input("> ")

        if choice == "1":
            prompt = input("Enter your text: ")
        elif choice == "2":
            file_path = input("Name your .wav audio file from audio/ directory:: ")
            prompt = str(transcriber.transcribe_audio(file_path))
            if prompt is None: # transcription failed
                print("Failed to transcribe the audio. Please try again.")
                continue
        elif choice == "3" or choice == "4":
            print("Speech generation is in progress, library errors ..")
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice.")
            continue

        chat_context = str(chatContext())
        prompt_text = chat_context + "\n" + prompt
        response = chatbot.chat_with_model(prompt_text)
        if response is None:  # If the chat failed
            print("Failed to chat with the model. Please try again.")
            continue

        with open('chat_history.txt', 'a') as file:
            # Write the conversation to the text file
            file.write("### instruction \n" + prompt + "\n")
            file.write("### response \n" + response + "\n")
        print(f"Response from model:\n{response}\n")


if __name__ == "__main__":
    main()
