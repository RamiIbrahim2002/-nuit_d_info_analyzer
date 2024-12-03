import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to clean text
def clean_text(text):
    return " ".join(text.split()) if text else ""

# Function to fetch detailed challenge data
def fetch_challenge_details(challenge_url):
    response = requests.get(challenge_url)
    if response.status_code != 200:
        return {
            "Logo": None,
            "Sponsor": None,
            "Theme": None,
            "Description": None,
            "Expected Elements": None,
            "Status": None,
        }

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the logo URL
    logo_tag = soup.find('img', {'src': lambda x: x and 'uploads/partenaires' in x})
    logo_url = logo_tag['src'] if logo_tag else None

    # Extract the sponsor name
    sponsor_tag = soup.find('h1')
    sponsor = clean_text(sponsor_tag.text) if sponsor_tag else None

    # Extract the theme
    theme_tag = soup.find('div', class_='alert alert-info')
    theme = clean_text(theme_tag.find('h4').text) if theme_tag else None

    # Extract the description
    description_paragraph = soup.find('p')
    description = clean_text(description_paragraph.text) if description_paragraph else None

    # Extract expected elements
    elements_section = soup.find('h2', string="Elements attendus")
    expected_elements = None
    if elements_section:
        next_div = elements_section.find_next('div', class_='alert alert-danger')
        expected_elements = clean_text(next_div.text) if next_div else None

    # Extract status (e.g., closed submissions)
    status_section = soup.find('div', class_='alert alert-danger')
    status = clean_text(status_section.text) if status_section else None

    return {
        "Logo": f"https://www.nuitdelinfo.com{logo_url}" if logo_url else None,
        "Sponsor": sponsor,
        "Theme": theme,
        "Description": description,
        "Expected Elements": expected_elements,
        "Status": status,
    }

# URL of the website
base_url = "https://www.nuitdelinfo.com"
challenges_url = f"{base_url}/inscription/defis/liste"

# Fetch the main page
response = requests.get(challenges_url)
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all challenge elements
    challenges = soup.find_all('div', class_='defi')

    # Prepare data storage
    data = []

    # Process each challenge
    for challenge in challenges:
        # Extract title and URL
        title_tag = challenge.find('div', class_='title').find('a')
        title = clean_text(title_tag.text)
        link = clean_text(title_tag['href'])
        
        # Ensure correct URL construction
        challenge_url = f"{base_url}{link}" if not link.startswith('http') else link

        # Extract prize details
        prize_div = challenge.find('div', class_='lot')
        prize = clean_text(prize_div.get_text(separator="\n")) if prize_div else "No prize details"

        # Fetch detailed challenge information
        details = fetch_challenge_details(challenge_url)

        # Append all data to the list
        data.append({
            "Title": title,
            "Link": challenge_url,
            "Prize": prize,
            "Logo": details["Logo"],
            "Sponsor": details["Sponsor"],
            "Theme": details["Theme"],
            "Description": details["Description"],
            "Expected Elements": details["Expected Elements"],
            "Status": details["Status"],
        })

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(data)
    output_file = "detailed_nuit_de_l_info_challenges.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data successfully written to {output_file}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
