# from nltk.tokenize import sent_tokenize
from .aspect_keywords import ASPECT_KEYWORDS

import re

def sent_tokenize(text):
    return re.split(r'[.!?]+', text)

def extract_aspects(review):
    sentences = sent_tokenize(review)
    
    aspect_sentences = {aspect: [] for aspect in ASPECT_KEYWORDS}
    
    for sentence in sentences:
        for aspect, keywords in ASPECT_KEYWORDS.items():
            if any(word in sentence.lower() for word in keywords):
                aspect_sentences[aspect].append(sentence)
    
    return aspect_sentences