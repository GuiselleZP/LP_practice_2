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

class ImportantSets():
    def __init__(self, grammar):
        self.__grammar = self.__get_grammar(grammar)
        self.__dict_of_the_first = dict()
        self.__dict_of_the_following = dict()
        self.__prediction_dict = dict()
        self.__get_dict_of_the_first()
        self.__get_dict_of_the_following()
        self.__get_prediction_dict()

    def __get_grammar(self, grammar):
        grammar_dict = dict()
        for line in grammar:
            line = line.strip()
            line = line.split("\t->\t")
            key = line[0]
            rules = tuple(line[1].split(' | '))
            
            if grammar_dict.get(key) is None:
                grammar_dict[key] = list()

            grammar_dict[key].append(rules)
        return grammar_dict

    def __is_a_non_terminal(self, symbol):
        if re.match("(\'.*\'.*)", symbol) is None:
            return True
        else:
            return False
        
    def __call_first_set_non_terminal(self, symbol):
        if symbol not in self.__dict_of_the_first:
            set_first = set()
            for rules_tupl in self.__grammar[symbol]:
                for rule in rules_tupl:
                    aux = self.__get_set_of_the_first(rule)
                    set_first = aux | set_first
            self.__dict_of_the_first[symbol] = set_first
        return self.__dict_of_the_first[symbol]


    def __get_set_of_the_first(self, rule):
        empty_symbol = False
        set_first = set()
        aux_set = set()
        aux = rule.split(' ', 1)
        symbol = aux[0]

        if self.__is_a_non_terminal(symbol):
            aux_set = self.__call_first_set_non_terminal(symbol)
            if "''" in aux_set:
                empty_symbol = True
                temp_set = aux_set
                aux_set = set()
                aux_set = aux_set | temp_set
                aux_set.discard("''")
        else:
            if "''" == symbol:
                aux_set.add("''")              
            else:
                aux_set.add(symbol)
        set_first = set_first | aux_set

        if len(aux) == 2 and empty_symbol:
            leftover = aux[1]
            aux_set = self.__get_set_of_the_first(leftover)
            set_first = set_first | aux_set
        return set_first
                   
                    
    def __get_dict_of_the_first(self):
        for key in self.__grammar:
            if key not in self.__dict_of_the_first:
                  self.__call_first_set_non_terminal(key)

    def __get_set_of_the_following(self, symbol):
        pass
       
    def __get_dict_of_the_following(self):
        pass

    def __get_prediction_dict(self):
        pass
    def get_dict_of_grammar(self):
        return self.__grammar

    def get_dict_of_the_first(self):
        return self.__dict_of_the_first

    def get_dict_of_the_following(self):
        pass

    def get_prediction_dict(self):
        pass


def main():
    # cls()
    with open(GRAMAR_FL, 'r') as fl:
        grammar = fl.readlines()
        sets = ImportantSets(grammar)
        print(sets.get_dict_of_grammar())
        print(sets.get_dict_of_the_first())

if __name__ == '__main__':
    main()
