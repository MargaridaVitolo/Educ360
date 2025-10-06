#%%
import os
caminho = "vendas.txt"

try:
    with open(caminho,'r') as arq:
        linhas = arq.readlines()
        linhas = [linha.rstrip('\n').split(';') for linha in linhas]
        if len(linhas) == 0:
            print(f'Arquivo {caminho} vazio!')
except Exception as erro:
    print(f'Arquivo {caminho} não encontrado!')  

print ("=" * 20, "RELATÓRIO DE VENDAS", "="* 20)
cabecalho = linhas[0]
print (f"{cabecalho[0]:20}{cabecalho[1]:15}Valor   Total de Vendas {'':12}")
print ("-" * 61)

   
total = 0.0
for x in linhas[1:]:
    try:
        nome   = x[0]
        depto  = x[1]
        vendas = float(x[2].replace(',','.'))
        total  += vendas
        print(f"{nome:20}{depto:15}R$     {vendas:12,.2f}")
    except (IndexError, ValueError) as erro:
        print(f"Erro nos dados da linha: {x} - {erro}")


print ("-" * 61)
print(f"{'TOTAL GERAL':35}R$     {total:12,.2f}")
print ("=" * 61)


#%%
#sugestão IA
def ler_arquivo(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as arquivo:
            linhas = [linha.strip().split(';') for linha in arquivo if linha.strip()]
        return linhas
    except FileNotFoundError:
        print(f'Arquivo "{caminho}" não encontrado!')
        return None
    except Exception as e:
        print(f'Erro ao ler o arquivo: {e}')
        return None

def imprimir_relatorio_vendas(linhas):
    if not linhas or len(linhas) < 2:
        print('Arquivo vazio ou com dados insuficientes.')
        return

    print("=" * 20, "RELATÓRIO DE VENDAS", "=" * 20)
    cabecalho = linhas[0]
    print(f"{cabecalho[0]:20}{cabecalho[1]:15}VALOR{'':12}")
    print("-" * 61)

    total = 0.0
    for linha in linhas[1:]:
        try:
            nome = linha[0]
            depto = linha[1]
            vendas = float(linha[2].replace(',', '.'))
            total += vendas
            print(f"{nome:20}{depto:15}R$ {vendas:12,.2f}")
        except (IndexError, ValueError) as e:
            print(f"Erro nos dados da linha: {linha} - {e}")

    print("-" * 61)
    print(f"{'TOTAL GERAL':35} R$ {total:12,.2f}")
    print("=" * 61)

def main():
    caminho_arquivo = 'vendas.txt'
    linhas = ler_arquivo(caminho_arquivo)
    if linhas:
        imprimir_relatorio_vendas(linhas)

if __name__ == "__main__":
    main()

#%%
# ORIGINAL QUE MONTEI

import os
caminho = "vendas.txt"


if os.path.exists(caminho):
    with open(caminho,'r') as arq:
        linhas = arq.readlines()
        linhas = [linha.rstrip('\n').split(';') for linha in linhas]
else: 
    print('Arquivo não encontrado!')  


total = 0
for x in range(21):
    nome   = (linhas[x][0])
    depto  = (linhas[x][1])
    if x == 0:
        vendas = (linhas[x][2])
        print ("=" * 20, "RELATÓRIO DE VENDAS", "="* 20)
        print (f"{nome:20}{depto:15}VALOR  {vendas:12}")
        print ("-" * 61)
    else:
        vendas = float((linhas[x][2]))
        print (f"{nome:20}{depto:15}R$    {vendas:12,.2f}")
        total = total + float(linhas[x][2])



print ("-" * 61)
print ("TOTAL GERAL", " " * 22, "R$   ", f"{total:12,.2f}")
print ("=" * 61)