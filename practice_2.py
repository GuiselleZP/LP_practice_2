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
        print('gramatica creada')
        self.__dict_of_the_first = dict()
        self.__dict_of_the_following = dict()
        self.__prediction_sets_list = list()
        self.__get_dict_of_the_first()
        print('dic primeros creado')
        self.__get_dict_of_the_following()
        print('dic siguientes creado')
        self.__get_prediction_sets_list()
        print('lista conjuntos de pred creada')

    def __get_grammar(self, grammar):
        grammar_dict = dict()
        for line in grammar:
            line = line.strip()
            line = line.split("\t->\t")
            key = line[0]
            rule = line[1]

            if grammar_dict.get(key) is None:
                grammar_dict[key] = list()

            grammar_dict[key].append(rule)
        return grammar_dict

    def __is_a_non_terminal(self, symbol):
        if re.match("(\'.*\'.*)", symbol) is None:
            return True
        else:
            return False

    def __call_first_set_non_terminal(self, symbol):
        if symbol not in self.__dict_of_the_first:
            set_first = set()
            for rule in self.__grammar[symbol]:
                print('F:{}: -> :{}:'.format(symbol, rule))
                if symbol == rule[0]:
                    if "''" in set_first:
                        rule = rule[1:]
                        rule = rule.strip()
                    else:
                        continue
                aux = self.__get_set_of_the_first(rule)
                print('conjunto en call de', rule)
                print(aux)
                set_first = aux | set_first
            print('PRIMEROS DE', symbol)
            print(set_first)
            self.__dict_of_the_first[symbol] = set_first
        return self.__dict_of_the_first[symbol]

    def __get_set_of_the_first(self, rule):
        epsilon = False
        set_first = set()
        aux_set = set()
        aux = rule.split(' ', 1)
        symbol = aux[0]

        if self.__is_a_non_terminal(symbol):
            print('call secundaria para buscar primeros de', symbol)
            aux_set = self.__call_first_set_non_terminal(symbol)
            print('conjunto de:', symbol)
            print(aux_set)
            print('len:', len(rule))
            if "''" in aux_set and len(rule) > 1:
                epsilon = True
                temp_set = aux_set
                aux_set = set()
                aux_set = aux_set | temp_set
                aux_set.discard("''")
        else:
            if "''" == symbol:
                aux_set.add("''")
                print('epsilon')
            else:
                print('terminal')
                aux_set.add(symbol)
        set_first = set_first | aux_set

        if len(aux) == 2 and epsilon:
            print('tiene epsilon')
            leftover = aux[1]
            print('recursion desde first busca primeros de:{}:'.format(leftover))
            aux_set = self.__get_set_of_the_first(leftover)
            set_first = set_first | aux_set
        print('conjunto primeros de', rule)
        print(set_first)
        return set_first

    def __get_dict_of_the_first(self):
        for key in self.__grammar:
            if key not in self.__dict_of_the_first:
                self.__call_first_set_non_terminal(key)
        print('DICCIONARIO PRIMEROS')
        print(self.__dict_of_the_first)

    def __search_symbol(self, rule, symbol):
        result = None
        for index in range(len(rule)):
            if rule[index] == symbol:
                index += 1
                result = rule[index:]
                result = result.strip()
                break
        return result

    def __call_following_set_non_terminal(self, symbol):
        if symbol not in self.__dict_of_the_following:
            set_following = set()
            aux_set = set()
            if symbol == 'S':
                set_following.add("'$'")
            for key in self.__grammar:
                for rule in self.__grammar[key]:
                    print('S:{}: -> :{}:sym:{}:'.format(key, rule, symbol))
                    aux_set = self.__get_set_of_the_following(key, rule,
                                                              symbol)
                    set_following |= aux_set
                self.__dict_of_the_following[symbol] = set_following
            print('SIGUIENTES DE', symbol)
            print(set_following)
        return self.__dict_of_the_following[symbol]

    def __get_set_of_the_following(self, key, rule, symbol):
        leftover = self.__search_symbol(rule, symbol)
        set_following = set()
        if leftover is not None:
            epsilon = False
            aux_set = set()
            if len(leftover) > 0:
                print('hay sig:{}'.format(leftover))
                print('recursion desde sigiente')
                aux_set = self.__get_set_of_the_first(leftover)
                print('conjunto de lef:{}:'.format(leftover))
                print(aux_set)
                if "''" in aux_set:
                    epsilon = True
                    temp_set = aux_set
                    aux_set = set()
                    aux_set |= temp_set
                    aux_set.discard("''")
                set_following |= aux_set
            if len(leftover) == 0 or epsilon:
                print('lef:{}:epsilon:{}'.format(leftover, epsilon))
                print('llamada call desde sig')
                aux_set = self.__call_following_set_non_terminal(key)
                print('conjunto de', key)
                print(aux_set)
                set_following |= aux_set
        print('conjunto sig')
        print(set_following)
        return set_following

    def __get_dict_of_the_following(self):
        for key in self.__grammar:
            if key not in self.__dict_of_the_following:
                self.__call_following_set_non_terminal(key)
        print('DICCIONARIO SIGUIENTES')
        print(self.__dict_of_the_following)

    def __get_prediction_set(self, key, rule):
        print('llamando primeros de:{}:'.format(rule))
        prediction_set = self.__get_set_of_the_first(rule)
        print('primeros obtenidos')
        print(prediction_set)
        if "''" in prediction_set:
            temp_set = prediction_set
            prediction_set = set()
            prediction_set |= temp_set
            prediction_set.discard("''")
            print('llamado a siguientes de', key)
            prediction_set |= self.__dict_of_the_following[key]
        print('conjunto pred')
        print(prediction_set)
        return prediction_set

    def __get_prediction_sets_list(self):
        for key in self.__grammar:
            for rule in self.__grammar[key]:
                print('P:{}: -> :{}:'.format(key, rule))
                prediction_set = self.__get_prediction_set(key, rule)
                self.__prediction_sets_list.append(prediction_set)
        print('LISTA CONJUNTOS PREDICCION')
        print(self.__prediction_sets_list)

    def get_dict_of_grammar(self):
        return self.__grammar

    def get_dict_of_the_first(self):
        return self.__dict_of_the_first

    def get_dict_of_the_following(self):
        return self.__dict_of_the_following

    def get_prediction_sets_list(self):
        return self.__prediction_sets_list


def main():
    # cls()
    with open(GRAMAR_FL, 'r') as fl:
        grammar = fl.readlines()
        sets = ImportantSets(grammar)
        print(sets.get_dict_of_grammar())
        print(sets.get_dict_of_the_first())
        print(sets.get_dict_of_the_following())
        print(sets.get_prediction_sets_list())


if __name__ == '__main__':
    main()
