#while TRUE
#%%

boleto_acum = 0

while True:
    boleto = float(input("Valor do boleto:"))
    if boleto == 0:
        break
    boleto_acum = boleto_acum + boleto

print ("Valor total a pagar:", boleto_acum)    

#%%

empresa = "Escola@gmail.com"

for letra in(empresa):
    if letra == "@":
        print("-------")
    else:
        print (letra)