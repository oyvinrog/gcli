"""'

Autocomplete in Windows terminal using openAI Davinci model

Example commands:

    show yellow text
    find all files containing "hello", 
    show files created last 3 days
    show files with size greater than 100MB
    show all hidden files
    show all files with extension .txt
    show all files with a number in the name

    
How do I estimate the cost of doing this?
------------------------------------------------
Lets say you write 30 commands every hour, and the cost of davinci is $0.0200 / 1K tokens
To estimate the cost of using the ChatGPT API, you'll need to consider the number of tokens in both input and output 
messages and the cost per token. In this example, let's assume that each command you send (including the input and output tokens) 
averages 50 tokens.

Calculate the total number of tokens per hour:
Number of commands per hour (30) * Average tokens per command (50) = 1500 tokens per hour

Calculate the hourly cost:
Tokens per hour (1500) / 1000 tokens (to convert to cost per 1K tokens) * Cost per 1K tokens ($0.0200) = $0.03 per hour

If you want to estimate the cost for a different duration, multiply the hourly cost by the number of hours. For example, to estimate
the cost for a month (assuming 30 days and constant usage):
Hourly cost ($0.03) * Hours per day (24) * Days per month (30) = $21.60

"""

import openai
import os
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
import subprocess
import sqlite3

def get_root_db_file():
    """Get root DB file"""

    root_db_file = "tokens.db"
    root_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), root_db_file)
    return root_db_path

def setup_db():
    """Setup local DB for logging tokens spent"""

    db = sqlite3.connect(get_root_db_file())
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tokens_spent (tokens INTEGER)")
    db.commit()
    db.close()

def log_tokens_spent(tokens):
    """Log tokens spent to a local DB """

    db = sqlite3.connect(get_root_db_file())
    cursor = db.cursor()
    setup_db()
    cursor.execute("INSERT INTO tokens_spent VALUES (?)", (tokens,))
    db.commit()
    db.close()

def get_tokens_spent():
    """Get tokens spent from local DB"""

    setup_db()

    db = sqlite3.connect(get_root_db_file())
    cursor = db.cursor()
    cursor.execute("SELECT coalesce(SUM(tokens),0) FROM tokens_spent")
    total = cursor.fetchone()[0]
    db.close()
    return total

def get_key():
    """Get openAI key from local file"""

    with open("key.txt", "r") as f:
        key = f.read().strip()
    return key

openai.api_key = get_key()

class ChatGPTCompleter(Completer):
    def __init__(self, debounce_time=0.5):
        self.debounce_time = debounce_time
        self.timer = None
        self.current_suggestions = []

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        if "just a test" in text:
            commands = ["auto1", "auto2", "this is a long text bla bla something else this is some more text bla bla bla bla bla"]
        else:
            commands = self.get_gpt_suggestions(text)
        
        for cmd in commands:
            yield Completion(cmd, start_position=-len(text))

    def get_gpt_suggestions(self, text):
        if not text.strip():
            return []

        # Cancel the previous timer if it exists
        if self.timer is not None:
            self.timer.cancel()

        # Create a new timer and start it
        self.timer = threading.Timer(self.debounce_time, self.fetch_gpt_suggestions, args=[text])
        self.timer.start()

        return self.current_suggestions

    def fetch_gpt_suggestions(self, text):
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",  # Change this to your preferred engine
                prompt="using Windows and CMD.exe assist with completing the following command. Don't show any extra text. just the command: " + text,
                max_tokens=700,
                n=3,
                stop=None,
                temperature=0.5,
            )

            self.current_suggestions = [choice.text.strip() for choice in response.choices]

            log_tokens_spent(response['usage']['total_tokens'])

        except Exception as e:
            print(f"Error: {e}")
            self.current_suggestions = []

# Initialize a PromptSession with the custom completer
session = PromptSession(completer=ChatGPTCompleter())


# use red color on command line
cost_so_far = get_tokens_spent()*0.0200/1000
print( "\033[1;31m" + "Tokens spent so far: " + str(get_tokens_spent()) + "\033[0;0m")
print( "\033[1;31m" + "Cost so far: $ " + str(cost_so_far) + "\033[0;0m")

# Main loop to receive input
while True:
    try:
        user_input = session.prompt("Enter your command: ")
        if user_input.lower() == "exit":
            break
        else:
            # run the command
            print("Running command: " + user_input)
            subprocess.run(user_input, shell=True)


    except KeyboardInterrupt:
        print("Exiting...")
        break
