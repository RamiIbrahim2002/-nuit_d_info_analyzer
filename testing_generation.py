import ollama

# Test function to call Mistral in chat mode
def test_mistral_chat():
    # Static test data
    test_name = "Sample Challenge"
    test_details = "This is a description of a sample challenge. Please summarize it and provide insights."

    # Construct the chat-based prompt
    chat_messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes challenges and provides insights."},
        {"role": "user", "content": f"Challenge: {test_name}\nDetails: {test_details}\n\nPlease summarize the challenge and provide insights."}
    ]

    # Print the prompt to check its structure
    print(f"Sending to Mistral Chat:\n{chat_messages}\n")

    try:
        # Call the Mistral model via Ollama API in chat mode
        response = ollama.chat(model="mistral", messages=chat_messages)

        # Print the raw response to debug
        print(f"Full response: {response}")

        # Extract the chat response
        response_text = response.get('text', 'No response text available')

        # If response is empty, handle it
        if response_text == 'No response text available':
            print("Warning: No valid response received.")
        else:
            print(f"Response text:\n{response_text}")

    except Exception as e:
        print(f"Error: {str(e)}")

# Run the test
test_mistral_chat()
