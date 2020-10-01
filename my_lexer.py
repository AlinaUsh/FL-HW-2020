import ply.lex as lex

tokens = [
             'LITERAL',
             'CONJ',
             'DISJ',
             'DOT',
             'OPERATOR',
             'OPENBR',
             'CLOSEBR'
         ]

t_LITERAL = r'[a-zA-Z_][a-zA-Z_0-9]*'

t_OPERATOR = r'\:\-'

t_CONJ = r'\,'

t_DOT = r'\.'

t_DISJ = r'\;'

t_OPENBR = r'\('

t_CLOSEBR = r'\)'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

template = 'Illegal character {0} at line {1} in position {2}'

def t_error(t):
    tokenize_file.error_fl = True
    print(template.format(t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)


def t_eof(t):
    return None


def tokenize_file(input_file_name: str):
    tokenize_file.error_fl = False
    tokens_list = []
    try:
        input_file = open(input_file_name)
    except:
        return True, False, None
    lexer = lex.lex()
    lexer.input(input_file.read())
    input_file.close()
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    return False, tokenize_file.error_fl, tokens_list
