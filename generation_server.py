from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('challenges.html')

@app.route('/api/challenges')
def get_challenges():
    try:
        # Read challenges from the .txt file
        with open('mistral_responses.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Format the data (assumes one challenge per line)
        challenges = {f"Challenge {i + 1}": line.strip() for i, line in enumerate(lines)}
        return jsonify(challenges)
    except FileNotFoundError:
        return jsonify({"error": "File 'mistral_responses.txt' not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
