import re
from nltk.tokenize import word_tokenize
import pyphen
dic = pyphen.Pyphen(lang='en_GB')


# only use words with more than syllables or it makes no sense
# "Car? I hardly know her!"
# not so funny is it?
def more_than_one_syllable(word):
    return len(dic.inserted(word).split('-')) > 1


def hardly_know_em(text: str):
    """
    if message contains a funny word, return that word (the last word if multiple) if it has more than one syllable.
    Otherwise return None
    """

    words = [word.lower() for word in word_tokenize(text)]
    for word in reversed(words):
        if len(word) > 25:
            continue
        # I hardly know her!
        if word[-1:] == 'a' \
                or word[-2:] in ('er', 'or', 'ar', 're') \
                or word[-3:] == 'eur':
            if more_than_one_syllable(word):
                return f"{word.lower()}? I barely know her!"

        # I hardly know him!
        if word[-2:] in ('im', 'em', 'um'):
            if more_than_one_syllable(word):
                return f"{word.lower()}? I barely know him!"

    # return None if message isn't jokeable
    return None


def clean_message(text: str):
    """
    return lowercase string stripped of trailing whitespaces and nonalphanumeric characters
    """
    return re.sub(r'[^\sa-zA-Z0-9]', '', text).lower().strip()
