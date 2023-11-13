import requests
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import os
from nltk.tokenize import word_tokenize, sent_tokenize
import syllables

file_path = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/Input.xlsx"  # Input excel file
df = pd.read_excel(file_path) #dataframe is used with the help of pandas

# Read the Stop Words Lists
stopwords_dir = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/20211030 Test Assignment/StopWords"  # Change this to the actual path
stop_words = set()
for file in os.listdir(stopwords_dir):
    with open(os.path.join(stopwords_dir, file), 'r', encoding='latin-1') as f: # encoding is used to specifies the character encoding used to interpret the file's contents. In this case, it's set to 'latin-1'. The choice of encoding depends on the character set used in the file. 'latin-1' is a common encoding that covers a wide range of characters.
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
stopwords = set(stopwords.words('english')) #words, such as "the," "and," "is," etc., are frequently used in the English language but usually don't carry significant meaning in the context of certain analyses, such as sentiment analysis or readability assessment.

# Extract the URLs from the earlier  DataFrame
urls_and_ids = df[['URL', 'URL_ID']].values.tolist() #list of lists (urls and url_ids) from specific columns of a Pandas DataFrame (df). 
result_data = []

for url, url_id in urls_and_ids:
    try:
        def extract_article(url):
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            # Create a BeautifulSoup object
            soup = BeautifulSoup(response.content, 'html.parser')
            title_element = soup.find('h1')  # based on html structure
            if title_element:
                title = title_element.get_text()
            else:
                title = "Title not found"  

            # Find and extract text
            article = ""
            for paragraph in soup.find_all('p'):  #  based on our HTML structure
                article += paragraph.get_text() + '\n'
            
            return title, article

        # using tuple unpacking to assign the values returned by the extract_article function to the variables
        title, article_text = extract_article(url)

        # to remove non-alphanumeric characters, convert text to lowercase,etc.
        #using the re.sub function from the Python re (regular expression) module to remove characters from the text variable. 
        #The result is a string where only word characters and spaces are retained, effectively removing any non-alphanumeric and non-whitespace characters
        def clean_text(text):
            text = re.sub(r'[^\w\s]', '', text)
            text = text.lower()
            return text

        def calculate_readability(text):
            # Tokenize sentences,module to split a text into list of sentences(text variablein our case)
            sentences = sent_tokenize(text)

            # Calculate Average Sentence Length
            #word_tokenize function is applied to the string text, and the result is a list of words
            avg_sentence_length = len(word_tokenize(text)) / len(sentences)

            # Calculate Percentage of Complex Words
            #creating a list of words from the tokenized text where the estimated number of syllables per word is greater than 2
            complex_words = [word for word in word_tokenize(text) if syllables.estimate(word) > 2]
            percentage_complex_words = len(complex_words) / len(word_tokenize(text))

            # Calculate Fog Index
            fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

            # Calculate Average Number of Words Per Sentence
            avg_words_per_sentence = len(word_tokenize(text)) / len(sentences)

            # Calculate Complex Word Count
            complex_word_count = len(complex_words)

            # Calculate Word Count
            word_count = len([word for word in word_tokenize(text) if word.lower() not in stop_words])

            # Calculate Syllable Count Per Word
            # calculates the total number of syllables in a given text
            syllable_count = sum(syllables.estimate(word) for word in word_tokenize(text))
            syllable_per_word = syllable_count / len(word_tokenize(text))

            return avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, \
                   complex_word_count, word_count, syllable_per_word

        def calculate_sentiment_scores(tokens):
            positive_score = sum(1 for word in tokens if word in positive_words and word not in stop_words)
            negative_score = sum(1 for word in tokens if word in negative_words and word not in stop_words)

            # Calculate Polarity Score
            polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

            # Calculate Subjectivity Score
            subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)

            return positive_score, negative_score, polarity_score, subjectivity_score

        # Clean and tokenize text and remove non-alphanumeric characters and converts the text to lowercase
        cleaned_text = clean_text(article_text)
        #tokenizes the cleaned text into individual words using the word_tokenize function from the nltk.tokenize
        tokens = word_tokenize(cleaned_text)

        # Sentiment Analysis
        #calculating sentiment scores for the tokenized text and then unpacking those scores into individual variables
        sentiment_scores = calculate_sentiment_scores(tokens)
        positive_score, negative_score, polarity_score, subjectivity_score = sentiment_scores

        # Readability Analysis
        #calculating readability-related scores for the cleaned text and then unpacking those scores into individual variables
        readability_scores = calculate_readability(cleaned_text)
        avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, \
        complex_word_count, word_count, syllable_per_word = readability_scores

        # store the results in result data
        result_data.append({
            'URL id': url_id,
            'URL': url,
            'Positive Score': positive_score,
            'Negative Score': negative_score,
            'Polarity Score': polarity_score,
            'Subjectivity Score': subjectivity_score,
            'Average Sentence Length': avg_sentence_length,
            'Percentage of Complex Words': percentage_complex_words,
            'Fog Index': fog_index,
            'Average Number of Words Per Sentence': avg_words_per_sentence,
            'Complex Word Count': complex_word_count,
            'Word Count': word_count,
            'Syllable Per Word': syllable_per_word,
        })

    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        # Skip the rest of the processing for this URL
        continue

result_df = pd.DataFrame(result_data)

# Save the DataFrame to an Excel file
output_excel_path = "C:/Users/ssaur/OneDrive/Documents/blackcoffer/output4.xlsx"  # Output path
result_df.to_excel(output_excel_path, index=False) #index=False specifies that the DataFrame's index should not be included in the Excel.
print(f"Results saved to {output_excel_path}")