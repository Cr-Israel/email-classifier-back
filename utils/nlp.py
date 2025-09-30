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

stemmer = PorterStemmer()

def preprocess_text(text: str):
  # Colocar em minúsculas
  text = text.lower()

  # Remover pontuação
  text = text.translate(str.maketrans('', '', string.punctuation))

  # Remover espaços extras
  text = " ".join(text.split())

  # Tokenizar
  tokens = word_tokenize(text)

  # Remover stopwords (português)
  stop_words = set(stopwords.words('portuguese'))
  tokens = [word for word in tokens if word not in stop_words]

  # Stemming
  tokens = [stemmer.stem(word) for word in tokens]

  return tokens