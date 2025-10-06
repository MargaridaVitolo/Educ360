#%%
import os
caminho = "arquivo.txt"

if os.path.exists(caminho):
    print("existe")
else: 
    print ("não existe")

#%%
import os
caminho = "arquivo.txt"

if os.path.exists(caminho):
    arq = open(caminho,'a')
else: 
    arq = open(caminho,'w')

linhaAdd = '\nLinha+'   
arq.write(linhaAdd)
#%%
import os
caminho = "arquivo.txt"

if os.path.exists(caminho):
    arq = open(caminho,'a')
else: 
    arq = open(caminho,'w')

linhaAdd = input("Digite nome do Aluno")
linhaAdd = '\n' + linhaAdd #+ para concatenar
arq.write(linhaAdd)

#%%
import os
caminho = "alunos.txt"

if os.path.exists(caminho):
    arq = open(caminho,'a')
else: 
    arq = open(caminho,'w')

while True:
    linhaAdd = input("Digite nome do Aluno - (Sair para parar)")
    if linhaAdd == 'Sair':
        break
    else:
        linhaAdd = '\n' + linhaAdd 
        arq.write(linhaAdd)

arq = open(caminho,'r')
linhas = arq.read()
print(linhas)