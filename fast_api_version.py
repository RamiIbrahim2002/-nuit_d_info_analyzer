from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Function to load and parse the .txt file
def load_txt_file(file_path):
    insights = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split content into sections for each challenge
            challenges = content.split("-" * 50)
            for challenge in challenges:
                if challenge.strip():  # Skip empty sections
                    lines = challenge.strip().split('\n')
                    
                    # Extract Title, Details, and Insights
                    title_line = lines[0] if lines else "Unknown"
                    title = title_line.replace("Response for '", "").replace("':", "").strip()
                    
                    # Find "Details:" and "Insights:"
                    details_start = challenge.find("Details:") + len("Details:")
                    insights_start = challenge.find("Insights:")
                    
                    details = challenge[details_start:insights_start].strip()
                    insights_text = challenge[insights_start + len("Insights:"):].strip()
                    
                    insights.append({
                        "title": title,
                        "details": details,
                        "insights": insights_text
                    })
    except Exception as e:
        print(f"Error loading file: {e}")
    return insights

# Load the insights at startup
file_path = "mistral_responses.txt"
insights = load_txt_file(file_path)

@app.get("/challenges")
def get_challenges():
    # Return only the titles with IDs
    return [{"id": idx, "title": item["title"]} for idx, item in enumerate(insights)]

@app.get("/challenge/{id}")
def get_challenge(id: int):
    # Return details and insights for a specific challenge
    if 0 <= id < len(insights):
        return insights[id]
    return JSONResponse({"error": "Invalid challenge ID"}, status_code=404)
