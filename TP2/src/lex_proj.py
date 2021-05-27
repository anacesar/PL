import sys
import ply.lex as lex

tokens = ['TERMINATOR','ID','NUM']

reservadas = {"int" : "INT",
              "STARTDECL" : "STARTDECL",
              "ENDDECL" : "ENDDECL",
              "STARTBODY" : "STARTBODY",
              "ENDBODY" : "ENDBODY",
              "or" : "OR",
              "and" : "AND",
              "not" : "NOT",
              "if" : "IF",
              "repeat" : "REPEAT",
              "until" : "UNTIL",
              "print" : "PRINT",
              "read" : "READ"
              }
tokens = tokens + list(reservadas.values())

literals = ['(',')',',','=','>','<','+', '*', '-','/','{', '}', '!','[',']']

t_STARTDECL = r'STARTDECL'
t_ENDDECL = r'ENDDECL'
t_STARTBODY = r'STARTBODY'
t_ENDBODY = r'ENDBODY'
t_INT = r'int'
t_TERMINATOR = r';'
t_OR = r'or'
t_AND = r'and'
t_NOT = r'not'
t_NUM = r'\d+' 
t_IF = r'if'
t_REPEAT = r'repeat'
t_UNTIL = r'until'
t_PRINT = r'print'
t_READ = r'read'
t_ignore = " \t\n\r"


def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    if t.value in reservadas:
        t.type = reservadas [t.value ]
    return t

def t_error(t):
    # print("Caráter ilegal: ", t.value[0])
    t.lexer.skip(1)
    return t

#Build the lexer
lexer = lex.lex()

# Reading input
for linha in sys.stdin:
    lexer.input(linha)
    for tok in lexer:
        print(tok)



