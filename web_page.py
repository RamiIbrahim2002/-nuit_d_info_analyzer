import pandas as pd
import ollama
import json

def generate_challenge_insights(file_path):
    # Load the Excel sheet
    df = pd.read_excel(file_path)
    challenges_data = df[['Title', 'Details Section']].dropna()

    def call_mistral_api(challenge_name, challenge_details):
        try:
            messages = [
                {"role": "system", "content": "You are an AI assistant that summarizes challenges and provides insights."},
                {"role": "user", "content": f"Challenge: {challenge_name}\nDetails: {challenge_details}\nSummarize the challenge and provide insights."}
            ]
            
            response = ollama.chat(model="mistral", messages=messages)
            response_text = response.get('message', {}).get('content', 'No response text available')
            
            return response_text
        except Exception as e:
            return f"Error: {str(e)}"

    # Prepare results with insights
    results = []
    for _, challenge in challenges_data.iterrows():
        challenge_name = challenge['Title']
        challenge_details = challenge['Details Section']
        
        response_text = call_mistral_api(challenge_name, challenge_details)
        
        results.append({
            'Challenge Title': challenge_name,
            'Challenge Details': challenge_details,
            'AI Insights': response_text
        })

    # Generate HTML with embedded data
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackathon Challenge Insights</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold text-center mb-6 text-blue-600">Hackathon Challenge Insights</h1>
        
        <div class="grid md:grid-cols-3 gap-6">
            <div id="challengeList" class="md:col-span-1 bg-white shadow-md rounded-lg p-4">
                <h2 class="text-xl font-semibold mb-4">Challenges</h2>
                <!-- Challenge list will be populated here -->
            </div>

            <div id="challengeDetails" class="md:col-span-2 bg-white shadow-md rounded-lg p-6">
                <div class="text-center text-gray-500">
                    Select a challenge to view details
                </div>
            </div>
        </div>
    </div>

    <script>
    const challenges = {json.dumps(results)};

    const challengeList = document.getElementById('challengeList');
    const challengeDetails = document.getElementById('challengeDetails');

    // Populate challenge list
    challenges.forEach((challenge, index) => {{
        const challengeItem = document.createElement('div');
        challengeItem.className = 'cursor-pointer p-3 mb-2 rounded-lg hover:bg-gray-100';
        challengeItem.textContent = challenge['Challenge Title'];
        
        challengeItem.addEventListener('click', () => {{
            // Update challenge details
            challengeDetails.innerHTML = `
                <h2 class="text-2xl font-bold mb-4 text-blue-700">${{challenge['Challenge Title']}}</h2>
                
                <div class="mb-4">
                    <h3 class="font-semibold text-lg mb-2">Challenge Details</h3>
                    <p class="text-gray-700">${{challenge['Challenge Details']}}</p>
                </div>
                
                <div>
                    <h3 class="font-semibold text-lg mb-2">AI Insights</h3>
                    <p class="text-gray-800 italic">${{challenge['AI Insights']}}</p>
                </div>
            `;
        }});

        challengeList.appendChild(challengeItem);
    }});

    // Automatically select first challenge if exists
    if (challenges.length > 0) {{
        const firstChallenge = challenges[0];
        challengeDetails.innerHTML = `
            <h2 class="text-2xl font-bold mb-4 text-blue-700">${{firstChallenge['Challenge Title']}}</h2>
            
            <div class="mb-4">
                <h3 class="font-semibold text-lg mb-2">Challenge Details</h3>
                <p class="text-gray-700">${{firstChallenge['Challenge Details']}}</p>
            </div>
            
            <div>
                <h3 class="font-semibold text-lg mb-2">AI Insights</h3>
                <p class="text-gray-800 italic">${{firstChallenge['AI Insights']}}</p>
            </div>
        `;
    }}
    </script>
</body>
</html>
    '''

    # Write to file
    with open('challenge_insights_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Interactive dashboard has been generated as 'challenge_insights_dashboard.html'")

# Usage
generate_challenge_insights("detailed_nuit_de_l_info_challenges.xlsx")