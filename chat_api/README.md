Here's a loom explaining the tasks done, click [here](https://www.loom.com/share/5925ff5caff640739b4391917f3b83d7?sid=0bd7a895-a194-484a-9d3f-da39e10db4d5) !!!

The current code is hacked out in a few days like a hackathon.

So, Possible improvements:

* coqui TTS (text to speech) doesn't work, I had installation issues, whether try that or maybe try another TTS model.
* the current hacked out code reads the chat history from a file every time it runs. Its slow if chat history grows large, it would be efficient to keep chat history in memory and write when necessary.
* Also, I can just store tokens & tokenize each message as its added to chat_history.txt file instead of raw text. Earlier I assumed, the user might want to see their chats, but then can retokenize then, and it should not hurt the perf now.
* parallelize multiple indpendent tasks: probably use the `multiprocessing` module in python.
