#!/user/bin/python3

# Author Stephen Slatky
# A simple text generator using a markov chain.
# It will take in a text source and output works based
# on the source.
from os import listdir
from random import randint, random


# import hyphen
# TODO Finish improting songs with Chorus/Verse

class structure_def:

    def __init__(self, length=0, times_seen=1):
        self.length = length
        self.times_seen = times_seen

class words_def:

    # TODO Possible improvement, track type of word (Adj, Noun, Adv, etc)
    def __init__(self, num=1):
        self.num_seen = num


class structure_chain:

    def __init__(self):
        self.song_struct = dict()

    # Input: Source directory
    def read_source(self, source):
        num_songs = len(listdir(source)) + 1
        for i in range(1, num_songs):
            self._parse_sources(source + str(i) + ".txt")
        self._normalize(num_songs)

    def _parse_sources(self, source):
        last_struct_type = None
        with open(source, 'r') as f:
            for line in f:
                if line[0] is "[":
                    last_struct_type = line[1].lower()
                    if line[1].lower() not in self.song_struct:
                        # Use first letter to determine Chorus or verse.
                        self.song_struct[line[1].lower()] = structure_def()
                    else:
                        self.song_struct[line[1].lower()].times_seen += 1
                else:
                    if last_struct_type is not None:
                        self.song_struct[last_struct_type].length += 1

    # Gets the Average per song of length of type
    def _normalize(self, num_songs):
        for item in self.song_struct:
            self.song_struct[item].length = round(self.song_struct[item].length / self.song_struct[item].times_seen)
            self.song_struct[item].times_seen = round(self.song_struct[item].times_seen / num_songs)


class song_chain:

    def __init__(self):
        self.struct = None
        self.alpha = dict()  # Alphabet (or known as dictionary)
        # self.h_en = hyphen.Hyphenator('en_US')

    def add_to_alpha(self, cur_word, next_word):
        # print(self.h_en.syllables(cur_word))
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

    def read_source(self, source):
        self.struct = structure_chain()
        self.struct.read_source(source)
        for i in range(1, len(listdir(source)) + 1):
            self._parse_source(source + str(i) + ".txt")

    def _parse_source(self, file):
        with open(file, "r") as f:
            for line in f:
                # Ignore the Chours and Verse tags
                if line[0] is not "[":
                    word_list = line.strip("\n").strip(".").strip("!").strip("?").strip(",").split(" ")
                    for e, word in enumerate(word_list):
                        try:
                            self.add_to_alpha(word.lower(), word_list[e + 1].lower())
                        except IndexError:
                            pass

    def create_chorus(self, line_len, song_len):
        song = []
        song.append(["[Chorus]"])
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
                    except KeyError:
                        break
                line.append(word)
            song.append(line)

            while randint(0, 10) >= 9:
                song.append(line)

        return list(song)


    def create_song(self, line_len=8, song_len=60):
        song = []
        struct_count = 0

        chorus = self.create_chorus(line_len, self.struct.song_struct["c"].length)

        isChrous = self.chorus_dice_roll()
        if isChrous:
            struct_count = self.struct.song_struct["v"].length
            for line in chorus:
                song.append(line)
            song.append(["[Verse]"])
        else:
            song.append(["[Verse]"])

        for line_count in range(song_len):

            # Alternate between chorus and Verse
            if struct_count <= line_count:
                struct_count += self.struct.song_struct["v"].length
                for line in chorus:
                    song.append(line)
                song.append(["[Verse]"])

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
                    except KeyError:
                        break
                line.append(word)
            song.append(line)
            # 1/10 times it will duplicate a line to make a chorus
            # while randint(0, 10) is 10:
            #     song.append(line)
        write_song(song)


    # TODO Fix for more struct entries. Only works for verse chrous stuct at the moment
    def chorus_dice_roll(self):
        total = sum(list(self.struct.song_struct[key].times_seen for key in self.struct.song_struct))
        combo_list = list((self.struct.song_struct[key].times_seen/total, key) for key in self.struct.song_struct)
        dice = random()
        if dice <= combo_list[0][0]: return False
        else: return True



# TODO Find avg line length
# TODO Or maybe this can be done with syllables? Maybe there is a way to get syllables based on spelling?

# Takes in a list of lines where each line
# has a list of words in them
def write_song(song):
    song_num = len(listdir("./songs")) + 1
    with open("./songs/" + str(song_num) + ".txt", 'w') as f:
        description = "==========================================================\n" \
                      "Version 5: Putting together a structure to the song \n" \
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
    generator = song_chain()



    generator.read_source(source)
    generator.create_song()


if __name__ == '__main__':
    main()
