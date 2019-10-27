from os import system, name


def cls():
    # for windows
    if name == 'nt':
        system('cls')
    # for mac and linux (os.name = 'posix')
    else:
        system('clear')


class Rule():
    def __init__(self, rule):
        self.__rule = rule
        self.__split_rule = rule.split(' ')
        self.__len = len(self.__split_rule)

    def get_symbol(self, index):
        symbol = None
        if index < self.__len:
            symbol = self.__split_rule[index]
        return symbol

    def get_first(self):
        return self.__split_rule[0]

    def get_second(self, symbol):
        second = None
        for index in range(self.__len):
            if self.__split_rule[index] == symbol:
                index += 1
                if index < self.__len:
                    second = self.__split_rule[index]
        return second


class ImportantSets():
    def __init__(self, grammar):
        self.__grammar = self.__get_grammar()
        self.__set_of_the_firsts = set()
        self.__set_of_the_seconds = set()
        self.__prediction_set = set()

    def __get_grammar(grammar):
        grammar_dict = dict()
        for line in grammar:
            line = line.strip()
            line = line.split("\t->\t")
            key = line[0]
            rules = tuple(line[1].split(" | "))

            if grammar_dict.get(key) is None:
                grammar_dict[key] = list()

            grammar_dict[key].append(rules)
        return grammar_dict

    def __get_set_of_the_first():
        pass


def main():
    cls()
    test = Rule("'a' B 'c'")
    q = test.get_symbol(1)
    print(q)
    q = test.get_first()
    print(q)
    q = test.get_second('B')
    print(q)


if __name__ == '__main__':
    main()
