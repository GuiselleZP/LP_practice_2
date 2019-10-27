import re
from os import system, name
from pathlib import Path

LOCAL_FOLDER = Path(__file__).parent
GRAMAR_FL = LOCAL_FOLDER / 'data/SR_grammar.txt'


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
        self.__grammar = self.__get_grammar(grammar)
        self.__dict_of_the_first = dict()
        self.__seconds_dict = dict()
        self.__prediction_dict = dict()
        self.__get_dict_of_the_first()
        self.__get_dict_of_the_seconds()
        self.__get_prediction_dict()

    def __get_grammar(self, grammar):
        grammar_dict = dict()
        for line in grammar:
            line = line.strip()
            line = line.split("\t->\t")
            key = line[0]
            rules = line[1].split(" | ")

            rules_list = list()
            for rule in rules:
                rule = Rule(rule)
                rules_list.append(rule)
            rules_tupl = tuple(rules_list)

            if grammar_dict.get(key) is None:
                grammar_dict[key] = list()

            grammar_dict[key].append(rules_tupl)
        return grammar_dict

    def __get_set_of_the_first(self, key):
        if key not in self.__dict_of_the_first:
            set_of_the_first = set()
            for rules_tupl in self.__grammar[key]:
                for rule in rules_tupl:
                    first = rule.get_first()
                    if re.match("(^\'.*\'.*)", first) is None:
                        aux_set_1 = self.__get_set_of_the_first(first)
                        if "''" in aux_set_1:
                            first = rule.get_symbol(1)
                            aux_set_2 = self.__get_set_of_the_first(first)
                            aux_set_1 = aux_set_1 | aux_set_2
                            aux_set_1.discard("''")
                        set_of_the_first = set_of_the_first | aux_set_1
                    else:
                        set_of_the_first.add(first)
            self.__dict_of_the_first[key] = set_of_the_first
            return set_of_the_first

    def __get_dict_of_the_first(self):
        for key in self.__grammar:
            if key not in self.__dict_of_the_first:
                self.__get_set_of_the_first(key)

    def __get_set_of_the_secods(self, key):
        pass

    def __get_dict_of_the_seconds(self):
        pass

    def __get_prediction_dict(self):
        pass

    def get_dict_of_the_first(self):
        return self.__dict_of_the_first

    def get_set_of_the_secods(self):
        pass

    def get_prediction_dict(self):
        pass


def main():
    cls()
    with open(GRAMAR_FL, 'r') as fl:
        grammar = fl.readlines()
        sets = ImportantSets(grammar)
        print(sets.get_dict_of_the_first())


if __name__ == '__main__':
    main()
