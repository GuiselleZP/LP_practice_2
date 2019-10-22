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
    grammar_dic = {} 
    with open (GRAMAR_FL, 'r') as fl:
        for line in fl:
            line = line.strip()
            line = line.split('\t->\t')
            temp_key = line[0]
            temp_rules = tuple(line[1].split(' | '))

            if grammar_dic.get(temp_key) == None:
                grammar_dic[temp_key] = []
            
            grammar_dic[temp_key].append(temp_rules)
    return grammar_dic

def main():
    cls()
    grammar_dic = get_grammar()
    

if __name__ == '__main__':
    main()
