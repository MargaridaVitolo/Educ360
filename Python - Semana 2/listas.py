#%%
dados = [20,10,40,30]
#type(dados)
#for x in range(4):
#    print(dados[x])

#dados[-1] #devolve o último
#dados[-2] #devolve o penúltimo

#Funcões
# sum, max, min, equacao=media

print('Soma', sum(dados))
print('Maior', max(dados))
print('Menor', min(dados))
print('Tamanho', len(dados))
print('Média', sum(dados) / len(dados))

print('Dados ordenados', sorted(dados))