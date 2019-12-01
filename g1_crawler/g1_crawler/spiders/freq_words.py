import nltk
from nltk.corpus import stopwords
import string

def freq_words(tokens):
    try:
        sr = stopwords.words('portuguese')
    except:
        nltk.download('stopwords')

    clean_tokens = tokens[:]
    
    # for token in tokens:
    #     if token in stopwords.words('portuguese'):
    #         clean_tokens.remove(token)
    # Find stopwords and remove them
    for stopword in stopwords.words('portuguese'):
        if stopword in clean_tokens:
            clean_tokens.remove(stopword)
    
    freq = nltk.FreqDist(clean_tokens)
    for key, val in freq.items():
        if val > 3:        
            print(str(key) + ':' + str(val))
    freq.plot(20, cumulative=False)
    freq.plot() 
