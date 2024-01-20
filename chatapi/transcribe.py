import subprocess
import re, os, time

class Transcribe:
    """
    Transcribe class is used to convert audio files into text using the
    whisper.cpp/main with ggml-base.en.bin as the default model.
    
    Attributes:
        cwd (str): The current working directory.
        audio_file_name (str): The name of the audio file to be transcribed.
        model (str): The model used for transcription.
        transcribe_pattern (regex): The regex to extract transcribed output from whisper.cpp/main `stdout`.
        stats_pattern (regex): the regex to extract the stats from whisper.cpp/main `stderr`
    """
    def __init__(self, cwd, audio_file_name, model):
        self.cwd = cwd
        self.audio_file_name = audio_file_name
        self.model = model
        self.transcribe_pattern = r"\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\]\s*(.+)"
        # This pattern is used to extract the stats (encode time and decode time) from the output
        self.stats_pattern = r"(whisper_print_timings:\s+(encode time|decode time).*)$"

    def transcribe(self, filepath):
        """
        Transcribes the audio file at the given filepath into text.
        
        Args:
            filepath (str): The path of the audio file to be transcribed.
            
        Returns:
            str: The transcribed text if successful, else an error message.
        """
        try:
            # Check if the file exists
            if not os.path.isfile(filepath):
                raise FileNotFoundError(f"The file '{audio_file_name}.wav' does not exist.")

            # Run the transcription
            process = subprocess.run(["./main", "-m", f"./models/{self.model}", "-f", filepath],
                                        cwd=self.cwd, capture_output=True)
            # Decode the output
            transcribe_str = process.stdout.decode('utf-8')
            print(f"transcribe_str: \n {transcribe_str}")
            stats_str = process.stderr.decode('utf-8')
            print(f"stats_str: \n {stats_str}")
            
            # Extract the transcribed text and stats from the output
            transcribe_pattern = self.transcribe_pattern
            transcribed = ""
            for match in re.finditer(transcribe_pattern, transcribe_str):
                transcribed += match.group(1)
                print(str(match.group(1)))
                time.sleep(0.1)
            print(f"you said: {transcribed}")
            print("voice transcription speed...\n")
            stats_pattern = self.stats_pattern
            for match in re.finditer(stats_pattern, stats_str, re.MULTILINE):
                print(match.group(1).split(':', 1)[1].strip())
            
            # Clean up the audio file
            try:
                os.remove(filepath)
                print("audiofile deleted")
            except Exception as e:
                print(e)
            
            return str(transcribed).strip()

        except Exception as e:
            return f"Error in transcribing audio: {e}"