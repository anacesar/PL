'''
imprimir o nome (convertido para maiúsculas) de todos os concorrentes que se inscrevem como
'Individuais' e são de 'Valongo'.
'''
import re

atletas = []

name_regex = re.compile(r'"nome":"([a-zA-ZçóáéíãâÁ ]+)"')
birth_regex = re.compile(r'"dataNasc":"(.+)"')


def stuff(info): 
    if name := name_regex.search(info): print(name.group(1))
    ##birth = birth_regex.search()

def func(conteudo): 
    
    cenas = re.findall(r'{[^{]+}', conteudo)
    for m in cenas:
        stuff(m)
        #if(cenas) : print(cenas.group())
    

with open("inscritos-form.json") as f: 
    conteudo = f.read()
    func(conteudo)


'''
for linha in f:
    res = atleta.findall(linha)
    if(res):
        print(res)
'''



