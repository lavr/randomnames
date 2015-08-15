import random

class WordsFromFile(list):
    def __init__(self, filename):
        with open(filename) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                self.append(line.strip())

left = WordsFromFile(filename='data/docker-adjective.txt')
right = WordsFromFile(filename='data/wikidata-names.txt')


def get_random_name():
    r = random.SystemRandom()
    while 1:
        name = '%s_%s' % (r.choice(left), r.choice(right))
        if name == "boring_wozniak": # Steve Wozniak is not boring
            continue
        return name


if __name__ == '__main__':
    print(get_random_name())