#%%
import os
caminho = "arquivo.txt"

if os.path.exists(caminho):
    with open(caminho,'r') as arq:
        x = 0
        for linha in arq:
            #strip - elimina espaços antes e depois da linha
            #rstrip - elimina espaços a direita
            #lstrip - elimina espaços a esquerda
            #if linha.rstrip() == "Marco Mastria":
            #    print(linha.rstrip())
            print(linha.rstrip())
            x = x + 1
        print("Total de linhas", x)
else: 
    print('Arquivo não encontrado!')

#%%
import os
caminho = "arquivo.txt"

if os.path.exists(caminho):
    with open(caminho,'r') as arq:
        x = 0
        for linha in arq:
            x = x + 1
        print("Total de linhas", x)
else: 
    print('Arquivo não encontrado!')  

print(tuple(open(caminho,'r')))

#%%

# verificar o ; após a associação do 0 ao x
# x= 0;