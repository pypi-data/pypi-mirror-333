# Onupoma AI

A simple Python package that allows users to communicate with the Onupoma AI chatbot.

## Installation

You can install the package via pip:

```bash
pip install onupoma_ai
```
```bash
from onupoma_ai import OnupomaAI

# Replace this with your actual API key
api_key = "your_api_key_here"

# Initialize the OnupomaAI object with the API key
ai = OnupomaAI(api_key=api_key)

# Send a question to the AI and get a response
chat_input = "What is Onupoma?"
chat_response = ai.get_response(chat_input)
print(f"Chat Response: {chat_response}")

# Send a "think" message to the AI and get a response
think_input = "Think about what a PC is"
think_response = ai.get_think_response(think_input)
print(f"Think Response: {think_response}")
```
## Installation
Python 3.x
requests package (automatically installed via pip)
## License
This package is open-source and available under the MIT License.

## Contact
For API key requests, please contact MD Jakaria Fiad on Facebook.
Link : https://www.facebook.com/mdjakaria.fiad