import re
from nltk.tokenize import word_tokenize
import pyphen

dic = pyphen.Pyphen(lang='en_GB')


def n_syllables(word: str) -> int:
    """
    returns the number of syllables in word (according to pyphen)
    """
    return len(dic.inserted(word).split('-'))


def clean_message(text: str) -> str:
    """
    return lowercase string stripped of trailing whitespaces and nonalphanumeric characters
    """
    return re.sub(r'[^\sa-zA-Z0-9]', '', text).lower().strip()


def hardly_know_em(text: str):
    """
    if message contains a funny word, return that word (the last word if multiple) if it has more than one syllable.
    Otherwise return None
    """
    words = [word.lower() for word in word_tokenize(text)]
    for word in reversed(words):
        word = word.lower().capitalize()

        if len(word) > 25:
            continue
        # I hardly know her!
        if word[-1:] == 'a' \
                or word[-2:] in ('er', 'or', 'ar', 're') \
                or word[-3:] == 'eur':
            if n_syllables(word) > 1:
                return f"{word}? I hardly know her!"

        # I hardly know him!
        elif word[-2:] == 'im':
            if n_syllables(word) > 1:
                return f"{word}? I hardly know him!"

        # I hardly know 'em!
        elif word[-2:] in ('um', 'em'):
            if n_syllables(word) > 1:
                return f"{word}? I hardly know 'em!"

        # return None if message isn't joke-able
        else:
            return None


def haiku_detection(text: str, haiku_form: tuple = (5, 7, 5)):
    """
    looks for haikus in text
    :param text: input text
    :param haiku_form: tuple of number of syllables in each line
    :return: None if non-haiku-able
    """
    # text = "Whitecaps on the bay A broken signboard banging In the April wind".split()

    words = [word.lower() for word in word_tokenize(text)]

    # make word:syllables dictionary
    syllables = {word: n_syllables(word) for word in words}

    tot_syllables = sum(syllables.values())

    # if not haiku-able
    if tot_syllables != sum(list(haiku_form)):
        # print(f"There are {tot_syllables} syllables : {syllables}")
        return None

    # if haiku-able
    else:
        lines = [[] for _ in range(len(haiku_form))]
        count, line = 0, 0
        # check if words can be put into lines
        for word in words:
            count += syllables[word]
            if count > haiku_form[line]:
                # can't format as haiku
                # print(f"Not possible to split word at syllable boundary: {word}, {syllables}")
                return None
            lines[line].append(word)
            if count == haiku_form[line]:
                line += 1
                count = 0

    # validate the haiku
    for i, line in enumerate(haiku_form):
        sum_line = sum(syllables[word] for word in lines[i])
        if sum_line > line:
            raise SyntaxError(f"Too many syllables in line {i}. Got {sum_line}, want {line}")
        elif sum_line < line:
            raise SyntaxError(f"Not enough syllables in line {i}. Got {sum_line}, want {line}")

    return "\n".join(" ".join(line) for line in lines)


def boy_and_lavagirl(text: str):
    """
    Looks for the word before 'boy' in text and returns "____ boy and lava girl"
    returns None if 'boy' not in text.
    Takes last instance if many instances

    eg: boy_and_lavagirl("Spotted a fit boy in the chippy")
       > 'fit boy and lava girl'
    """
    boy_adj = re.findall(r'([A-Za-z]+)\sboy', text)

    if len(boy_adj) > 0:
        output = boy_adj[-1] + " boy and lava girl"
    else:
        output = None

    return output
