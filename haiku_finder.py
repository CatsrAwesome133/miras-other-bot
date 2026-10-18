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
    counter = 0
    syllables = 0
    temp = ""
    bar = []

    for word in words:
        counter += 1
        if any(c.isalpha() for c in word):
            temp = "".join([char for char in word if char.isalpha()])
            syllables += get_syllables(temp)
            if syllables in [5, 12, 17]:
                bar.append(counter)

    if syllables == 17:
        print("Yep")
        return True
    else: 
        print("Nop")
        return False


text = "HEllo!"

haiku_phrase("and today i had a cake")
haiku_phrase("An old silent pond, A frog jumps into the pond, Splash! Silence again.")
#print(get_syllables("".join([char for char in text if char.isalpha()])))