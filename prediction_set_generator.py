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

def set_of_first(grammar_dic):
    first_dict = dict()
    for key, rule_list in grammar_dic.items():
        first_set = set()
        for rules_tuple in rule_list:
            for rule in rules_tuple:
                split_rule = rule.split(' ', 1)
                first = split_rule[0]
                first_set.add(first)
        first_dict[key] = first_set
    
    for key, value in first_dict.items():
        for first in value:
            if re.match("(^\'.*\'.*|^\".*\".*)", first) is None:




def main():
    cls()
    grammar_dic = get_grammar()
    set_of_first(grammar_dic)
    

if __name__ == '__main__':
    main()
