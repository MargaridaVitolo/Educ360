#%%

lista=['Maria','Margarida',12] # lista

dicio = {"Nome":"Ivan",
         "Idade":50,
         "Cidade":"São Paulo",
         "Linguagens":["Python","SQL","Oracle"],
         "Cargos":[
             {"Empresa":"xpto","função":"Programador"},
             {"Empresa":"xpto1","função":"Programador1"},
             {"Empresa":"xpto2","função":"Programador2"}
         ]}
# chave / valor
#type (dicio)

#print(dicio)
#sobrepoe a chave
#dicio["nome"] = "Sandra"

#print(dicio)

'''
for chave in dicio:
    print(chave)

for valores in dicio.values():
    print(valores)

for chave in dicio.keys():
    print(chave)  

#pesquisa
if "São Paulo" in dicio.values():
    print("Encontrado")

'''
#print(dicio["Linguagens"])
# passa o nome da chave
#print(dicio[3]) --dá erro

#print(dicio["linguagens"][-1])

print(dicio["Cargos"][-1])
print(dicio["Cargos"][-1]["função"])
print(dicio["Cargos"][-1]["Empresa"])

#%%

produto = input("Nome do produto")

lista={
    "tv":1500,
    "radio":200,
    "micro":500,
    "geladeira":3500,
    "forno":900
}

if produto in lista:
    print(lista[produto])
else:
    print(produto, "não cadastrado(a)")

#%%
# Aula


nomes= [{"idade":36, "nome": "Fabio"},{"idade":35, "nome": "Eder","Depto":"TI"} ]
nomes
nomes[1]["nome"]

#for pessoa in nomes:
#    if pessoa.get("nome")=="Fabio":
#        print(pessoa["idade"])


idade_eder = [p["idade"] for p in nomes if p.get("nome") == "Eder"][0]       
print (idade_eder)

#%%

nomes= [{"nome": "Fabio","idade":35},
        {"nome": "ivan", "idade":15},
        {"nome": "Eder", "idade":35,"Depto":"TI"} 
        ]

#nomes[0].get("idade")
#nomes[0]["idade"]
#nomes[0].get("idade") = 32 cannot assign to function call here.
#nomes[0]["idade"] = 32

#nomes[0].values()

#nomes[0].items

#nomes[2].keys()

# pop tira o registro
#nomes[2].pop("Depto")
#nomes[2]

#clear - limpa
#nomes[2].clear()
#nomes
