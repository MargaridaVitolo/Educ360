#%%

linha=["Margarida", 
       [10,20,30],
       "Marco", 
       "Ana",
       [1967,1968,1992]]

# inicio e quantidade - e a quantidade sempre é a partir do início
print(linha[2:4])

#percorre a string e pega a penúltima posição
print(linha[0][-2])
#percorre a lista interna e pega o último elemento
print(linha[1][-1])

anos = linha[4]

print(anos[0:2])
print(anos[1:3])

#%%
linha=["Margarida", 
       [10,20,30],
       "Marco", 
       "Ana",
       [1967,1968,1992,1994,1995]]

anos = linha[4]

print(anos[1:5])
print(anos[0:5:2])
#%%
linha=["Margarida", 
       [10,20,30],
       "Marco", 
       "Ana",
       [1967,1968,1992],
       [1,2,3,4,5,6,7,8,9]]

numeros = linha[5]
#numeros impares
print('Números ímpares', numeros[0:9:2])
#numeros pares
print('Números pares', numeros[1:9:2])
#inverter a lista
print('Lista invertida', numeros[::-1])

print('Lista invertida(2)', numeros[8:0:-1])