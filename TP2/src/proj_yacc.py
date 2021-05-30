import ply.yacc as yacc
import re 

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
    #print(p.parser.table)
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
    p.parser.table[p[1]] = ("int", p.parser.offset, 1, 0)
    p.parser.offset+=1
    p[0] = "pushi 0\n"

def p_DeclIds_Array(p):
    "DeclIds : ID '[' NUM ']'"
    size = int(p[3])
    p.parser.table[p[1]] = ("intArray", p.parser.offset, size, list())
    p.parser.offset+=size
    p[0] = "pushn " + p[3] + "\n"

def p_Enumerate(p):
    "Enumerate : ',' DeclDef"
    p[0] = p[2]
    #p[0] = ',' + p[2]

def p_Enumerate_Empty(p):
    "Enumerate : "
    p[0] = ""
'''
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

'''
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
    p[0] = p[1] + "\n"
    #print("p2",p[1])

def p_Atr_IdNum(p):
    "Atr : Id '=' Exp"
    #print("atr with id ", p[1])
    p[0] = p[3] + "storeg " + str(sum(map(int, re.findall('\d+', p[1])))) + "\n"
    #p[0] = p[1] + '=' + p[3]

def p_Atr_IDNUM(p):
    "Atr : Array '=' Exp"
    p[0] = p[1] + p[3] + "storen\n" 
    #p[0] = p[1] + '[' + p[3] + "] = " + p[6]

def p_Instruction_Repeat(p):
    "Instruction : Repeat "
    p[0] = p[1] + "\n"


def p_Instruction_If(p):
    "Instruction : If"
    p[0] = p[1] + "\n"

def p_Instruction_Print(p):
    "Instruction : Print TERMINATOR"
    p[0] = p[1] + "\n"

def p_Instruction_Read(p):
    "Instruction : Read TERMINATOR"
    p[0] = p[1] + "\n"


def p_If(p):
    "If : IF '(' Cond ')' '{' Instructions '}' Else"
    endif = "endif" + str(p.parser.nr)
    else_ = p[8].split(':')[0]
    if(else_ == "") : else_ = endif 
    jump = "jump " + endif + "\n"
    p[0] = p[3] + "jz " + else_ + "\n" + p[6] + jump + p[8] + endif + ":" 
    p.parser.nr += 1
    #p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]

def p_Else(p):
    "Else : ELSE '{' Instructions '}'"
    else_ = "else" + str(p.parser.nr)
    p[0] = else_ + ":\n" + p[3] + "\n"

def p_ElseEmpty(p):
    "Else : "
    p[0] = ""

def p_Repeat(p):
    "Repeat : REPEAT '{' Instructions '}' UNTIL '(' Cond ')'"
    ciclo = "ciclo" + str(p.parser.nr)
    p.parser.nr += 1
    p[0] = ciclo + ":\n" + p[3] + p[7] + "jz " + ciclo + "\n"
    #p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7]

def p_PrintIdNum(p):
    "Print : PRINT '(' IdNum ')' "
    p[0] = p[3] + "writei\n" 

def p_PrintArray(p):
    "Print : PRINT '(' Array ')' "
    p[0] = p[3] + "loadn\nwritei\n" 

def p_ReadID(p):
    "Read : READ '(' ID ')' "
    (_,offset,_,_) = p.parser.table[p[3]]
    p[0] = "read\natoi\nstoreg " +  str(offset) + "\n"
    #p[0] = p[1] + p[2] + p[3] + p[4]

def p_ReadArray(p):
    "Read : READ '(' Array ')' "
    p[0] = p[3] + "read\natoi\nstoren\n"
    #p[0] = p[1] + p[2] + p[3] + p[4]


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
    p[0] = p[2] + "not\n" 

def p_Cond3_ExpR(p):
    "Cond3 : ExpRelacional"
    p[0] = p[1]

def p_Cond3(p):
    "Cond3 : '(' Cond ')'"
    p[0] = p[1] 

def p_ExpRelacional_Bigger(p):
    "ExpRelacional : Exp '>' Exp"
    p[0] = p[1] + p[3] + "sup\n"


def p_ExpRelacional_Lower(p):
    "ExpRelacional : Exp '<' Exp"
    p[0] = p[1] + p[3] + "inf\n"


def p_ExpRelacional_BiggerEqual(p):
    "ExpRelacional : Exp '>' '=' Exp"
    p[0] = p[1] + p[4] + "supeq\n"
    

def p_ExpRelacional_LowerEqual(p):
    "ExpRelacional : Exp '<' '=' Exp"
    p[0] = p[1] + p[4] + "infeq\n"


def p_ExpRelacional_Diff(p):
    "ExpRelacional : Exp '!' '=' Exp"
    p[0] = p[1] + p[4] + "equal\nnot\n"


def p_ExpRelacional_Equal(p):
    "ExpRelacional : Exp '=' '=' Exp"
    p[0] = p[1] + p[4] + "equal\n"


def p_ExpRelacional(p):
    "ExpRelacional : Exp"
    p[0] = p[1]

def p_ExpPlus(p):
    "Exp : Exp '+' Termo"
    p[0] = p[1] + p[3] + "add\n"
    #p[0] = p[1] + '+' + p[3]

def p_ExpMinus(p):
    "Exp : Exp '-' Termo"
    p[0] = p[1] + p[3] + "sub\n"

def p_ExpTermo(p):
    "Exp : Termo"
    p[0] = p[1]

def p_TermoMul(p):
    "Termo : Termo '*' Fator"
    p[0] = p[1] + p[3] + "mul\n"

def p_TermoMod(p):
    "Termo : Termo '%' Fator"
    p[0] = p[1] + p[3] + "mod\n"

def p_TermoFator(p):
    "Termo : Fator"
    p[0] = p[1]

def p_FatorExp(p):
    "Fator : '(' Exp ')' "
    p[0] = p[2]

def p_FatorIdNum(p):
    "Fator : IdNum "
    p[0] = p[1]

def p_FatorArray(p):
    "Fator : Array "
    p[0] = p[1]

def p_IdNum(p):
    "IdNum : Num"
    p[0] = p[1]

def p_IdNumId(p):
    "IdNum : Id"
    p[0] = p[1]

def p_Num(p):
    "Num : NUM "
    p[0] = "pushi " + p[1] + "\n"

def p_Id(p):
    "Id : ID "
    (_,offset,_,_) = p.parser.table[p[1]]
    p[0] = "pushg " + str(offset) + "\n"

def p_ArrayN(p):
    "Array : ArrayNum"
    p[0] = p[1]

def p_ArrayI(p):
    "Array : ArrayId"
    p[0] = p[1]

def p_ArrayNum(p):
    "ArrayNum : ID '[' NUM ']'"
    (_,offset,_,_) = p.parser.table[p[1]]
    p[0] = "pushgp\npushi " + str(offset) +"\npadd\npushi " + p[3] + "\n"

def p_ArrayID(p):
    "ArrayId : ID '[' ID ']'"
    (_,of1,_,_) = p.parser.table[p[1]]
    (_,of2,_,_) = p.parser.table[p[3]]
    p[0] = "pushgp\npushi " + str(of1) +"\npadd\npushg " + str(of2) + "\n"


def p_error(p):
    print('Syntax error!')
    parser.success = False



#Build the parser
parser = yacc.yacc()
parser.table = dict()
parser.offset = 0
parser.nr = 1

#Read input and parse it by line
import sys
linhas=""
for linha in sys.stdin:
    linhas += linha
parser.success = True
result = parser.parse(linhas)

if parser.success:
    print(result)
    #print("Frase Válida reconhecida.")
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