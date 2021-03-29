import re
import sys

# ------------- Data Structures ------------------------------------------------

#names of all atletas as individuals and from Valongo 
atletas = []

#

#-------------- Regexs ----------------------------------------------------------
name_regex = re.compile(r'"nome":"([\w ]+|)"')

#assuming valid birth formats: DD/MM/YY, DD/MM/YYYY, YY/MM/DD, YYYY/MM/DD,
#                              DD-MM-YY, DD-MM-YYYY, YY-MM-DD, YYYY-MM-DD.
day = "([012]\d|3[0-1])"
month = "(0\d|1[012])"
year = "\d{2,4}"
birth_regex = re.compile(rf'dataNasc":"({day}\/{month}\/{year}|{year}\/{month}\/{day}|{day}\-{month}\-{year}|{year}\-{month}\-{day}|)"')

#falta apanhar linha 231 --> º do alem
address_regex = re.compile(r'"morada":"([\w\-\.\/, ]*)"')

# use regexs to catch fields of information
def parseGroup(group):
    name = name_regex.search(group)
    if name: 
        name = name.group(1)
        #print(name)
    else: name = ""

    birth = birth_regex.search(group)
    if birth: birth = birth.group(1)#print(birth.group(1))
    else : 
        birth = ""
        #print("no birth")
    address = address_regex.search(group)
    if address: print(address.group(1))
    else : 
        address = ""
        print("no address")


# ---------------   Parse file --------------------------------------
def readFile(conteudo): 
    #catchs all groups of info
    cenas = re.findall(r'{[^{]+}', conteudo) #because of [^{] only catchs the info we need  
    #if(cenas) : print("cenas.group()")
    for group in cenas:
        parseGroup(group)
    

with open("inscritos-form.json") as f: 
    conteudo = f.read()
    readFile(conteudo)


# ------------------------------ User interaction --------------------------

def menu():
    print("\n ------------------- Processador de inscritos numa atividade Desportiva  ------------------- ")
    print("|                                                                                              |")
    print("|  1- nome dos atletas inscritos como 'Individuais' e são de 'Valongo'.                        |")
    print("|  2- nome, telemóvel e prova dos inscritos cujo nome é 'Paulo' ou ´Ricardo' e usam o Gmail.   |")
    print("|  3- info equipa 'TURBULENTOS'.                                                               |")
    print("|  4- lista dos escalões por ordem alfabética e número de atletas inscritos                    |")
    print("|  5- página HTML com a lista de equipes inscritas em qualquer prova.                          |")
    print("|  0- sair                                                                                     |")
    print("|                                                                                              |")
    print(" ---------------------------------------------------------------------------------------------- ")

#menu()
#for command in sys.stdin:
#    if(command == '1\n'): print("pressed option 1")
#    elif(command == '0\n') : break
#    else: print("Opção inválida")
#
    