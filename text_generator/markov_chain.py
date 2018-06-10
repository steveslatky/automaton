#!/user/bin/python3

# Author Stephen Slatky
# A simple text generator using a markov chain.
# It will take in a text source and output works based
# on the source.
from random import randint


class words_def:

    # TODO Possible improvement, track type of word
    def __init__(self, num=1):
        self.num_seen = num


class chain:

    def __init__(self):
        self.alpha = dict()  # Alphabet (or known as dictionary)

    def add_to_alpha(self, cur_word, next_word):
        if next_word is not None:
            if cur_word not in self.alpha:
                self.alpha[cur_word] = {next_word: words_def()}
            else:
                if next_word in self.alpha[cur_word]:
                    self.alpha[cur_word][next_word].num_seen += 1
                else:
                    self.alpha[cur_word][next_word] = words_def()

    def read_source(self, file):
        with open(file, "r") as f:
            for line in f:
                # TODO Fix not taking in punctuation
                word_list = line.strip("\n").strip(".").strip("!").strip("?").strip(",").split(" ")
                for e, word in enumerate(word_list):
                    try:
                        self.add_to_alpha(word.lower(), word_list[e + 1].lower())
                    except IndexError:
                        pass

    def create_song(self, line_len=8, song_len=60):
        line_count = 0
        song = []
        for line_count in range(song_len):
            words_in_line = 0
            word = None
            line = []
            for words_in_line in range(line_len):
                # Pick random word if start of line
                if word is None:
                    word = list(self.alpha.keys())[randint(0, len(self.alpha) - 1)]
                else:
                    # get strongest link from word
                    try:
                        next_words_list = self.alpha[word]
                        word = pick_word(next_words_list)
                    except KeyError:
                        break
                line.append(word)
            song.append(line)
        write_song(song)


# TODO Find avg line length
# Or maybe this can be done with syllables? Maybe there is a way to get syllables based on spelling?

# Takes in a list of lines where each line
# has a list of words in them
def write_song(song):
    with open("./songs/1.txt", 'w') as f:
        for line in song:
            if line is not None:
                f.write(" ".join(line))
                f.write("\n")


def pick_word(next_word_list):
    combo_list = []
    for word in next_word_list:
        combo_list.append((next_word_list[word].num_seen, word))
    combo_list = sorted(combo_list)
    return combo_list[len(combo_list) - 1][1]


def main():
    generator = chain()
    for i in range(1, 8):
        generator.read_source("./sources/kanye/" + str(i) + ".txt")
    generator.create_song()


if __name__ == '__main__':
    main()
