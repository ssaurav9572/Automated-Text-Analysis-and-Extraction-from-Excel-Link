# Here I am extracting article title and article text and saving them in Output_Text_Files ,filename as their url id

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

file_path = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/Input.xlsx"  # Replace with the actual path to your Excel file
df = pd.read_excel(file_path)

# Output directory to save text files
output_dir = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/Output_Text_Files"
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist,true is used so that it doesn't give error .

# Read the Stop Words List
stopwords_dir = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/20211030 Test Assignment/StopWords"  # Change this to the actual path
stop_words = set()
for file in os.listdir(stopwords_dir):
    with open(os.path.join(stopwords_dir, file), 'r', encoding='latin-1') as f:
        stop_words.update(set(f.read().splitlines()))

# Read the Master Dictionary
sentiment_dir = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/20211030 Test Assignment/MasterDictionary"  # Change this to the actual path

positive_words = set()
negative_words = set()
for file in os.listdir(sentiment_dir):
    with open(os.path.join(sentiment_dir, file), 'r', encoding='latin-1') as f:
        if file == 'positive-words.txt':
            positive_words.update(f.read().splitlines())
        else:
            negative_words.update(f.read().splitlines())

# Extract the URLs and URL_IDs from the DataFrame
urls_and_ids = df[['URL', 'URL_ID']].values.tolist()

for url, url_id in urls_and_ids:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Create a BeautifulSoup object
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find and extract text
        article = ""
        for paragraph in soup.find_all('p'):  # based on our HTML structure
            article += paragraph.get_text() + '\n'

        # Save the article text to a text file
        output_file_path = os.path.join(output_dir, f"{url_id}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(article)

        print(f"Article for URL_ID {url_id} saved to {output_file_path}")

    except Exception as e:
        print(f"Error processing URL {url}: {e}")