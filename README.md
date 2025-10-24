# 🚀 VelozMart Priority Sorter (MPS)

### 🧠 Otimização de priorização logística usando **Bucketed Priority Queues**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pandas](https://img.shields.io/badge/Library-pandas%20|%20numpy-yellow.svg)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-success.svg)
![License](https://img.shields.io/badge/Licença-MIT-lightgrey.svg)
![Contribuições](https://img.shields.io/badge/Contribuições-Bem--vindas-orange.svg)

---

## 📦 Sobre o Projeto

O **VelozMart Priority Sorter (MPS)** é uma simulação conceitual desenvolvida durante o programa **DiverseDEV | Mercado Eletrônico**, com o desafio de criar uma solução de **logística inteligente e priorização de pedidos**.

O objetivo é comparar o desempenho de uma **fila tradicional (FIFO)** com um modelo avançado baseado em **Bucketed Priority Queues (BPQ)** — uma técnica que agrupa pedidos em *faixas de prioridade* para otimizar o fluxo de expedição e reduzir violações de SLA.

---

<details open>
<summary>⚙️ <strong>Contexto do Problema</strong></summary>

A **VelozMart**, empresa fictícia de varejo e logística, enfrentava atrasos devido ao uso de filas simples (FIFO), que ignoravam fatores como:

- 🏷️ **priorityScore** → importância e valor do pedido  
- ⏰ **dispatchWindow** → tempo restante até o prazo  
- 📏 **sizeCategory** → impacto logístico (P, M, G)

A missão foi criar um modelo de **priorização dinâmica e escalável** para processar grandes volumes de pedidos com critérios múltiplos.
</details>

---

<details open>
<summary>🧩 <strong>Solução Proposta — Bucketed Priority Queues (BPQ)</strong></summary>

A estratégia **BPQ** combina o melhor de três mundos:
1️⃣ **Simplicidade** do peso composto (score);  
2️⃣ **Organização** por *buckets* (faixas de prioridade);  
3️⃣ **Desempenho** de estruturas de heap/fila.

#### 🧮 Cálculo de Score

```python
orderScore = priorityScore / (dispatchWindow ** 1.5 * sizeCategory)
```
Cada pedido recebe um score normalizado e é atribuído a um bucket de prioridade (ex: 0–5, 6–10...).
Dentro de cada bucket, os pedidos são ordenados por urgência e tamanho.
</details>


<details> <summary>📊 <strong>Comparação FIFO × BPQ</strong></summary>

A simulação gera dados sintéticos com milhares de pedidos e avalia métricas de desempenho entre dois métodos:

| Método | ⏱️ Atraso Médio | ⚠️ % SLA Estourado | 📦 Aproveitamento Médio |
|:--|:--:|:--:|:--:|
| **Bucketed Priority Queues** | ![varia](https://img.shields.io/badge/Varia_conforme_execução-blue) | ![menor](https://img.shields.io/badge/Menor_Taxa-brightgreen) | ![maior](https://img.shields.io/badge/Maior_Eficiência-brightgreen) |
| **FIFO (Ordem de Chegada)** | ![base](https://img.shields.io/badge/Valor_Base-lightgrey) | ![maior](https://img.shields.io/badge/Maior_Taxa-red) | ![menor](https://img.shields.io/badge/Menor_Aproveitamento-red) |


💡 O BPQ apresentou melhor equilíbrio entre urgência, desempenho e aproveitamento das docas, mesmo com pequenas variações no atraso médio.
```python
Exemplo de saída:

=== Resultado Buckets ===
Atraso médio: 4.22
% SLA estourado: 12.40%
Aproveitamento médio: 91.75%

=== Resultado FIFO ===
Atraso médio: 3.85
% SLA estourado: 22.30%
Aproveitamento médio: 79.52%
</details>
```
</details>

<details> <summary>🧠 <strong>Estrutura do Código</strong></summary>

1️⃣ Geração dos Dados Sintéticos
```python
df = pd.DataFrame({
    'id': range(n_pedidos),
    'tempo_chegada': np.random.randint(0, 120, n_pedidos),
    'dispatch_window': np.random.randint(5, 15, n_pedidos),
    'priority_score': np.random.uniform(1, 10, n_pedidos),
    'sizeCategory': np.random.choice(['P','M','G'], n_pedidos, p=[0.3,0.4,0.3])
})
```

2️⃣ Simulação de Lotes

A função simular_blocos() agrupa os pedidos em lotes de expedição, respeitando a capacidade máxima e recalculando o atraso e o SLA.

3️⃣ Execução e Métricas
```python
res_buckets = simular_blocos(df, metodo='buckets')
res_fifo = simular_blocos(df, metodo='fifo')
```
</details>

<details> <summary>🧪 <strong>Teste A/B — FIFO x BPQ</strong></summary>

O teste A/B compara os métodos em três dimensões principais:

  - ⏱️ Atraso médio por pedido

  - 📉 Percentual de pedidos fora do SLA

  - 📦 Aproveitamento da capacidade da doca

Mesmo com leve aumento no atraso médio, o BPQ reduz significativamente a frequência de atrasos críticos e melhora o uso dos recursos logísticos.

</details>
<details> <summary>💻 <strong>Como Executar</strong></summary>
🔧 Pré-requisitos

Python 3.9+

Bibliotecas: pandas, numpy

▶️ Instalação e Execução
```bash
pip install pandas numpy
python veloxmart_priority_sorter.py
```

O script exibirá no console as métricas comparativas entre FIFO e BPQ.

</details>


<details>
<summary>⚖️ <strong>Trade-offs da Solução</strong></summary>

| Aspecto | Nível | Justificativa |
|:--|:--:|:--|
| 🧩 **Simplicidade** | Média-baixa | Exige calibração de pesos e faixas |
| ⚡ **Desempenho** | Alto | Inserção/remoção O(1), escalável |
| 🛠️ **Manutenibilidade** | Média | Ajustes periódicos de parâmetros |

</details>

---

## 🤝 Equipe de Desenvolvimento

👥 **Grupo 1 – DiverseDEV 2025**

| Nome | Função |
|:--|:--|
| Adenir Gonçalves | 💻 Desenvolvimento |
| André Oliveira | 🔍 Lógica e Otimização |
| Andressa Ribeiro | 📊 Análise de Dados |
| Antonio Monte | ⚙️ Estrutura e Modelagem |
| Breno Fabrizio | 🧠 Algoritmos e Relatório |


🎓 Programa DiverseDEV | Mercado Eletrônico

O DiverseDEV é um programa de bolsas integrais do Mercado Eletrônico, com foco na formação de novos desenvolvedores back-end.
São mais de 370 horas de aprendizado técnico, mentoria e desafios reais, promovendo inclusão e impacto social através da tecnologia. 🌍

💬 “Inteligência logística não é apenas sobre velocidade — é sobre saber o que realmente precisa ir primeiro.”
