import re
import sys

# ------------- Data Structures ------------------------------------------------

#names of all atletas as individuals and from Valongo 
atletas = []

#nome, email e prova 
atletasb = []

#-------------- Regexs ----------------------------------------------------------
name_regex = re.compile(r'"nome":"([\w\. ]+|)"')

#assuming valid birth formats: DD/MM/YY, DD/MM/YYYY, YY/MM/DD, YYYY/MM/DD,
#                              DD-MM-YY, DD-MM-YYYY, YY-MM-DD, YYYY-MM-DD.
day = "([012]\d|3[0-1])"
month = "(0\d|1[012])"
year = "\d{2,4}"
birth_regex = re.compile(rf'dataNasc":"({day}\/{month}\/{year}|{year}\/{month}\/{day}|{day}\-{month}\-{year}|{year}\-{month}\-{day}|)"')

address_regex = re.compile(r'"morada":"([\w\-\.\/, ]*|)"')

mail_regex = re.compile(r'"email":"(\b([\w\-]+\.)*[\w\-]+@([\w\-]+\.)*\w+\b|)"')

prova_regex = re.compile(r'"prova":"([\w \-:]+|)"')

escalao_regex = re.compile(r'"escalao":"([\w ]+|)"')

equipa_regex = re.compile(r'"equipa":"([\w \-\.,|\/\'&]+|)"')

# use regexs to catch fields of information
def parseGroup(group):
    if name := name_regex.search(group) : name = name.group(1)
    else: name = "anonymus"

    if birth := birth_regex.search(group): birth = birth.group(1)#print(birth.group(1))
    else: birth = "no birth"

    if address := address_regex.search(group): address = address.group(1)
    else: adress = "no address" 

    if email := mail_regex.search(group): email = email.group(1)
    else: email = "no email"
    
    if prova := prova_regex.search(group): prova = prova.group(1)
    else: prova = "no prova"

    if escalao := escalao_regex.search(group): escalao = escalao.group(1)
    else: prova = "no escalao"
    
    if equipa := equipa_regex.search(group): equipa = equipa.group(1)
    else: equipa = "no equipa"
    
    #alinea a 
    if re.match(r'(?i)(indiv)', equipa) and re.search(r'(?i)(valongo)', address): 
        #equipa = "Individual"
        #print("%s --> %s    | %s" % (name, equipa, address))
        atletas.append(name.upper())
    if re.match(r'(?i)(paulo|ricardo)', name) and re.search(r'.*@.*(?i)(gmail).*', email):
        atletasb.append((name, email, prova))
    
    #print('[nome = %s\ndataNac = %s\nmorada = %s\nemail = %s\nprova = %s\nescalao = %s\nequipa = %s\n' % (name, birth, address, email, prova, escalao, equipa))


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


print(atletasb)
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