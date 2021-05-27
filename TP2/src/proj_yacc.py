import ply.yacc as yacc

from lex_proj import tokens

def p_Language(p):
    "Language : Declarations Functionality"
    p[0] = p[1] + p[2]
    print("declarations: ",p[1])

def p_Declarations(p):
    "Declarations : STARTDECL BodyDecls ENDDECL"
    print("Body_Decls: ", p[2])


def p_Functionality(p):
    "Functionality : START Instructions END"

def p_Body_Decls_Body_Decl(p):
    "BodyDecls : BodyDecls BodyDecl"
    p[0] = p[1] + p[2]

def p_Body_Decls(p):
    "BodyDecls : BodyDecl"
    p[0] = p[1]

def p_Body_Decl(p):
    "BodyDecl : INT Def TERMINATOR"
    p[0] = p[1] + p[3]

def p_Body_Decl_Empty(p):
    "BodyDecl : "
    pass

def p_Def(p):
    "Def : Ids Enumerate"
    p[0] = p[1] + p[2]

def p_Ids_Id(p):
    "Ids : ID"
    p[0] = p[1]

def p_Ids_Num(p):
    "Ids : ID '[' NUM ']'"
    p[0] = p[2] #??

def p_Enumerate(p):
    "Enumerate : ',' Def"

def p_Enumerate_Empty(p):
    "Enumerate : "
    pass






def p_error(p):
    print('Syntax error!')


#Build the parser
parser = yacc.yacc()

#Read input and parse it by line
import sys

for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)

    if parser.success:
        print("Frase Válida reconhecida.",linha)
    else:
        print("Frase inválida. Corrija e tente de novo...")
