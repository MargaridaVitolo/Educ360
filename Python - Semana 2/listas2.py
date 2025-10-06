#%%

linha=["Margarida", 
       [10,20,30],
       "Marco", 
       "Ana",
       [1967,1968,1992]]

#print(linha[1][1])

#numeros = linha[1]
#type (numeros)
#print(numeros[-1])

#print(linha[-1][-1])

#%%

# inclusões

dados = [10]
#entrada = int(input("Digite um valor"))
#dados.append(entrada)
dados.append(int(input("Digite um valor")))

#insere o valor em uma posição específica
dados.insert(0,30)

dados

#%%
#aulas

a = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
print(a) #Lista original com duplicatas
i = 0
j = 1
while (i <= len(a)-2):
    while (j <= len(a)-1):
        if a[i] == a[j]:
            del(a[j])
        else:
            j += 1
    i += 1
    j = i+1

print(a)

#%%
a = [1,2,3,4,5,6,7,8,9,10,1,2,3,4,11,5,6,7,8,9,10]

b = list(set(a))

c = list(dict.fromkeys(a))
print(a)
print(b)
print(c)