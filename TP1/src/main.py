import re
import sys
import os

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
    else: name = "no name"

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
    else: equipa = "Individual"
    
    #alinea a 
    if re.match(r'(?i)(indiv)', equipa):
        equipa = "Individual"
        if re.search(r'(?i)(valongo)', address): 
            atletas.append(name.upper())
    #alinea b
    if re.match(r'(?i)(paulo|ricardo)', name) and re.match(r'.*(?i:)(gmail).*', email):
        atletasb.append((name, email, prova))
    #alinea c
    if re.search(r'(?i)(^turbulentos)$', equipa):
        turbulentos.append((name, birth, address, email, prova, escalao, equipa))
    #alinea d
    escaloes[escalao] = escaloes[escalao] + 1 if escalao in escaloes else 1
    #alinea e 
    equal = False
    equipa_low = equipa.lower()
    if equipa_low in equipas:
        for(n,_,e,p,_) in equipas[equipa_low]:
            #if name and email are the same we consider the same person
            if n==name and e==email:
                if prova not in p:
                    print("name : %s equipa %s" % (n, equipa))
                    p.append(prova)
                equal = True
                break
        if not equal: 
            equipas[equipa_low].append((name, birth, email, [prova], escalao))
    else: 
        equipas[equipa_low] = [(name, birth, email, [prova], escalao)]



#------------------------------ HTML files ------------------------------------------
#creates html file for a team with info about all its elements 
def equipaHTML(equipa, file_name):
    f = open(file_name,'w')  

    docHTML = """
<!DOCTYPE html>
<html>
  <head>
    <title>Organizador de provas de Orientação</title>
    <meta charset="UTF-8">
  </head>
    <body>
        <h1>Trabalho PL 1</h1>
        <h2>Processador de Inscritos numa atividade Desportiva</h2>

        <h3>Constituição detalhada da equipa '""" + equipa + """'</h3>
        <ul>""" 

    for (nome,data,email,provas,escalao) in equipas[equipa]:
            docHTML = docHTML + """
            <li>Nome: """ + nome + "</li>"
            docHTML += """
            <details>
                <summary>Mais informação</summary>
                <ul>
                    <li>Data de Nascimento:""" + data + """</li>
                    <li>Email: """ + email + """</li>
                    <li>Provas: """ + "; ".join(provas) + """</li>
                    <li>Escalão: """ + escalao + """</li>
                </ul>
            </details>"""
    
    docHTML += """
        </ul>
    </body>
</html>"""   
    f.write(docHTML)
    f.close()   


#creates html file with name of all teams and number of elements 
def equipasHTML():
    if not os.path.exists('html'):
        os.makedirs('html')

    f = open('./equipas.html','w')

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
        file_name = "./html/" + "_".join(re.split(r"[/' ]", equipa)) + ".html"
        equipaHTML(equipa, file_name)
        docHTML = docHTML + """
            <li> <a href =""" + file_name+ ">" + equipa + "</a>  = " + str(len(equipas[equipa])) + "</li>"

    docHTML += """
        </ul>
    </body>
    <div class="grupo">
        <p><strong>Grupo 70:</strong> 
        <ul>
            <li>Ana César a86038</li>
            <li>Margarida Faria a71924</li>
        </ul>
        </p>
    </div>
</html>
    """
    f.write(docHTML)
    f.close()
    print("\nFicheiro HTML criado com o nome 'equipas.html' :)\nPath para o ficheiro: ./equipas.html\n")


# ------------------------------   Parse file ------------------------------
def readFile(conteudo): 
    #catchs all groups of info
    cenas = re.findall(r'{[^{]+}', conteudo) #because of [^{] only catchs the info we need  
    for group in cenas:
        parseGroup(group)
    

with open("inscritos-form.json") as f: 
    conteudo = f.read()
    readFile(conteudo)

# ------------------------------ User interface -------------------------------

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

# Functions to show results 
def showCommand1():
    print("Nome dos concorrentes 'Individuais' e de 'Valongo':")
    print(',\n'.join(atletas))

def showCommand2():
    print("Concorrentes cujo nome é 'Paulo' ou 'Ricardo' e cujo email é 'Gmail' :")
    print('-'*111)
    print('| {:<45}| {:<40}| {:<20}|'.format("Nome", "Email", "Prova"))
    print('-'*111)
    for (nome, email, prova) in atletasb :
       print('| {:<45}| {:<40}| {:<20}|'.format(nome, email, prova))
    print('-'*111)

def showCommand3():
    print("Informação dos atletas da equipa 'Turbulentos':")
    for(name, birth, address, email, prova, escalao, equipa) in turbulentos:
        print('[Nome    = %s\n DataNac = %s\n Morada  = %s\n Email   = %s\n Prova   = %s\n Escalao = %s\n Equipa  = %s]\n' % (name, birth, address, email, prova, escalao, equipa))

def showCommand4():
    print("Lista dos escalões por ordem alfabética")
    print('-'*65)
    print('| {:<40}| {:<20}|'.format("Escalão", "Nº atletas inscritos"))
    print('-'*65)
    for k,v in sorted(escaloes.items()):
            print('| {:<40}| {:<20}|'.format(k,v))
    print('-'*65)

# user interaction 
menu()
print("Selecione a sua opção:")
for command in sys.stdin:
    print()
    if command == '1\n': showCommand1()
    elif(command == '2\n'): showCommand2()
    elif(command == '3\n'): showCommand3()
    elif command == '4\n':  showCommand4()
    elif command == '5\n': equipasHTML()
    elif command == '6\n': menu()
    elif(command == '0\n') : break
    else: print("Opção inválida")
    print("Selecione a sua opção: (6 para ver Menu)")