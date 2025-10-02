# Margarida Vitolo

# --------------------------------------
# Operadores
# --------------------------------------
#%%
num1 = 20
num2 = 4

print ("Soma:", num1 + num2)
print ("Subtração:", num1 - num2)
print ("Multiplicação:", num1 * num2)
print ("Divisão:", num1 / num2)

#%%

num1 = 25
num2 = 7

print ("Inteiro:", num1 // num2)
print ("Resto:", num1 % num2)

#%%

print("5ˆ4", 5**4)
#%%

result= 10 + 6 * 2
print (result)

# o resultado é 22 devido a ordem de precedencia das operações 
# primeiro foi resolvida a multiplicação para depois resolver a soma

#%%
# --------------------------------------
# Variáveis e Input
# --------------------------------------

nome_cidade = "São Paulo"
print ("Tipo variável nome_cidade" )
print(type(nome_cidade))

temperatura = 23.5
print ("Tipo variável temperatura" )
print(type(temperatura))

#%%

n = int(input("Digite o número de alunos:"))
print ("Quantidade de alunos =", n)

#%%

n = float(input("Digite o preço do kg de feijão:"))
print ("Valor do kg de feijão =", n)

#%%

n = int(input("Digite um número:"))
print("A raíz quadrada desse número é:", n ** (1/2))

#%%
# --------------------------------------
# Booleano
# --------------------------------------

valor_a = 15
valor_b = 15

print("Validação", valor_a, "<", valor_b, "=", valor_a < valor_b)

#%%

palavra_1 = "Olá"
palavra_2 = "olá"

print("Validação", palavra_1, "=", palavra_2, ":", palavra_1 == palavra_2)
print("Validação", palavra_1, "<>", palavra_2, ":", palavra_1 != palavra_2)
# %%

cliente_cadastrado = True
vl_compra = float(input("Digite o valor da compra:"))

frete_gratis = (vl_compra >= 200 and cliente_cadastrado)

print ("Compra com isenção de frete?", frete_gratis)

#%%
# --------------------------------------
# Decisões
# --------------------------------------

numero = int(input("Digite um número (exceto o 0):"))

if numero > 0:
    print("Número positivo!")

#%%

turno = input("Digite o seu turno: (M) Manhã, (N) Noite")

if turno == 'M':
    print("Bom dia!")
else:
    print("Boa noite!")

#%%

temp = float(input("Digite a temperatura (Celsius):"))    

if temp > 30:
    print ("Está muito quente!")
elif temp < 10:
        print ("Está muito frio!")
else:
     print ("Temperatura agradável!")

#%%

num = int(input("Digite um número inteiro:"))

if (num % 2) == 0:
     if num > 10:
          print ("Número par e grande!") 
     else:
          print ("Número par e pequeno")
else:
     print ("Número ímpar!")          

#%%
# --------------------------------------
# Repetições
# --------------------------------------

x = 1

while x <= 7:
     print (x)
     x = x + 1

#%%
     
x = 5

while x >= 1:
     print (x)
     x = x - 1

#%%

x = 1
numero= int(input("Qual a tabuada deseja montar:"))
              
while x <= 10:
    print (x, "*", numero, "=", x* numero)
    x = x + 1       

#%%

soma = 0

while True:
    numero = float(input("Digite um número:"))
    soma = soma + numero
    if numero == 0 or soma >= 100:
        break

     