#%%
n1 = int(input("Digite valor 1"))
n2 = int(input("Digite valor 2"))

result = n1 * n2

print(result)

#%%
#def cria função

def calc():
    result = n1 * n2
    print(result)

n1 = int(input("Digite valor 1"))
n2 = int(input("Digite valor 2"))

calc()
#%%

def calc(pn1, pn2):
    result = pn1 * pn2
    print(result)

calc(19,20)

#%%

def calc(pn1, pn2):
    presult = pn1 * pn2
    return presult

result = calc(19,20)
print (result)

#%%

#def calc(pn1:float, pn2:float)->int:  -- permite indicar o tipo do retorno da saída

def calc(pn1:float, pn2:float):
    """
    pn1 é o primeiro valor
    pn2 é o segundo valor
    presult é o retorno
    """    
    
    presult = pn1 * pn2
    return presult

result = calc(19,20)
print (result)