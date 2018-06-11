#!/user/bin/python3

# Author Stephen Slatky
# A simple text generator using a markov chain.
# It will take in a text source and output works based
# on the source.
from os import listdir
from random import randint
import hyphen

class words_def:

    # TODO Possible improvement, track type of word
    def __init__(self, num=1):
        self.num_seen = num


class chain:

    def __init__(self):
        self.alpha = dict()  # Alphabet (or known as dictionary)
        self.h_en = hyphen.Hyphenator('en_US')

    def add_to_alpha(self, cur_word, next_word):
        print(self.h_en.syllables(cur_word))
        if next_word is not None:
            # Sanitize words
            cur_word = cur_word.strip(",").strip("\"")
            next_word = next_word.strip(",").strip("\"")

            # New Word
            if cur_word not in self.alpha:
                self.alpha[cur_word] = {next_word: words_def()}
            # Existing word
            else:
                if next_word in self.alpha[cur_word]:
                    self.alpha[cur_word][next_word].num_seen += 1
                else:
                    self.alpha[cur_word][next_word] = words_def()

    def read_source(self, file):
        with open(file, "r") as f:
            for line in f:
                word_list = line.strip("\n").strip(".").strip("!").strip("?").strip(",").split(" ")
                for e, word in enumerate(word_list):
                    try:
                        self.add_to_alpha(word.lower(), word_list[e + 1].lower())
                    except IndexError:
                        pass

    def create_song(self, line_len=8, song_len=60):
        song = []
        for line_count in range(song_len):
            word = None
            line = []
            for words_in_line in range(line_len):
                # Pick random word if start of line
                if word is None:
                    word = list(self.alpha.keys())[randint(0, len(self.alpha) - 1)]
                else:
                    try:
                        next_words_list = self.alpha[word]
                        word = pick_word(next_words_list)
                    except KeyError:  # TODO Fix what happens if you don't find connecting word
                        break
                line.append(word)
            song.append(line)
            # 1/10 times it will duplicate a line to make a chorus
            while randint(0, 10) is 10:
                song.append(line)

        # write_song(song)


# TODO Find avg line length
# TODO Or maybe this can be done with syllables? Maybe there is a way to get syllables based on spelling?

# Takes in a list of lines where each line
# has a list of words in them
def write_song(song):
    song_num = len(listdir("./songs")) + 1
    with open("./songs/" + str(song_num) + ".txt", 'w') as f:
        description = "==========================================================\n" \
                      "Version 5, Gonna try and get the count syllables\n" \
                      "\n" \
                      "==========================================================\n"
        f.write(description)
        for line in song:
            if line is not None:
                try:
                    f.write(" ".join(line) + "\n")
                # Debugging stuff
                except TypeError:
                    print("Failed to write line")
                    print(line)


def pick_word(next_word_list):
    # Create list of tuples of word and time seen, makes it easier to work with
    combo_list = [(next_word_list[word].num_seen, word) for word in next_word_list]
    combo_list = sorted(combo_list, reverse=True)

    # If the list is 1 word just return that word
    if len(combo_list) is 1:
        return combo_list[0][1]

    # Count total amount of times all words were seen and then
    # Roll the dice to see what word to pick
    total = 0
    for word in combo_list:
        total += word[0]
    dice_roll = randint(0, total - 1)

    count = 0
    # Get word based on probability that it showed up.
    # Confession: bad way to do this, but it works
    for word in combo_list:
        if count >= dice_roll:
            return word[1]
        else:
            count += word[0]
    # If all else fails for some reason just return the most used word
    return combo_list[0][1]


def main():
    source = "./sources/kanye/"
    generator = chain()
    for i in range(1, len(listdir(source)) + 1):
        generator.read_source(source + str(i) + ".txt")
    generator.create_song()


if __name__ == '__main__':
    main()
