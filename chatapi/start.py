import requests, os, time, json, sys
import keyboard

# Load the configuration file
with open('config.json', 'r') as f:
    config = json.load(f)

def main():
    """
    Main function to handle user input and make requests to the chat API.

    This function first presents the user with two options:
    1. Text to Text (Text2Text)
    2. Voice to Text (Voice2Text)

    Depending on the user's choice, it either:
    - Takes a text from the user and sends it as a payload to the endpoint (t2t mode), or
    - Waits for audio to be sent, then sends the filepath as payload to the endpoint (v2t mode).

    In then makes a POST request to the chat API and prints the response.

    If choice is not recognized, it prints an error message and exits.

    Raises:
        FileNotFoundError: If the audio file is not found after 5 minutes in Voice2Text mode.
    """
    while True:
        # Display options to the user
        print("\n1. Text to Text (Text2Text)")
        print("2. Voice to Text (Voice2Text)")
        print("3. Exit.")
        choice = input("> ")

        if choice == '3':
            print("exiting....")
            break
        # Handle Text to Text mode
        if choice == "1":
            MODE = "t2t"
            prompt = input("Enter your text: ")
            payload = {'prompt': prompt}
        # Handle Voice to Text mode
        elif choice == "2":
            MODE = "v2t"
            print("Run v2t.sh, waiting...")
            homepath = config['root']['homepath']
            filepath = f"/chatapi/audio/{config['transcribe']['audio_file_name']}.wav"
            start_time = time.time()
            last_size = -1
            # If running from host, `homepath` is required. Not needed when running from container.
            while True:
                # Check if the audio file exists and is still being written
                if os.path.exists(homepath + filepath):
                    curr_size = os.path.getsize(homepath + filepath)
                    # If file size hasn't changed, break the loop
                    if curr_size == last_size:
                        print("voice command is written successfully...")
                        break
                    else: 
                        last_size = curr_size
                # If .wav file is not available after 5 mins, raise an error
                if time.time() - start_time > 300: 
                    raise FileNotFoundError(f"{filepath} not found after 5 minutes.")
                time.sleep(1)  # Check every second
            payload = {'filepath': filepath}
            print(f"filepath: {filepath} \n payload: {payload}")
        else:
            print("Invalid choice..")
            continue

        # Make a POST request to the chat API
        URL = "http://localhost:8000"
        print(f"Calling URL: {URL}/{MODE} with payload: {payload}")
        response = requests.post(f"{URL}/{MODE}", json=payload, stream=True)
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                print(decoded_line)

if __name__ == "__main__":
    main()