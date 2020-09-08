import re
from nltk.tokenize import word_tokenize
import pyphen
dic = pyphen.Pyphen(lang='en_GB')


def good_word(text: str):
    """
    if message contains a funny word, return that word (the last word if multiple) if it has more than one syllable.
    Otherwise return None
    """
    words = [word.lower() for word in word_tokenize(text)]
    for word in reversed(words):
        if len(word) > 25:
            continue
        if word[-1] == 'a' \
                or word[-2:] in ('er', 'or', 'ar', 're') \
                or word[-3:] == 'eur':
            # calculate number of syllables
            if len(dic.inserted(word).split('-')) > 1:
                return word.lower()
    return None


def clean_message(text: str):
    """
    return lowercase string stripped of trailing whitespaces and nonalphanumeric characters
    """
    return re.sub(r'[^\sa-zA-Z0-9]', '', text).lower().strip()
