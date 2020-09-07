from nltk.tokenize import word_tokenize
import pyphen
dic = pyphen.Pyphen(lang='en_GB')


# if message contains a funny word, return that word if it has more than one syllable. otherwise return None
def good_word(text: str):
    words = [word.lower() for word in word_tokenize(text)]
    for word in reversed(words):
        if len(word) > 25:
            pass
        if word[-1] == 'a' \
                or word[-2:] in ('er', 'or', 'ar', 're') \
                or word[-3:] == 'eur':
            # calculate number of syllables
            if len(dic.inserted(word).split('-')) > 1:
                return word.lower()
    return None
