import nltk
from nltk.corpus import cmudict


nltk.download('cmudict')
d = cmudict.dict()


# syllables - it's called haiku for a reason
def get_syllables(word):
    word = word.lower()
    if word in d:
        # Returns a list of phonemes for the first pronunciation variant
        phonemes = d[word][0]
        # Count phonemes that end with a digit (vowel stress markers)
        return len([ph for ph in phonemes if ph[-1].isdigit()])
    else:
        return None  # Word not in dictionary


def haiku_phrase(phrase):
    words = phrase.split(' ')
    print(words)

haiku_phrase("and today i had a cake")