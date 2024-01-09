from transformers import AutoTokenizer
import json

class Tokenizer:
    def __init__(self, config_path='./config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.tokenizer = AutoTokenizer.from_pretrained(f'./dist/models/{self.config["tokenizer"]["model_path"]}', local_files_only=True, use_auth_token=False)
        print("tokenizer loaded")

    def get_num_tokens(self, input_text):
        encoded_input = self.tokenizer.encode(input_text)
        return len(encoded_input)
