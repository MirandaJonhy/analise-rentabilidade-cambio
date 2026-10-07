"""
gerar_dados.py
---------------
Gera uma base sintética de operações de câmbio simulando o dia a dia
de uma fintech de pagamentos internacionais.

Saída: data/raw/operacoes.csv

Regras de negócio simuladas:
- Moedas diferentes têm spreads diferentes (USD é mais competitivo, EUR/GBP têm spread maior).
- Segmentos de cliente têm tickets médios diferentes (PF < PME < Corporate).
- O custo operacional varia por corredor (moeda de destino).
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

# ----------------------------
# Configurações iniciais
# ----------------------------
fake = Faker("pt_BR")
Faker.seed(42)
random.seed(42)
np.random.seed(42)

QTD_OPERACOES = 1000
DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM = datetime(2024, 12, 31)

# Moedas e regras de negócio (spread base e custo operacional por corredor)
MOEDAS = {
    "USD": {"spread_base": 0.015, "custo_base": 12.0},  # moeda mais competitiva
    "EUR": {"spread_base": 0.025, "custo_base": 18.0},
    "GBP": {"spread_base": 0.030, "custo_base": 22.0},
    "ARS": {"spread_base": 0.045, "custo_base": 8.0},   # moeda volátil
    "JPY": {"spread_base": 0.028, "custo_base": 20.0},
}

# Segmentos de cliente e ticket médio (em BRL)
SEGMENTOS = {
    "PF":        {"ticket_medio": 5_000,   "peso": 0.55},
    "PME":       {"ticket_medio": 50_000,  "peso": 0.35},
    "Corporate": {"ticket_medio": 500_000, "peso": 0.10},
}

# ----------------------------
# Funções auxiliares
# ----------------------------
def gerar_data_aleatoria() -> datetime:
    """Gera uma data aleatória dentro do período definido."""
    delta = DATA_FIM - DATA_INICIO
    dias = random.randint(0, delta.days)
    return DATA_INICIO + timedelta(days=dias)


def escolher_segmento() -> str:
    """Sorteia um segmento respeitando os pesos definidos."""
    segmentos = list(SEGMENTOS.keys())
    pesos = [SEGMENTOS[s]["peso"] for s in segmentos]
    return random.choices(segmentos, weights=pesos, k=1)[0]


def gerar_valor_brl(segmento: str) -> float:
    """Gera o valor da operação em BRL com variação em torno do ticket médio."""
    ticket = SEGMENTOS[segmento]["ticket_medio"]
    # variação de ±60% em torno do ticket médio, com distribuição log-normal
    valor = np.random.lognormal(mean=np.log(ticket), sigma=0.6)
    return round(float(valor), 2)


def gerar_taxa_mercado(moeda: str) -> float:
    """Simula a taxa de mercado (PTAX) da moeda, em BRL."""
    taxas_referencia = {
        "USD": 5.40, "EUR": 5.85, "GBP": 6.90, "ARS": 0.006, "JPY": 0.036,
    }
    base = taxas_referencia[moeda]
    variacao = np.random.normal(0, 0.02)  # ±2% de variação
    return round(base * (1 + variacao), 6)


def gerar_taxa_aplicada(moeda: str, taxa_mercado: float) -> float:
    """Aplica o spread da moeda sobre a taxa de mercado."""
    spread = MOEDAS[moeda]["spread_base"] * np.random.uniform(0.7, 1.5)
    return round(taxa_mercado * (1 + spread), 6)


def gerar_custo_operacional(moeda_destino: str, valor_brl: float) -> float:
    """Custo operacional = custo base da moeda + 0,1% do valor da operação."""
    custo_base = MOEDAS[moeda_destino]["custo_base"]
    custo_variavel = valor_brl * 0.001
    return round(custo_base + custo_variavel, 2)


# ----------------------------
# Geração da base
# ----------------------------
def gerar_base() -> pd.DataFrame:
    registros = []

    for i in range(1, QTD_OPERACOES + 1):
        segmento = escolher_segmento()
        moeda_destino = random.choices(
            list(MOEDAS.keys()),
            weights=[0.45, 0.25, 0.10, 0.10, 0.10],  # USD domina
            k=1,
        )[0]

        valor_brl = gerar_valor_brl(segmento)
        taxa_mercado = gerar_taxa_mercado(moeda_destino)
        taxa_aplicada = gerar_taxa_aplicada(moeda_destino, taxa_mercado)
        custo_operacional = gerar_custo_operacional(moeda_destino, valor_brl)

        registros.append({
            "id_operacao": f"OP{i:05d}",
            "data": gerar_data_aleatoria().strftime("%Y-%m-%d"),
            "cliente": fake.company() if segmento != "PF" else fake.name(),
            "segmento": segmento,
            "moeda_origem": "BRL",
            "moeda_destino": moeda_destino,
            "valor_brl": valor_brl,
            "taxa_mercado": taxa_mercado,
            "taxa_aplicada": taxa_aplicada,
            "custo_operacional": custo_operacional,
        })

    return pd.DataFrame(registros)


def main():
    print("🔄 Gerando base sintética de operações de câmbio...")
    df = gerar_base()

    # Garante que a pasta de saída existe
    output_path = Path("data/raw/operacoes.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"✅ Base gerada com sucesso: {len(df)} operações")
    print(f"📁 Salva em: {output_path}")
    print("\n👀 Prévia:")
    print(df.head())


if __name__ == "__main__":
    main()