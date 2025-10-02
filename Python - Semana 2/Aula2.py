# Margarida Vitolo

# ------------------------
# Listas
# ------------------------
#%%

vendas = [23,45,54,67]

print("Soma de valores:", sum(vendas))
print('Maior:', max(vendas))
print('Menor:', min(vendas))
print('Total itens:', len(vendas))

vendas.append(500)
vendas.insert(1,999)

print(vendas)

#%%
# ------------------------
# Slices
# ------------------------
#%%

alfabeto = ["A","B","C","D","E","F","G"]

print(alfabeto[2:5])

#%%

numeros = [3,6,9,12,15]
#numeros impares
print('Números ímpares', numeros[0:5:2])

#inverter a lista
print('Lista invertida', numeros[::-1])

#%%
# ------------------------
# SPLIT
# ------------------------
#%%

registro_paises = "Brasil,Argentina,Chile,Uruguai,Paraguai"

lista = registro_paises.split(",")
print(lista)

#%%

registro_funcionario = "ID005;Maria Silva;12500.75;Contabilidade"

lista2 = registro_funcionario.split(";")
print(lista2)

if float(lista2[2]) > 50000:
    print(lista2[1])
    print("Salário superior 50000")
else:
    print(lista2[1])
    print("Salário inferior 50000")

#%%
# ------------------------
# DICIONÁRIOS
# ------------------------
#%%

aluno = {"Nome":"Margarida",
         "Idade": 58,
         "Curso":"Análise dados com Python"
         }

print(aluno["Nome"])
#%%
produto = input("Nome do produto")

estoque={
    "TV":1500,
    "Rádio":200,
    "Microondas":900
}

if produto in estoque:
    print("Preço do produto", produto, "=", estoque [produto])
else:
    print(produto, "não cadastrado(a)")

#%%
# ------------------------
# MÓDULOS
# ------------------------
#%%    

import random

numeros = []
for x in range(5):
    numeros.append (random.randint(1,100))

print("Lista", numeros)    

#%%
# ------------------------
# TUPLAS
# ------------------------
#%%     

dados_empresa=("Matriz 01", 2023, ["Alice", "Roberto", "Carla"])

print(dados_empresa[2][0])

dados_empresa[2].append("Felipe")

print(dados_empresa[2])