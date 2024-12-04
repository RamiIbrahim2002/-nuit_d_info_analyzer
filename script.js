// Fetch and process the .txt file
fetch('mistral_responses.txt')
    .then(response => response.text())
    .then(text => {
        const challenges = parseChallengesFromTxt(text);
        console.log("Parsed Challenges:", challenges);

        const challengeList = document.getElementById('challenge-list');
        const challengeTitle = document.getElementById('challenge-title');
        const challengeDetails = document.getElementById('challenge-details');
        const challengeInsights = document.getElementById('challenge-insights');

        // Populate the challenge list
        challenges.forEach((challenge, index) => {
            const listItem = document.createElement('li');
            listItem.textContent = challenge.title;
            listItem.onclick = () => {
                // Show details and insights when a challenge is clicked
                console.log("Selected Challenge:", challenge);
                challengeTitle.textContent = challenge.title;
                challengeDetails.innerHTML = formatText(challenge.details); // Use formatText for details
                challengeInsights.innerHTML = formatText(challenge.insights); // Use formatText for insights
            };
            challengeList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error loading challenges:', error));

// Function to parse the .txt file
function parseChallengesFromTxt(txt) {
    const challenges = [];
    const entries = txt.split("--------------------------------------------------");

    entries.forEach(entry => {
        if (entry.trim()) {
            const titleMatch = entry.match(/Response for '(.*?)':/);
            const title = titleMatch ? titleMatch[1] : "Unknown";

            const detailsStart = entry.indexOf("Details:") + "Details:".length;
            const insightsStart = entry.indexOf("Insights:");
            const details = entry.substring(detailsStart, insightsStart).trim();
            const insights = entry.substring(insightsStart + "Insights:".length).trim();

            challenges.push({
                title: title,
                details: details,
                insights: insights
            });
        }
    });
    return challenges;
}

// Function to format text with new lines after each period
function formatText(text) {
    // Add a newline after each period (.)
    return text.replace(/\./g, '.\n');
}
