import subprocess

class Server:
    def __init__(self, command, cwd):
        self.command = command
        self.cwd = cwd

    def start_server(self):
        print("Starting the server to run model at localhost:8000 ...")
#        try:
        mlc_rest = subprocess.run(self.command, cwd=self.cwd, capture_output=True)
        return mlc_rest
   #     except Exception as e:
    #        print(f"Error in model chat server: {e}")
     #       return e
