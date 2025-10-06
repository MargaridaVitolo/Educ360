#%%
try:
    a = 12/0
except:
    print("Erro: divisão por zero")

    #%%
#%%
a = 0
b = 4

try:
    x = 12/a
except:
    x = 12/b
    print(x)
#%%
a = 0
b = 4

try:
    x = 12/a
except Exception as erro:
    print("Erro:", erro)