#%%

#dados_lista=[58,'Margarida','SP']
#print(type(dados_lista))

# não permite repetições
#pesquisa é mais rápida pois não permite repetições

dados_tupla=(58,'Margarida','SP',["RJ","BA"])
#print(type(dados_tupla))
# TypeError: 'tuple' object does not support item assignment
# não permite alterações
#dados_tupla[0] = 57

# não permite alteração na tupla, entretanto se vc tiver uma lista como um item
# será possível fazer a edição do conteúdo
dados_tupla[3].append("PE")

print(dados_tupla[3])