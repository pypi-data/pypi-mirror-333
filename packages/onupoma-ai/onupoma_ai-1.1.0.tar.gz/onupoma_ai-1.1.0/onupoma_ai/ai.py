import requests

class OnupomaAI:
    def __init__(self, base_url="https://onupoma.top/chat.php?question="):
        self.base_url = base_url

    def get_response(self, user_input):
        """Get AI response from the API."""
        response = requests.get(f"{self.base_url}{user_input}")
        if response.status_code == 200:
            return response.text  # This assumes the API responds with text
        else:
            return "Sorry, there was an error in getting the AI response."

