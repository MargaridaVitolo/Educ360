open('arquivo.txt')

#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'r')

print(conteudo.read())
#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'r')
linhas = conteudo.read()
print(linhas)

#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'w')

# com isso o arquivo foi "zerado"
# se p arquivo não existe ele vai criar o arquivo


#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'r+')
linhas = conteudo.read()
print(linhas)
#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'r+')
linhas = conteudo.write('Linha acionada')
# grava na primeira linha - sobrepondo o primeiro registro
#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'w+')
linhas = conteudo.write('Linha acionada')
# trunca o arquivo e coloca o dado da linha acima
#%%
varArquivo = 'arquivo.txt'
conteudo = open(varArquivo,'rb')
linhas=conteudo.read()
print(linhas)
# arquivo binario

