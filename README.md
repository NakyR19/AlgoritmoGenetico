---
title: TSP
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Algoritmo genético para resolução do problema do TSP
---

# 🧬 Algoritmo Genético — Caixeiro Viajante (TSP)

Implementação de um **Algoritmo Genético** para resolver o **Problema do Caixeiro Viajante** (Travelling Salesman Problem), com dashboard interativo em Streamlit.

> Projeto da **Unidade III** da disciplina de Inteligência Artificial.

---

## Página no HugginFace:

https://huggingface.co/spaces/NakyR19/TSP

---

## Participantes

LUAN ALMEIDA VALENÇA  
LUIZ FELIPE TOJAL GOMES CORUMBA  
RAFAEL MACHADO COSTA MENESES  
RAFAEL SANTOS SILVA  

---

## Estrutura do Projeto

```
ia_unidadeIII/
├── src/
│   ├── ga.py                # Classe ga — implementação do algoritmo genético
│   └── streamlit_app.py     # Dashboard Streamlit para visualização e execução
├── docs/
│   └── Relatório_IA_GA.pdf  # Relatório acadêmico do projeto
├── Dockerfile               # Configuração do container Docker (deploy HuggingFace)
├── requirements.txt         # Dependências do projeto
├── .gitignore               # Regras de ignore do Git
└── README.md                # Documentação do projeto
```

| Arquivo / Diretório | Descrição |
|----------------------|-----------|
| `src/ga.py` | Classe `ga` com toda a lógica do algoritmo genético (fitness, seleção, cruzamento, mutação e elitismo) |
| `src/streamlit_app.py` | Dashboard Streamlit com controles interativos e 5 abas de visualização |
| `docs/` | Relatório acadêmico em PDF |
| `Dockerfile` | Imagem Docker usada para deploy no HuggingFace Spaces |
| `requirements.txt` | Lista de dependências Python (`numpy`, `streamlit`, `plotly`, `pandas`) |

## Como o Algoritmo Funciona

O AG segue o pseudocódigo clássico:

```
GENETIC-ALGORITHM(population, fitness):
    repeat
        weights ← WEIGHTED-BY(population, fitness)
        population2 ← empty list
        for each individual:
            parent1, parent2 ← WEIGHTED-RANDOM-CHOICES(population, weights)
            child ← REPRODUCE(parent1, parent2)
            if (small random probability) then child ← MUTATE(child)
            add child to population2
        population ← population2
    until criteria met
    return best individual
```

### Operadores

| Operador | Método | Descrição |
|----------|--------|-----------|
| **Seleção** | `weighted_by()` | Seleção proporcional ao fitness (inversão da distância) |
| **Cruzamento** | `reproduce()` | Order Crossover (OX1) — preserva a ordem das cidades |
| **Mutação** | `mutate()` | Inversão de segmento aleatório na rota |
| **Elitismo** | — | Os melhores indivíduos passam diretamente para a próxima geração |

## Dashboard

O dashboard oferece controles interativos e 5 abas de visualização:

- **Rota** — melhor rota encontrada pelo AG
- **Evolução** — snapshots da rota em 5 gerações (primeira, 3 intermediárias e última)
- **Convergência** — curva de melhoria do fitness ao longo das gerações
- **Heatmap** — matriz de distâncias entre as cidades
- **Dados** — tabelas com coordenadas e detalhes trecho-a-trecho

### Parâmetros configuráveis

- Número de cidades (5–50)
- Tamanho da população (20–500)
- Probabilidade de mutação (0–1)
- Número de gerações (50–2000)
- Tamanho da elite (1–20)
- Seed para reprodutibilidade

## Como Executar

### 1. Instalar dependências

```bash
pip install numpy streamlit plotly pandas
```

### 2. Rodar o dashboard

```bash
streamlit run src/streamlit_app.py
```

O dashboard abrirá automaticamente no navegador. Ajuste os parâmetros na barra lateral e clique em **Executar**.

## Tecnologias

- **Python 3**
- **NumPy** — cálculos numéricos e matriz de distâncias
- **Streamlit** — interface web interativa
- **Plotly** — gráficos interativos
- **Pandas** — exibição de tabelas de dados
