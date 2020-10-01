import sys
from my_lexer import tokenize_file


class Node:
    def __init__(self, left, right, name):
        self.left = left
        self.right = right
        self.name = name


class Parser:
    def __init__(self, token_list_, pos_):
        self.token_list = token_list_
        self.pos = pos_

    def accept(self, token_type) -> bool:
        if self.token_list[self.pos].type == token_type:
            self.pos += 1
            return True
        return False

    def expect(self, token_type) -> bool:
        if self.token_list[self.pos].type == token_type:
            self.pos += 1
            return True
        template = "Unexpected character {0} at line {1} on position {2} instead of {3}"
        print(template.format(
            self.token_list[self.pos].type,
            self.token_list[self.pos].lineno,
            self.token_list[self.pos].lexpos,
            token_type
        ))
        return False

    def lit(self) -> Node:
        if self.accept('OPENBR'):
            r = self.disj()
            if self.expect('CLOSEBR'):
                return r
            return None
        l = self.token_list[self.pos]
        self.pos += 1
        if l.type != 'LITERAL':
            return None
        return Node(None, None, l.value)

    def disj(self) -> Node:
        l = self.conj()
        if self.accept('DISJ'):
            r = self.disj()
            if r == None:
                return None
            return Node(l, r, "or")
        return l

    def conj(self) -> Node:
        l = self.lit()
        if self.accept('CONJ'):
            r = self.conj()
            if r == None:
                return None
            return Node(l, r, "and")
        return l

    def corkscrew(self):
        try:
            l = self.token_list[self.pos]
            self.pos += 1
            if l.type == 'LITERAL':
                if self.accept('OPERATOR'):
                    r = self.disj()
                    if r == None:
                        return None, -1
                    if self.expect('DOT'):
                        return Node(Node(None, None, l.value), r, 'def'), self.pos
                    return None, -1
                if self.expect('DOT'):
                    return Node(None, None, l.value), self.pos
            return None, -1
        except IndexError:
            return None, -1

    def error(self, mes: str):
        print(mes)


def lexer(s):
    for c in s:
        if c == " ":
            continue
        yield c
    while True:
        yield '\0'


def pr(node) -> str:
    a = "("
    if node.left != None:
        a += pr(node.left)
    a += " " + node.name + " "
    if node.right != None:
        a += pr(node.right)
    a += ')'
    return a


lex_error_str = "Failed to lex"
parse_error_str = "Failed to parse"
correct_program_str = "Correct program"
open_file_error_str = "Failed to open {0}"


def parse_file(token_list) -> bool:
    if (len(token_list) == 0):
        print(correct_program_str)
        return True
    pos = 0
    while pos < len(token_list):
        p = Parser(token_list, pos)
        tree, pos = p.corkscrew()
        if tree == None:
            print(parse_error_str)
            return False
    print(correct_program_str)
    return True


def check_file(filename: str) -> bool:
    open_file_error, lexer_error, token_list = tokenize_file(filename)
    if (open_file_error):
        print(open_file_error_str.format(filename))
        return False
    if (lexer_error):
        print(lex_error_str)
        return False
    return parse_file(token_list)


if __name__ == "__main__":
    check_file(sys.argv[1])
