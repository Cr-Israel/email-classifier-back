import nltk
import string
import re
import inflect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# lower case
def lower_case(text):
  text_lower = text.lower()
  return text_lower
  print(text_lower)

lower_case("Hello, World!")
# removing punctuation
def remove_punctuation(text):
  translator = str.maketrans('', '', string.punctuation)
  text_punctuation = text.translate(translator)
  return text_punctuation
  print(translator)
  print(text_punctuation)

remove_punctuation("Hello, World!")

# removing whitespace
def remove_whitespace(text):
  text_whitespace = " ".join(text.split())
  return text_whitespace
  print(text_whitespace)

remove_whitespace("Hello, World!")

#removing stopwords
def remove_stopwords(text):
  stop_words = set(stopwords.words('portuguese'))
  word_tokens = word_tokenize(text)
  filtered_sentence = [word for word in word_tokens if word.lower() not in stop_words]
  return filtered_sentence
  print(filtered_sentence)

remove_stopwords("Hello, World!")

stemmer = PorterStemmer()

# Stemming
def stem_words(text):
  word_tokens = word_tokenize(text)
  stems = [stemmer.stem(word) for word in word_tokens]
  return stems
  print(stems)

stem_words("Hello, World!")