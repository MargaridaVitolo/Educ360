#%%
def soma(pn1:int, pn2:int, pn3:int):
    return (pn1 + pn2 + pn3)

def media(ptotal:int, pqt:int):
    return ptotal / pqt

print(media(60,3))
print(soma(10,20,30))

print (media(soma(10,20,30),3))

#%%

def soma(pval:list):
    return sum(pval)

def media(ptotal:float, pqt:int):
    return ptotal / pqt

valores = [10,20,30,40,50]

print(soma(valores))

print(media(soma(valores),len(valores)))

#%%

def soma(*arg:int)->int:
    return sum(*arg)

valores = [10,20,30,40,50]

print(soma(valores))
#%%

def soma(nome:str, *arg:int)->int:
    print("Nome:", nome)
    return sum(*arg)

valores = [10,20,30,40,50]

print(soma("Jonas", valores))