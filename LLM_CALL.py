import pandas as pd
import ollama

# Load the Excel sheet created previously
file_path = "detailed_nuit_de_l_info_challenges.xlsx"
df = pd.read_excel(file_path)

# Extract the relevant columns: Title and Details Section
challenges_data = df[['Title', 'Details Section']].dropna()  # Drop rows with missing values

# Prepare the data to send to Mistral
challenges_data_list = challenges_data.to_dict(orient='records')

# Function to call Mistral model using Ollama for each challenge (using chat)
def call_mistral_api(challenge_name, challenge_details):
    try:
        # Create a conversation-style prompt
        messages = [
            {"role": "system", "content": "You are an AI assistant that summarizes challenges and provides insights."},
            {"role": "user", "content": f"Challenge: {challenge_name}\nDetails: {challenge_details}\nSummarize the challenge and provide insights."}
        ]
        
        # Call Mistral model via Ollama (using the chat endpoint)
        response = ollama.chat(model="mistral", messages=messages)

        # Extract the assistant's response
        response_text = response.get('message', {}).get('content', 'No response text available')

        # If no response text is returned, handle the response or try to debug
        if response_text == 'No response text available':
            response_text = f"Warning: No valid response for challenge '{challenge_name}'"
        
        return response_text
    except Exception as e:
        return f"Error: {str(e)}"

# Open a file to save the responses
with open('mistral_responses.txt', 'w', encoding='utf-8') as file:
    # Iterate over the challenges and get analysis for each
    for challenge in challenges_data_list:
        challenge_name = challenge['Title']
        challenge_details = challenge['Details Section']
        
        # Get Mistral's response for the current challenge
        response_text = call_mistral_api(challenge_name, challenge_details)
        
        # Write the response to the file
        file.write(f"Response for '{challenge_name}':\n")
        file.write(response_text + '\n')
        file.write("-" * 50 + '\n')  # Divider for clarity between challenge responses

print("Responses have been saved to 'mistral_responses.txt'.")
