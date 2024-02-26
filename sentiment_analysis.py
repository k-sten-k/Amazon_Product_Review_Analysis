# This program performs sentiment analysis and review similarity of Amazon product reviews.

# Importing libraries
import pandas as pd
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

# Loading a smaller spaCy English model
nlp = spacy.load('en_core_web_sm')

# Add the SpacyTextBlob component to perform sentiment analysis
nlp.add_pipe('spacytextblob')


# Preprocessing function to tokenize, lemmatize, and remove stopwords and punctuation
def preprocess(text):
    """
    Preprocesses the input text by tokenizing, lemmatizing, and removing stopwords and punctuation.
    """
    doc = nlp(text)
    return ' '.join([token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct])

# Sentiment analysis function using the SpacyTextBlob component
def analyze_sentiment(text):
    """
    Analyzes the sentiment of the input text using the SpacyTextBlob component.
    """
    doc = nlp(text)
    polarity = doc._.blob.polarity      # Extracting polarity score
    sentiment = doc._.blob.sentiment    # Extracting sentiment score
    label = "positive" if polarity > 0 else ("negative" if polarity < 0 else "neutral")     # Labeling sentiment
    return {"polarity": polarity, "sentiment": sentiment, "label": label}       # Returning dictionary containing sentiment analysis results 


# Reading Amazon reviews CSV file into DataFrame, removing rows with missing review text
df = pd.read_csv('amazon_product_reviews.csv', sep=',')
df = df.dropna(subset=['reviews.text'])  

# Selecting only the review text column
df = df[['reviews.text']]

# Selecting a random subsample of 5 reviews
sample_reviews = df.sample(5, random_state=10)

# Applying preprocessing to each review
sample_reviews['processed_reviews'] = sample_reviews['reviews.text'].apply(preprocess)

# Analyzing sentiment for each preprocessed review
sentiment_analysis = []
for review in sample_reviews['processed_reviews']:
    sentiment_analysis.append(analyze_sentiment(review))

# Adding sentiment analysis results as separate columns
sample_reviews['polarity'] = [analysis['polarity'] for analysis in sentiment_analysis]
sample_reviews['sentiment'] = [analysis['sentiment'] for analysis in sentiment_analysis]
sample_reviews['label'] = [analysis['label'] for analysis in sentiment_analysis]

# Printing the resulting DataFrame with desired columns
print("\n----------Sentiment Analysis Results----------")
print(sample_reviews[['reviews.text', 'polarity', 'sentiment', 'label']])


# Loading the spaCy model with word vectors
nlp = spacy.load("en_core_web_md")

# Defining the two reviews to compare
my_review_of_choice_1 = df['reviews.text'][37]
my_review_of_choice_2 = df['reviews.text'][3070]

# Preprocessing the reviews using spaCy
review1_doc = nlp(my_review_of_choice_1)
review2_doc = nlp(my_review_of_choice_2)

# Computing the similarity score between the two reviews
similarity_score = review1_doc.similarity(review2_doc)

# Printing the similarity score
print("\n----------Similarity Score----------")
print("Similarity Score:", similarity_score)
