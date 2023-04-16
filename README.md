
# Auto-complete for Windows Command Prompt using OpenAI GPT-3

  

This Python script helps in generating auto-complete suggestions for Windows command prompt using OpenAI's GPT-3 model. The script records the total tokens spent and the associated cost for each GPT-3 API call. The user can enter a command, and the script will provide auto-complete suggestions based on the input. The user can choose to execute the suggested command or enter a new command.




## Usage

  

Run the script:

  

    python gcli.py

  

Enter a command in the prompt and see auto-complete suggestions. Choose a suggested command or enter a new command to execute. Enter "exit" to quit the script.

### Examples

![delete_empty_folders](https://user-images.githubusercontent.com/16526012/232335720-441d2474-bfb2-4b2a-8a53-ab60fe453d10.jpg)
![oracle_backup](https://user-images.githubusercontent.com/16526012/232335728-7418a158-5d3c-4cf5-b071-ea800da0ff1e.jpg)
![sqlserver_backup](https://user-images.githubusercontent.com/16526012/232335738-85c2f724-4ba9-4ee4-b4f3-3d98e1dff31c.jpg)

  
find all files containing "hello",

show files created last 3 days

show files with size greater than 100MB

show all hidden files

show all files with extension .txt

show all files with a number in the name
  
show all running processes

take an Oracle backup

take a SQL Server backup


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

pip install  openai  prompt_toolkit

```

  

2. Save your OpenAI API key in a file named "key.txt" in the same directory as the script.

  

