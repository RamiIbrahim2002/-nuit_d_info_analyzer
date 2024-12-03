import pandas as pd

file_path = "detailed_nuit_de_l_info_challenges.xlsx"
df = pd.read_excel(file_path)

challenges_data = df[['Title', 'Details Section']].dropna() 

for index, row in challenges_data.iterrows():
    print(f"Challenge Name: {row['Title']}")
    print(f"Details Section: {row['Details Section']}")
    print("-" * 50)  # Separator between each challenge
