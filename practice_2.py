import re
import sys
from os import system, name
from pathlib import Path

LOCAL_FOLDER = Path(__file__).parent
TOKENS_FL = LOCAL_FOLDER / 'data/tokens.txt'
RESERVED_WORDS_FL = LOCAL_FOLDER / 'data/reserved_words.txt'
REGULAR_EXPRESIONS_FL = LOCAL_FOLDER / 'data/regular_expresions.txt'

def cls():
    # for windows
    if name == 'nt':
        system('cls')
    #for mac and linux (os.name = 'posix')
    else:
        system('clear')

def load_data():
    global tk_dic, re_dic, rw_list
    with open(TOKENS_FL, 'r') as fl:
        tk_dic = dict([[x.strip() for x in line.split('\t')] for line in fl])
    with open(REGULAR_EXPRESIONS_FL, 'r') as fl:
        re_dic = dict([[x.strip() for x in line.split('\t')] for line in fl])
    with open(RESERVED_WORDS_FL, 'r') as fl:
        rw_list = set([x.strip() for x in fl.readlines()])


def lexical_error(position):
    with open(ANALYZED_FL, 'a') as fl:
        output = '>>> Error lexico(linea: {}, posicion: {})\n'\
                .format(position[0], position[1])
        fl.write(output + '\n')
        print(output)
        sys.exit()

def register_token(token, position):
    with open(ANALYZED_FL, 'a') as fl:
        if type(token[0]) is int:
            if token[1] in tk_dic:
                tk = tk_dic[token[1]]
            else:
                tk = token[1]
            output = "<{}, {}, {}>".format(tk, position[0], position[1])
        else:
            output = "<{}, {}, {}, {}>".format(token[0], token[1],position[0],\
                                        position[1])
        fl.write(output + '\n');
        print(output)

def analyze(string, position):
    identifier = re.compile(re_dic['id'], re.I)
    number = re.compile(re_dic['tk_num'])
    array = re.compile(re_dic['tk_cadena'])
    operators = re.compile(re_dic['operators'])
    ignore = re.compile(re_dic['ignore'])
    token = []
    separator = 0

    if array.match(string) is not None:
        temp = array.match(string)
        i = 0
        for char in string:
            separator += 1
            if char == string[0]:
                i += 1
                if i == 2:
                    break
        token.append('tk_cadena')
    elif identifier.match(string) is not None:
        temp = re.match(identifier, string)
        separator = temp.end()
        if string[:separator] in rw_list:
            token.append(0)
        else:
            token.append('id')
    elif number.match(string) is not None:
        temp = re.match(number, string)
        separator = temp.end()
        token.append('tk_num')
    elif operators.match(string) is not None:
        temp = operators.match(string)
        separator = temp.end()
        token.append(0)
    elif string[0] == '\t':
        position[1] += 4
        return analyze(string[1:], position)
    elif string[0] == ' ':
        position[1] += 1
        return analyze(string[1:], position)
    elif ignore.match(string) is not None:
        return
    else:
        return lexical_error(position)

    token.append(string[:separator])
    register_token(token, position)
    position[1] += separator
    return analyze(string[separator:], position)


def main():
    global ANALYZED_FL, LOCAL_FOLDER, ANALYZED_FL

    cls()
    name_file = input("Ingrese el nombre del archivo a analizar:\n")
    new_name = name_file.split('.')[0]
    new_name = new_name + '_alz.txt'
    
    INPUT_FL = LOCAL_FOLDER / 'test'/ name_file
    ANALYZED_FL = LOCAL_FOLDER / 'test' / new_name

    load_data()
    
    auxfl = open(ANALYZED_FL, 'w')
    auxfl.close()
    position = [1, 1]
    with open(INPUT_FL, 'r') as fl:
        for line in fl:
            position[1] = 1
            analyze(line, position)
            position[0] += 1

if __name__ == '__main__':
    main()
