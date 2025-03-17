import requests
import subprocess
import time

class OllamaProvider:
    """A provider class to interact with Ollama LLMs"""

    def __init__(self, base_url = "http://localhost:11434", model="llama3", auto_start = True):
        """
        Initialize the Ollama Provider.

        :param base_url : Base URL of the Ollama server.
        :param model : The LLM model to use.

        Make sure ollama is installed 
        if not - curl -fsSL https://ollama.com/install.sh | sh
        """

        self.base_url = base_url
        self.model = model

        if auto_start and not self._is_ollama_running():
            print("Ollama is not running. Starting it now...")
            self._start_ollama()
            time.sleep(3)  # Give it a few seconds to start
    def _is_ollama_running(self):
        """
        Check if Ollama server is running.

        :return: True if running, False otherwise.
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _start_ollama(self):
        """
        Start the Ollama server.
        """
        try:
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            raise RuntimeError(f"Failed to start Ollama: {e}")
        

    
    def generate(self, prompt, stream=False):
        """
        Generate a response from the model.
        
        :param prompt : The input prompt string.
        :param stream : Weather to stream the response.
        :return : The generated response as a string
        """

        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model" : self.model,
            "prompt" : prompt,
            "stream" : stream
        }

        response = requests.post(endpoint, json=payload, stream=stream)

        if response.status_code != 200:
            raise Exception(f"Ollama API error : {response.text}")
        
        if stream:
            return (line.decode('utf-8') for line in response.iter_lines() if line)
        
        return response.json().get('response', "")
    
    def list_models(self):
        """
        List available models on the Ollama server.
        
        :return : A list of model names.
        """

        endpoint = f"{self.base_url}/api/tags"
        response = requests.get(endpoint)

        if(response.status_code != 200):
            raise Exception(f'Ollama API error : {response.text}')
        
        return [model["name"] for model in response.json().get("models", [])]
    
    def chat(self, messages):
        """
        Engage in a chat-style conversation.
        
        :param messages : A list of message dict.
        :return : Model reponse as a string."""

        endpoint = f"{self.base_url}/api/chat"
        payload = {
            "model" : self.model,
            "messages" : messages
        }
        response = requests.post(endpoint, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama API error : {response.text}")
        return response.json().get("message", {}).get("content", "")

