# Automated-Text-Analysis-and-Extraction-from-Excel-Link


# Web Scraping and Text Extraction Script

This Python script is designed to scrape text content from web pages and save it into individual text files. It utilizes the requests library to fetch web pages and BeautifulSoup for parsing HTML content.

URL Extraction from Excel: The script reads URLs and their corresponding IDs from an Excel file using the pandas library.

Text Extraction: It extracts text content from HTML pages by parsing them using BeautifulSoup. The script specifically targets <p> tags for text extraction, assuming a particular HTML structure.

Text File Generation: The extracted text is then saved into individual text files. Each text file is named based on the URL ID.

Error Handling: Exception handling is implemented to manage errors that may occur during the scraping process. It prints error messages if encountered and continues to the next URL.

# Sentiment Analysis and Readability Assessment Script

This Python script performs sentiment analysis and readability assessment on the extracted text from web pages. It utilizes libraries such as nltk for text processing and syllables for syllable count estimation.

Text Cleaning: The script cleans the extracted text by removing non-alphanumeric characters and converting it to lowercase.

Tokenization: It tokenizes the cleaned text into individual words for further analysis using the nltk library.

Sentiment Analysis: Sentiment scores including positive score, negative score, polarity score, and subjectivity score are calculated based on the presence of positive and negative words in the text.

Readability Analysis: Readability-related scores such as average sentence length, percentage of complex words, fog index, etc., are calculated to assess the readability of the text.

Output Generation: The results of sentiment analysis and readability assessment are stored in a DataFrame and saved to an Excel file for further analysis.

# Integration:

These scripts can be integrated to provide a comprehensive solution for web scraping, text extraction, sentiment analysis, and readability assessment tasks. The first script extracts text content from web pages, while the second script analyzes the extracted text for sentiment and readability metrics.

# Usage:

To use these scripts, provide the necessary input files such as the Excel file containing URLs and the directories containing stop words and sentiment dictionaries. Adjust the file paths accordingly in the scripts. After running the scripts, the extracted text will be saved into text files, and sentiment and readability analysis results will be saved into an Excel file.
