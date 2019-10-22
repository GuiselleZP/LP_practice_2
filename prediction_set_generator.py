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

def set_of_first(grammar_dic, first_dict, key):
    if key in first_dict:
        return
    else:
        rule_list = grammar_dic[key]
        first_set = set()
        for rules_tuple in rule_list:
            for rule in rules_tuple:
                split_rule = rule.split(' ')
                first = split_rule[0]
                if re.match("(^\'.*\'.*)", first) is None:
                    temp_set = set_of_first(grammar_dic, first_dict, first)
                    temp_set.discard(' ')
                    first_set = first_set | temp_set
                else:
                    first_set.add(first)
        first_dict[key] = first_set
        print(first_dict)
        return first_set


def main():
    cls()
    grammar_dic = get_grammar()

    first_dict = dict()
    for key in grammar_dic:
        set_of_first(grammar_dic, first_dict, key)
    

if __name__ == '__main__':
    main()
