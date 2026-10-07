# 📊 Análise de Rentabilidade de Operações de Câmbio

Projeto de análise de dados que simula o dia a dia de uma **fintech de câmbio e pagamentos internacionais**, com foco em **análise de rentabilidade, spread e performance** por cliente, moeda e corredor.

> 💡 Projeto construído para demonstrar habilidades práticas em **SQL, Python, Looker Studio e Google Sheets**, aplicadas a um contexto real de negócio.

---

## 🎯 Objetivo

Responder perguntas de negócio que uma fintech de câmbio enfrenta no dia a dia:

1. Qual moeda gera mais **margem**?
2. Qual **segmento de cliente** é mais rentável?
3. Qual **corredor de moedas** movimenta mais volume?
4. Quem são os **top clientes** por receita?
5. Como a **rentabilidade evolui** ao longo do tempo?

---

## 🛠️ Stack utilizada

![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458?style=flat&logo=pandas&logoColor=white)
![Looker Studio](https://img.shields.io/badge/Looker_Studio-4285F4?style=flat&logo=looker&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=flat&logo=google-sheets&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)

- **SQL** (SQLite) — modelagem e queries analíticas
- **Python** (pandas, faker, numpy) — geração de dados e cálculos financeiros
- **Looker Studio** — dashboard interativo
- **Google Sheets** — fonte de dados do dashboard
- **Git/GitHub** — versionamento

---

## 📁 Estrutura do projeto

```
analise-rentabilidade-cambio/
│
├── data/
│   ├── raw/
│   │   └── operacoes.csv                    # Base bruta (gerada)
│   ├── processed/
│   │   ├── operacoes_com_margem.csv         # Base detalhada com margem
│   │   ├── analise_rentabilidade.csv        # Agregações por dimensão
│   │   └── base_looker.csv                  # Base final pro dashboard
│   └── cambio.db                            # Banco SQLite
│
├── scripts/
│   ├── gerar_dados.py                       # Gera 1.000 operações sintéticas
│   ├── carregar_sqlite.py                   # Carrega CSV no SQLite e roda queries
│   ├── analise.py                           # Calcula margem e agregações
│   └── preparar_para_looker.py              # Prepara base pro Looker Studio
│
├── sql/
│   ├── 01_criar_tabelas.sql                 # Schema da tabela
│   └── 02_queries_analise.sql               # 6 queries de análise de negócio
│
├── dashboard/
│   └── link_looker_studio.md                # Link do dashboard público
│
├── imagens/
│   └── dashboard.png                        # Print do dashboard
│
└── docs/
    └── insights.md                          # Insights de negócio
```

---

## 🔄 Como o projeto funciona

```
┌─────────────────────┐
│  gerar_dados.py     │  Gera 1.000 operações sintéticas realistas
│  (Python + Faker)   │  → data/raw/operacoes.csv
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ carregar_sqlite.py  │  Cria schema e roda queries SQL
│  (SQLite + SQL)     │  → data/cambio.db
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   analise.py        │  Calcula margem, receita e agregações
│     (pandas)        │  → data/processed/*.csv
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ preparar_looker.py  │  Gera base plana e amigável pro BI
│     (pandas)        │  → data/processed/base_looker.csv
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Looker Studio     │  Dashboard interativo
│  (via Google Sheets)│  → KPIs, gráficos e insights
└─────────────────────┘
```

---

## 📊 Principais insights

Base simulada com **1.000 operações de câmbio em 2024**, totalizando:

| Métrica | Valor |
|---------|-------|
| Volume total transacionado | **R$ 89,6 milhões** |
| Margem total | **R$ 2,2 milhões** |
| Margem média por operação | **R$ 2.234** |
| Margem % sobre volume | **2,49%** |

### 🔍 Descobertas principais

**1. EUR gera mais margem que USD, mesmo com menos operações**
- EUR: R$ 714 mil de margem (253 operações)
- USD: R$ 561 mil de margem (419 operações)
- **Insight:** o spread do EUR é maior (2,7% vs 1,7%), então vale priorizar esse corredor.

**2. Segmento Corporate concentra ~72% da margem total**
- Corporate: R$ 1,6M de margem (ticket médio de R$ 631k)
- PME: R$ 491k
- PF: R$ 66k
- **Insight:** foco em Corporate traz retorno desproporcional.

**3. Margem média por operação é de R$ 2.234**
- Isso representa **2,49% do volume transacionado**
- Benchmark saudável para fintechs de câmbio.

**4. Corredor BRL → EUR é o mais rentável**
- Apesar de BRL → USD ter mais volume, BRL → EUR gera mais margem.

> 📖 Análise completa em [`docs/insights.md`](docs/insights.md)

---

## 📈 Dashboard

O dashboard no Looker Studio apresenta:

- **4 KPIs executivos:** volume total, margem total, margem média e margem %
- **Margem por moeda:** qual moeda gera mais rentabilidade
- **Margem por segmento:** comparação entre PF, PME e Corporate
- **Evolução mensal:** volume e margem ao longo de 2024
- **Top 10 clientes:** ranking por margem gerada
- **Volume por corredor:** distribuição por par de moedas

🔗 **[Acessar dashboard no Looker Studio](dashboard/link_looker_studio.md)**

![Dashboard](imagens/dashboard.png)

---

## 🚀 Como rodar o projeto

### Pré-requisitos

- Python 3.10+
- pip

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/MirandaJonhy/analise-rentabilidade-cambio.git
cd analise-rentabilidade-cambio

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Gere a base sintética de operações
python scripts/gerar_dados.py

# 4. Carregue no SQLite e rode as queries
python scripts/carregar_sqlite.py

# 5. Calcule as métricas e agregações
python scripts/analise.py

# 6. Prepare a base pro Looker Studio
python scripts/preparar_para_looker.py
```

O dashboard é montado no Looker Studio a partir do arquivo `data/processed/base_looker.csv`.

---

## 🧠 Decisões de design

Algumas escolhas importantes do projeto:

- **Dados sintéticos:** dados reais de câmbio são sigilosos. A simulação usa regras de negócio realistas (spread varia por moeda, custo varia por corredor).
- **Camadas raw/processed:** boa prática de pipeline — dados brutos nunca são editados à mão.
- **SQL separado do Python:** os arquivos `.sql` mostram domínio da linguagem de forma explícita.
- **Cálculo de margem:** `spread_pct × valor_brl - custo_operacional`, refletindo a margem líquida real por operação.
- **Looker Studio + Sheets:** escolhidos por serem gratuitos, acessíveis e exatamente o que a vaga pede.

---

## 📌 Possíveis evoluções

- [ ] Migrar o pipeline para **Airflow** com DAG diária
- [ ] Armazenar os dados no **BigQuery** em vez de SQLite
- [ ] Adicionar **testes automatizados** (pytest)
- [ ] Implementar **detecção de anomalias** com IA
- [ ] Gerar **resumo executivo automático** com LLM

---

## 👤 Autor

**João Victor Miranda**

- 🔗 [GitHub](https://github.com/MirandaJonhy)
- 💼 [LinkedIn](https://www.linkedin.com/in/mirandajhonhy)

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar como referência de estudo.
