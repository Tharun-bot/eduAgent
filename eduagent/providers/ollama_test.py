from ollama import OllamaProvider

def test_ollama():
    ollama = OllamaProvider(model="llama3", auto_start=True)  # Auto-start enabled
    response = ollama.generate("What is the capital of France?")
    print("Response:", response)

if __name__ == "__main__":
    test_ollama()