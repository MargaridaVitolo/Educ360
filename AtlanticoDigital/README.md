# Educ360 - Dashboard de Análise de Projetos

Dashboard interativo desenvolvido para a **Atlântico Digital** para análise de métricas de performance de gestão de projetos e tarefas.

## 📋 Sobre o Projeto

O Educ360 é uma aplicação de business intelligence construída com Streamlit que permite analisar dados de gestão de tarefas e projetos, gerando insights sobre produtividade de equipes, cumprimento de prazos (SLA) e qualidade de entrega.

### Funcionalidades Principais

- **Upload de Dados**: Suporta arquivos CSV e Excel com estrutura específica
- **4 Relatórios Analíticos**:
  - Tarefas Reabertas - análise de reaberturas por equipe
  - Análise SLA - compara esforço estimado vs. realizado
  - Tempo Médio por Tipo de Tarefa - desempenho por categoria
  - Tempo Médio por Cliente - métricas por cliente
- **Filtros Interativos**: quadro, grupo, projeto, cliente, tipo de tarefa, período
- **Visualizações**: Gráficos interativos com Plotly
- **Detecção de Outliers**: Método IQR para análise robusta
- **Drill-down**: Navegação hierárquica nos dados

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- UV (gerenciador de pacotes)

### Instalação

```bash
# Navegar até o diretório do projeto
cd AtlanticoDigital

# Instalar dependências
uv sync
```

### Executar a Aplicação

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Executar o dashboard
streamlit run Atlantico.py
```

A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
AtlanticoDigital/
├── Atlantico.py              # Aplicação principal Streamlit
├── drill.py                  # Exemplo de drill-down
├── AtlanticoDigital.csv      # Dataset de exemplo (636 KB)
├── atividade extra.csv       # Dados suplementares
├── pyproject.toml           # Configuração do projeto e dependências
├── requirements.txt         # Dependências locked (gerado por uv)
├── README.md                # Este arquivo
└── Atlantico.gif            # Logo da empresa
```

## 📊 Formato dos Dados

A aplicação espera um arquivo CSV/Excel com **16 colunas**:

| Coluna | Descrição |
|--------|-----------|
| `quadro` | Board/Categoria |
| `cliente` | Nome do cliente |
| `grupo` | Grupo da tarefa |
| `projeto` | Nome do projeto |
| `tipo_tarefa` | Tipo da tarefa |
| `equipe` | Equipe responsável (separadas por vírgula) |
| `para` | Pessoa asignada |
| `id_tarefa` | ID da tarefa |
| `dt_abertura` | Data de abertura |
| `dt_entrega_desejada` | Data desejada de entrega |
| `dt_fechada` | Data de fechamento |
| `esforco_estimado` | Esforço estimado (horas) |
| `esforco_registrado` | Esforço registrado (horas) |
| `percentual_realizado` | % concluído |
| `fase` | Fase da tarefa |
| `st_reaberta` | Status de reabertura (Sim/Não) |

## 🛠️ Stack Tecnológica

- **Framework**: Streamlit 1.50+
- **Dados**: Pandas 2.3+, NumPy 2.3+
- **Visualização**: Plotly 6.3+
- **Text Matching**: thefuzz (FuzzyWuzzy)
- **Tabelas**: streamlit-aggrid
- **Gerenciador**: UV

## 🔍 Como Usar

1. **Abrir a aplicação** no navegador
2. **Fazer upload** do arquivo de dados (CSV/Excel)
3. **Selecionar** os relatórios desejados
4. **Aplicar filtros** conforme necessário
5. **Explorar** gráficos e tabelas interativas
6. Usar **drill-down** nas seções expansíveis para detalhes

## 📈 Recursos Avançados

- **Correção Fuzzy**: Normaliza nomes de projetos inconsistentes
- **Detecção de Outliers**: Remove anomalias usando IQR
- **Equipes Múltiplas**: Separação de múltiplas equipes em registros
- **Formatação Automática**: Conversão de horas para formato HH:MM
- **Top-N Configurável**: Limite resultados por métrica

## 📝 Desenvolvimento

### Autor
Margarida Vitolo

### Version
0.1.0

### Licença
Proprietário - Atlântico Digital

## 📞 Suporte

Para reportar bugs ou solicitar funcionalidades, entre em contato com a equipe de desenvolvimento.

---

**Nota**: Esta aplicação foi desenvolvida especificamente para as necessidades analíticas da Atlântico Digital. A estrutura de dados deve corresponder exatamente ao formato esperado.
