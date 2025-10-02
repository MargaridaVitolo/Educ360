#%%
linha = 'Olá, Margarida'
# pode usar qq caracter que será utilizado para separar os campos (,;|)
lista = linha.split(',')

print (lista)

#%%

registro = "001;Margarida;11250.00;Mogi das Cruzes"

lista = registro.split(";")
#saldo= float(lista[2])

if float(lista[2]) > 5000:
    print(lista[1])
    print("Aplicação aprovada")
else:
    print("Saldo insuficiente")