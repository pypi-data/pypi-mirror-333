import requests

class OnupomaAI:
    def __init__(self, api_key, base_url="https://onupoma.top/api/chat.php"):
        """
        Initialize the OnupomaAI with the required API key.
        
        :param api_key: Your API key for authentication.
        :param base_url: The base URL of the API (default is set to Onupoma AI's chat API).
        """
        self.api_key = api_key
        self.base_url = base_url

    def get_response(self, user_input):
        """
        Get AI response from the chat API.
        
        :param user_input: The text input to send to the AI.
        :return: AI response as text or an error message.
        """
        params = {
            "api_key": self.api_key,
            "question": user_input
        }
        
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            return response.text  # Assuming the API responds with plain text
        else:
            return f"Error: Unable to fetch response (Status Code: {response.status_code})"

    def get_think_response(self, user_input):
        """
        Get AI response from the think API.
        
        :param user_input: The text input to send to the AI.
        :return: AI think response as text or an error message.
        """
        think_url = "https://onupoma.top/api/think.php"
        params = {
            "api_key": self.api_key,
            "message": user_input
        }
        
        response = requests.get(think_url, params=params)
        
        if response.status_code == 200:
            return response.text  # Assuming the API responds with plain text
        else:
            return f"Error: Unable to fetch think response (Status Code: {response.status_code})"
