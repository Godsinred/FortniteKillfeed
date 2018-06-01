import nltk
import difflib

class Similarity:
    """
    Class responsible for checking words read from the screen which aren't readable and converting the words into
    readable phrases

    """
    def __init__(self):
        # the possible ways to die and the length of the phrase
        self.ways = {
            "eliminated" : 10,
            "shotgunned" : 10,
            "sniped" : 6,
            "bludgeoned" : 10,
            "\'sploded" : 8,
            "checked out early" : 17,
            "played themselves" : 17,
            "was lost in the storm" : 21,
            "didn\'t stick the landing" : 24,
            "is literally on fire" : 20,
            "took the L" : 10,
            "went out with a BANG" : 20
        }

    def check(self, line):
        """
        Checks to see if any of the words in the line are possible the self.ways to die
        :param line: the line that we get from google fiber to be compared
        :return: the correct line if any else the same line
        """

        if line == None:
            return line

        # check if it is a valid sentence
        words = line.split(' ')
        if len(words) < 3:
            return line

        for way in self.ways:
            if ((len(line)-self.ways[way]) > 2): # check if the line is shorter than ways
                for i in range(0, (len(line)-self.ways[way])):
                    seq = difflib.SequenceMatcher(None, way, line[i:(self.ways[way]+i)])
                    if (nltk.edit_distance(way, line[i:(self.ways[way]+i)]) <= 1) or (seq.ratio() >= 0.85):
                        print("YAY!!! we used found a correction. {} => {}".format(line[i:(self.ways[way]+i)], way))
                        index = len(line[:(self.ways[way]+i)].split(' ')) - len(way.split(' '))
                        return self.recreate_sentence(line, way, index)

        return line

    def recreate_sentence(self, line, way, index):
        """
        Recreates the sentence from line and way with the index of where the way should be
        :param line: the line to be fixed
        :param way: the correct way that it should be
        :param index: the place where the error was found
        :return: the correct sentence
        """
        sentence = ''
        words = line.split(' ')
        num_ways = len(way.split(' '))
        count = len(words)
        # list comprehension
        # indexes = [i + index for i in range(num_ways)]

        i = 0
        while i < count:
            if i == index:
                sentence += way + ' '
                i += num_ways

            else:
                sentence += words[i] + ' '
                i += 1

        return sentence.strip()

def main():
    """
    used for testing the similarity class

    :return:
    """
    line = "Manduin Wyrnn bludgeomed Cupidie"
    test = Similarity()
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")
    line = "brian shotaunned andrew"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")
    line = "jonny snlped izzy"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")
    line = "spring bludgeomed michael"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")
    line = "carlos sploded andrew"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    line = "sheng chedked out early"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    line = "alice plgyed themselves"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    line = "mauricio was l0st in the storm"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    line = "chris didn't stlck the landing"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    line = "thy is literaily on fire"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    line = "andrew took the I"
    new_line = test.check(line)
    print(line + "\nis now : " + new_line + "\n")

    print(nltk.edit_distance("shotgunned", "shotaunned"))
    a = 'shotgunned'
    b = 'shotaunned'

    seq = difflib.SequenceMatcher(None, a, b)
    d = seq.ratio()*100
    print(d)


if __name__ == "__main__":
    main()
