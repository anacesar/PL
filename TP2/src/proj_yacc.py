import ply.yacc as yacc

from lex_proj import tokens
 


def p_Language(p):
    "Language : Declarations Functionality"
    p[0] = p[1] + p[2] 
    #print("language : declarations " ,p[1] + "funcionality : " + p[2])


def p_Declarations(p):
    "Declarations : STARTDECL BodyDecls ENDDECL"
    p[0] = p[2] 


def p_Functionality(p):
    "Functionality : STARTBODY Instructions ENDBODY"
    print(p.parser.table)
    p[0] = "\nstart\n" + p[2] + "stop\n"
    #print("fun ",p[0])


def p_Body_Decls(p):
    "BodyDecls : BodyDecls BodyDecl"
    p[0] = p[1] + p[2]

def p_Body_Decls_Body_Decl(p):
    "BodyDecls : "
    p[0] = ""

def p_Body_Decl_INT(p):
    "BodyDecl : INT DeclDef TERMINATOR"
    p[0] = p[2]
    #p[0] = "int " + p[2] + p[3] + "\n"
    #print("def " , p[2])

def p_DeclDef(p):
    "DeclDef : DeclIds Enumerate"
    p[0] = p[1] + p[2]

def p_DeclIds_ID(p):
    "DeclIds : ID"
    p.parser.table[p[1]] = ("int", p.parser.offset, 1, [0])
    p.parser.offset+=1
    p[0] = "pushi 0\n"

def p_DeclIds_Array(p):
    "DeclIds : ID '[' NUM ']'"
    size = int(p[3])
    p.parser.table[p[1]] = ("intArray", p.parser.offset, size, int[size])
    p.parser.offset+=size
    p[0] = "pushn " + p[3] + "\n"

def p_Enumerate(p):
    "Enumerate : ',' DeclDef"
    p[0] = p[2]
    #p[0] = ',' + p[2]

def p_Enumerate_Empty(p):
    "Enumerate : "
    p[0] = ""

def p_Ids_Int(p):
    "Ids : ID"
    p[0] = p[1]
    #p[0] = p[1]

def p_Ids_ArrayID(p):
    "Ids : ID '[' ID ']'"
    p[0] = p[1] + '[' + p[3] + ']'
    #print("array " , p[0])

def p_Ids_Array(p):
    "Ids : ID '[' NUM ']'"
    #p[0] = "pushn " + p[3] + "\n"
    p[0] = p[1] + '[' + p[3] + ']'
    #print("array " , p[0])


def p_Instructions(p):
    "Instructions : Instructions Instruction"
    p[0] = p[1] + p[2]

def p_Instructions_Instruction(p):
    "Instructions : """
    p[0] = ""

def p_Instruction_Decl(p):
    "Instruction : BodyDecl "
    p[0] = p[1] + "\n"

def p_Instruction_DeclArrayID(p):
    "Instruction : INT ID '[' ID ']' TERMINATOR"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] 
    print("array " , p[0])

def p_Instruction_Atr(p):
    "Instruction : Atr TERMINATOR"
    p[0] = p[1] + p[2] + "\n"
    #print("p2",p[1])

def p_Atr_ID(p):
    "Atr : ID '=' Exp"
    p[0] = p[1] + '=' + p[3]

def p_Atr_IDID(p):
    "Atr : ID '[' ID ']' '=' Exp"
    print("atr array ")
    p[0] = p[1] + '[' + p[3] + "] = " + p[6]

def p_Atr_IDNUM(p):
    "Atr : ID '[' NUM ']' '=' Exp"
    p[0] = p[1] + '[' + p[3] + "] = " + p[6]

def p_Instruction_Repeat(p):
    "Instruction : Repeat "
    p[0] = p[1] + "\n"

def p_Instruction_If(p):
    "Instruction : If"
    p[0] = p[1] + "\n"
    print("if: ", p[1])

def p_Instruction_Print(p):
    "Instruction : Print TERMINATOR"
    p[0] = p[1] + p[2] + "\n"

def p_Instruction_Read(p):
    "Instruction : Read TERMINATOR"
    p[0] = p[1] + p[2] + "\n"


def p_If(p):
    "If : IF '(' Cond ')' '{' Instructions '}' Else"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]

def p_Else(p):
    "Else : ELSE '{' Instructions '}'"
    p[0] = p[1] + p[2] + p[3] + p[4]

def p_ElseEmpty(p):
    "Else : "
    p[0] = ""

def p_Repeat(p):
    "Repeat : REPEAT '{' Instructions '}' UNTIL '(' Cond ')'"
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]
    #print("repeat {" + p[2] + "}until( " + p[6] + "}")
    #p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]

def p_Cond_Cond(p):
   "Cond : Cond OR Cond2"
   p[0] = p[1] + p[2] + p[3]

def p_Cond_Cond2(p):
    "Cond : Cond2"
    p[0] = p[1]
   
def p_Cond2(p):
    "Cond2 : Cond2 AND Cond3"
    p[0] = p[1] + " " + p[2] + " " + p[3]
    print("and p1 : " , p[1] , " p3 : " , p[3])

def p_Cond2_Cond3(p):
    "Cond2 : Cond3"
    p[0] = p[1]

def p_Cond3_Not(p):
    "Cond3 : NOT Cond" #change to cond -- right recursive ??? 
    p[0] = p[1] + p[2]

def p_Cond3_ExpR(p):
    "Cond3 : ExpRelacional"
    p[0] = p[1]

def p_Cond3(p):
    "Cond3 : Cond"
    p[0] = p[1] 

def p_Cond3_Empty(p):
    "Cond3 : "
    p[0] = ""

def p_ExpRelacional_Bigger(p):
    "ExpRelacional : Exp '>' Exp"
    p[0] = p[1] + p[2] + p[3]


def p_ExpRelacional_Lower(p):
    "ExpRelacional : Exp '<' Exp"
    p[0] = p[1] + p[2] + p[3]



def p_ExpRelacional_BiggerEqual(p):
    "ExpRelacional : Exp '>' '=' Exp"
    p[0] = p[1] + p[2] + p[3] + p[4]
    


def p_ExpRelacional_LowerEqual(p):
    "ExpRelacional : Exp '<' '=' Exp"
    p[0] = p[1] + p[2] + p[3] + p[4]



def p_ExpRelacional_Diff(p):
    "ExpRelacional : Exp '!' '=' Exp"
    p[0] = p[1] + p[2] + p[3] + p[4]



def p_ExpRelacional_Equal(p):
    "ExpRelacional : Exp '=' '=' Exp"
    p[0] = p[1] + p[2] + p[3] + p[4]


def p_ExpRelacional(p):
    "ExpRelacional : Exp"
    p[0] = p[1]

def p_ExpPlus(p):
    "Exp : Exp '+' Termo"
    print("exp plus")
    p[0] = p[1] + '+' + p[3]

def p_ExpMinus(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] + p[2] + p[3]

def p_ExpTermo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_TermoMul(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] + '*' +  p[3]

def p_TermoDiv(p):
    "Termo : Termo '/' Fator"
    p[0] = p[1] + p[2] + p[3]

def p_TermoFator(p):
    "Termo : Fator"
    p[0] = p[1]

def p_FatorExp(p):
    "Fator : '(' Exp ')' "
    p[0] = p[2]


def p_FatorNum(p):
    "Fator : NUM "
    p[0] = p[1]

def p_FatorID(p):
    "Fator : ID "
    p[0] = p[1]


def p_PrintExp(p):
    "Print : PRINT '(' NUM ')' "
    p[0] = "pushi " + p[3] +"\nwritei\n" 
    #p[0] = p[1] + p[2] + p [3] + p[4]

def p_PrintDef(p):
    "Print : PRINT '(' Ids ')' "
    (t,o,s,v) = p.parser.table[p[3]]
    p[0] = "pushg " + o +"\nwritei\n" 
    #p[0] = p[1] + p[2] + p[3] + p[4]


def p_Read(p):
    "Read : READ '(' Ids ')' "
    p[0] = p[1] + p[2] + p[3] + p[4]


def p_error(p):
    print('Syntax error!')
    parser.success = False



#Build the parser
parser = yacc.yacc()
parser.table = dict()
parser.offset = 0


#Read input and parse it by line
import sys
linhas=""
for linha in sys.stdin:
    linhas += linha
parser.success = True
result = parser.parse(linhas)

if parser.success:
    print(result)
    print("Frase Válida reconhecida.")
else:
    print("Frase inválida. Corrija e tente de novo...")



'''
content=""
for linha in sys.stdin:
    parser.success = True
    content += linha
    parser.parse(content)
    if parser.success:
        print("Frase Válida reconhecida.",linha)
    else:
        print("Frase inválida. Corrija e tente de novo...")
'''