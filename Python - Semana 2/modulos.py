# módulo interno
#%%

import infos

print(infos.empresa)
print(infos.instrutor)

#%%
#-- importa somente uma parte do outro módulo
from infos import instrutor

#print (empresa) --dá erro
print (instrutor)

#%%

import random

print(random.randint(10,20))

#%%

import random

par=0
impar = 0
numeros = []
for x in range(20):
    numeros.append (random.randint(1,100))

for x in range(20):
    if numeros[x] % 2 == 0:
        print("Número", numeros[x], "é par")
        par = par + 1
    else:
        print("Número", numeros[x], "é impar")
        impar = impar + 1

print("Total de números pares  ", par)        
print("Total de números impares", impar)        

    