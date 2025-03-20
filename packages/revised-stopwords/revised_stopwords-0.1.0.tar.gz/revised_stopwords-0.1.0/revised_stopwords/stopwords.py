import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

def get_revised_stopwords():
    """Returns an optimized stopword list for sentiment analysis."""
    
    original_stopwords = set(stopwords.words('english'))

    #Sentiment-bearing words that should NOT be removed
    retained_stopwords = {
        "couldn", "couldn't", "wouldn", "wouldn't", "wasn", "wasn't", "mightn", "mightn't", "weren", "weren't",
        "doesn", "doesn't", "hadn", "hadn't", "ain", "shouldn", "shouldn't", "needn", "needn't",
        "didn", "didn't", "don", "don't", "very", "more", "hasn", "hasn't", "mustn", "mustn't",
        "isn", "isn't", "won", "won't", "aren", "aren't", "haven", "haven't", "shan", "shan't",
        "not", "no", "nor", "off", "against", "most"
    }

    #Remove only words that shouldn't be removed for sentiment
    revised_stopwords = original_stopwords - retained_stopwords
    
    return revised_stopwords

#Example Usage
if __name__ == "__main__":
    print(get_revised_stopwords())
