'''
imprimir o nome (convertido para maiúsculas) de todos os concorrentes que se inscrevem como
'Individuais' e são de 'Valongo'.
'''


import re

atletas = []

atleta = re.compile(r'"nome":"(([a-zA-Z ])+")')

f = open("teste.json")

for linha in f:
    res = atleta.findall(linha)
    if(res):
        print(res)

