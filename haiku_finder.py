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

    for i in range(len(words)):
        words[i] = words[i].replace("\n", "")

    for word in words:
        counter += 1

        if any(c.isalpha() for c in word):
            try:
                temp = "".join([c for c in word if c.isalpha()])
                syllables += get_syllables(temp)
                if syllables in [5, 12, 17]:
                    bar.append(counter)
            except TypeError:
                pass

    if len(bar) == 3:
        print("Yep")
        lines = []
        lines.append("".join([w+" " for w in words[:bar[0]]]))
        lines.append("".join([w+" " for w in words[bar[0]:bar[1]]]))
        lines.append("".join([w+" " for w in words[bar[1]:]]))
        return True, "".join([line+"\n" for line in lines])
    else: 
        print("Nop")
        return False, ""

if __name__ == '__main__':
    text = "HEllo!"

    print(haiku_phrase("and today i had a cake"))
    print(haiku_phrase("An old silent pond, \nA frog jumps into the pond, \nSplash! Silence again."))
    print(haiku_phrase("An old silent, ponder frog jumps into the pond, Splash! Silence again."))
    #print(get_syllables("".join([char for char in text if char.isalpha()])))