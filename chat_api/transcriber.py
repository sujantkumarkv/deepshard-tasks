import subprocess
import re, os

class Transcriber:
    def __init__(self, main_path, audio_folder):
        self.main_path = main_path
        self.audio_folder = audio_folder

    def transcribe_audio(self, audio_file_path):
        try:
            # Check if the file exists
            if not os.path.isfile(self.audio_folder + audio_file_path):
                raise FileNotFoundError(f"The file '{audio_file_path}' does not exist.")

            # Check if the file is a .wav file
            if not audio_file_path.endswith('.wav'):
                print(f"The file '{audio_file_path}' is not a .wav file. Converting it to .wav format...\n ffmpeg is required, you can manually get it with: `apt update && apt-get install -y ffmpeg`")
                """
                # to install it with subprocess (not thourougly tested yet), the issue is with console printing, I don't want the user to get bombarded with install statements in chat app.
                command = ["apt", "update"]
                process = subprocess.run(command, capture_output=True)
                if process.returncode != 0:
                    print(f"Failed to run command: {process.stderr.decode()}")
                else:
                    print(f"Command output: {process.stdout.decode()}")
                
                command = ["apt-get", "install", "-y", "ffmpeg"]
                process = subprocess.run(command, capture_output=True)
                if process.returncode != 0:
                    print(f"Failed to run command: {process.stderr.decode()}")
                else:
                    print(f"Command output: {process.stdout.decode()}")
                """
                subprocess.run(["ffmpeg", "-i", self.audio_folder + audio_file_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", self.audio_folder + audio_file_path + ".wav"], cwd=self.main_path)
                audio_file_path += ".wav"

            result = subprocess.run(["whisper.cpp/main", "-f", self.audio_folder + audio_file_path], cwd=self.main_path, capture_output=True)
            output_str = result.stdout.decode('utf-8')
            pattern = r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*(.+)"
            matches = re.findall(pattern, output_str)
            text = " ".join(matches)
            return text
        except Exception as e:
            print(f"Error in transcribing audio: {e}")
