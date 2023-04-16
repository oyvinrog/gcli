# Auto-complete for Windows Command Prompt using OpenAI GPT-3

This Python script helps in generating auto-complete suggestions for Windows command prompt using OpenAI's GPT-3 model. The script records the total tokens spent and the associated cost for each GPT-3 API call. The user can enter a command, and the script will provide auto-complete suggestions based on the input. The user can choose to execute the suggested command or enter a new command.

## Dependencies

- Python 3.6 or above
- openai
- os
- threading
- prompt_toolkit
- subprocess
- sqlite3

## Installation

1. Install the required dependencies:

```bash
pip install openai prompt_toolkit

2. Save your OpenAI API key in a file named "key.txt" in the same directory as the script.

## Usage

Run the script:

python script_name.py

Enter a command in the prompt and see auto-complete suggestions. Choose a suggested command or enter a new command to execute. Enter "exit" to quit the script.

