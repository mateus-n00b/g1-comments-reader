import nltk
from nltk.corpus import stopwords
from string import punctuation

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
    _stopwords = set(stopwords.words('portuguese') + list(punctuation))
    for stopword in _stopwords:
        if stopword in clean_tokens:
            clean_tokens.remove(stopword)
    
    freq = nltk.FreqDist(clean_tokens)
    for key, val in freq.items():
        if val > 2:        
            print(str(key) + ':' + str(val))
    freq.plot(20, cumulative=False)
    freq.plot() 
