import re
import sys
from os import system, name
from pathlib import Path

LOCAL_FOLDER = Path(__file__).parent
GRAMAR_FL = LOCAL_FOLDER / 'data/SR_grammar.txt'

def cls():
    # for windows
    if name == 'nt':
        system('cls')
    #for mac and linux (os.name = 'posix')
    else:
        system('clear')

def get_grammar():
    grammar_dic = dict() 
    with open (GRAMAR_FL, 'r') as fl:
        for line in fl:
            line = line.strip()
            line = line.split('\t->\t')
            temp_key = line[0]
            temp_rules = tuple(line[1].split(' | '))

            if grammar_dic.get(temp_key) is None:
                grammar_dic[temp_key] = []
            
            grammar_dic[temp_key].append(temp_rules)
    return grammar_dic

def get_set_of_first(key, grammar_dic, first_dic):
    if key not in first_dic:
        first_set = set()
        for rules_tup in grammar_dic[key]:
            for rule in rules_tup:
                split_rule = rule.split(' ')
                first = split_rule[0]
                if re.match("(^\'.*\'.*)", first) is None:
                    aux = get_set_of_first(first, grammar_dic, first_dic)
                    set_1 = aux[1]
                    if "''" in set_1:
                        first = split_rule[1]
                        aux = get_set_of_first(first, grammar_dic, first_dic)
                        set_2 = aux[1]
                        set_1 = set_1 | set_2
                        set_1.discard("''")
                    first_set = first_set | set_1
                else:
                    first_set.add(first)
        first_dic[key] = first_set
        return (first_dic, first_set)

def get_set_of_seconds(key, grammar_dic, seconds_dic):
    if key not in seconds_dic:
        seconds_set = set()

def get_first_dic(grammar_dic):
    first_dic = dict()
    for key in grammar_dic:
        if key not in first_dic:
            aux_dic = get_set_of_first(key, grammar_dic, first_dic)
            if aux_dic is None:
                break
            first_dic = aux_dic[0]
    return first_dic

def get_seconds_dic(grammar_dic):
    seconds_dic = dict()
    for key in grammar_dic:
        if key not in seconds_dic:
            aux_dic = get_set_of_seconds(key, grammar_dic, seconds_dic)
            if aux_dic is None:
                break
            seconds_dic = aux_dic[0]
        return seconds_dic

def main():
    cls()
    grammar_dic = get_grammar()
    first_dic = get_first_dic(grammar_dic)
    print (first_dic)
    

if __name__ == '__main__':
    main()
