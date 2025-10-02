#%%
x = 1

while x <= 10:
    print (x, "-----------")
    x = x + 1

#%%
a = 1
x = int(input("Repetições:"))
              
while a <= x:
    print (a, "-----------")
    a = a + 1
#%%
x = 1
numero= int(input("Qual a tabuada:"))
              
while x <= 10:
    print (x, "*", numero, "=", x* numero)
    x = x + 1

#%%

x = 10
numero= int(input("Qual a tabuada:"))
              
while x >= 1:
    print (x, "*", numero, "=", x* numero)
    x = x - 1  

#----------------------------------------
#%%
# for - sempre começa no 0 (start, stop, step)

numero= int(input("Qual a tabuada:"))

for x in range(1,11):
    print (x, "*", numero, "=", x* numero)