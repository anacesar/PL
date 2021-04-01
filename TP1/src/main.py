import re
import sys

# ------------------------------ Data Structures -------------------------------

#alinea a -> nome de todos os ateltas "individuais" e de "Valongo"
atletas = []

#alinea b -> nome, email e prova dos inscritos "Paulo" ou "Ricardo" that use "Gmail"
atletasb = []

#alinea c -> toda a info dos inscritos que pertencem à equipa "TURBULENTOS"
turbulentos = []

#alinea d -> dicionario com o número de atletas por escalao 
escaloes = {}

#alinea e -> dicionario com informacao dos ateltas por equipa
equipas = {}

#------------------------------ Regexs ------------------------------------------
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

escalao_regex = re.compile(r'"escalao":"([\w ]+)"')

equipa_regex = re.compile(r'"equipa":"([\w \-\.,|\/\'&]+|)"')


# use regexs to catch fields of information
def parseGroup(group):
    if name := name_regex.search(group) : name = name.group(1)
    else: name = "anonymus"

    if birth := birth_regex.search(group): birth = birth.group(1)
    else: birth = "no birth"

    if address := address_regex.search(group): address = address.group(1)
    else: adress = "no address" 

    if email := mail_regex.search(group): email = email.group(1)
    else: email = "no email"
    
    if prova := prova_regex.search(group): prova = prova.group(1)
    else: prova = "no prova"

    if escalao := escalao_regex.search(group): escalao = escalao.group(1)
    else: escalao = "Sem escalao"
    
    if equipa := equipa_regex.search(group): equipa = equipa.group(1)
    else: equipa = "no equipa"
    
    #alinea a 
    if re.match(r'(?i)(indiv)', equipa):
        equipa = "Individual"
        if re.search(r'(?i)(valongo)', address): 
            atletas.append(name.upper())
    #alinea b
    if re.match(r'(?i)(paulo|ricardo)', name) and re.match(r'.*(?i:)(gmail).*', email):
        atletasb.append((name, email, prova))
    #alinea c
    if re.search(r'^(?i)(turbulentos)$', equipa):
        #equipa = "turbulentos, Turbulentos ou TURBULENTOS"
        turbulentos.append((name, birth, address, email, prova, escalao, equipa))
    #alinea d
    escaloes[escalao] = escaloes[escalao] + 1 if escalao in escaloes else 1
    #aline e 
    if equipa in equipas:
        equipas[equipa].append((name, birth, email, prova, escalao))
    else: 
        equipas[equipa] = [(name, birth, email, prova, escalao)]



#Maaaaagz penso que seja esta a ideia para construir o cenas 
# temos que iterar as equipas com aquele for e passar aquilo para html COMO??? nao sheiiii
def equipasHTML():


    f = open('equipas.html','w')

    docHTML = """
<!DOCTYPE html>
<html>
  <head>
  <!--titulo associada a barra do browser-->
    <title>Organizador de provas de Orientação</title>
    <meta charset="UTF-8">
  </head>
    <body>
        <h1>Trabalho PL 1</h1>
        <h2>Processador de Inscritos numa atividade Desportiva</h2>

        <h3>Nome das equipas e número de atletas que a constituem</h3>
        <ul>"""

    for equipa in sorted(equipas, key = lambda key: len(equipas[key]), reverse=True):
        #print('{}   --> {}\n'.format(k,len(equipas[k])))
        docHTML += "<li>" + equipa + " = " + str(len(equipas[equipa])) + "</li>"
        print(docHTML)

    docHTML += """
        </ul>
    </body>
</html>
    """
    f.write(docHTML)
    f.close()
    print("file closed")

# ------------------------------   Parse file ------------------------------
def readFile(conteudo): 
    #catchs all groups of info
    cenas = re.findall(r'{[^{]+}', conteudo) #because of [^{] only catchs the info we need  
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

menu()
print("Selecione a sua opção:")
for command in sys.stdin:
    if command == '1\n': 
       print("Nome dos concorrentes 'Individuais' e de 'Valongo':")
       print(',\n'.join(atletas))
    elif(command == '2\n'):
       print("Nome dos concorrentes 'Individuais' e de 'Valongo':")
       for (nome, email, prova) in atletasb :
           print("nome: %s\n email: %s\n prova: %s" % (nome, email, prova))
    elif(command == '3\n'):
       print("Informação dos atletas da equipa 'Turbulentos':")
       for(name, birth, address, email, prova, escalao, equipa) in turbulentos:
            print('[nome = %s\ndataNac = %s\nmorada = %s\nemail = %s\nprova = %s\nescalao = %s\nequipa = %s\n' % (name, birth, address, email, prova, escalao, equipa))
    elif command == '4\n': 
        print("Escalão  | Nº atletas inscritos ")
        for k,v in sorted(escaloes.items()):
            print('{}   --> {}'.format(k,v))
    elif command == '5\n':
        equipasHTML()
    elif command == '6\n':
        menu()
    elif(command == '0\n') : break
    else: print("Opção inválida")
    print("Selecione a sua opção: (6 para ver Menu)")

