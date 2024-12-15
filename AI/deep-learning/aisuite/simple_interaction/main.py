import aisuite as ai
from os import getenv

# Initialize the AISuite client
client = ai.Client(
    {
        "openai": {"api_key": str(getenv("OPENAI_API_KEY")) }
    }
)

# Define the provider and model
models = ["openai:gpt-3.5-turbo", "llma3.2"]

# Set up the conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What’s the weather like in San Francisco?"},
]

# Generate the response
response = client.chat.completions.create(
    model=models[0],
    messages=messages,
)

# Display the response
print(response.choices[0].message.content)