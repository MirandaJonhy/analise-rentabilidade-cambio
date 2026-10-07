"""
analise.py
-----------
Lê a base bruta de operações de câmbio, calcula a margem por operação
e gera tabelas agregadas prontas para alimentar o dashboard.

Entrada:
- data/raw/operacoes.csv

Saída:
- data/processed/operacoes_com_margem.csv   (base detalhada, operação a operação)
- data/processed/analise_rentabilidade.csv  (tabela consolidada por dimensão)
"""

from pathlib import Path

import pandas as pd

# ----------------------------
# Caminhos do projeto
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "raw" / "operacoes.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DETALHADO = OUTPUT_DIR / "operacoes_com_margem.csv"
OUTPUT_AGREGADO = OUTPUT_DIR / "analise_rentabilidade.csv"


# ----------------------------
# Cálculo da margem
# ----------------------------
def calcular_margem(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula as métricas financeiras por operação:
    - spread_pct: spread cobrado em relação à taxa de mercado
    - receita_brl: receita bruta da operação em BRL
    - margem_brl: margem líquida (receita - custo operacional)
    """
    df = df.copy()

    # Spread percentual (ex: 0.025 = 2,5%)
    df["spread_pct"] = (df["taxa_aplicada"] - df["taxa_mercado"]) / df["taxa_mercado"]

    # Quantidade de moeda estrangeira da operação
    df["valor_moeda_estrangeira"] = df["valor_brl"] / df["taxa_aplicada"]

    # Receita bruta = spread × quantidade de moeda estrangeira
    df["receita_brl"] = df["spread_pct"] * df["valor_brl"]

    # Margem líquida = receita - custo operacional
    df["margem_brl"] = df["receita_brl"] - df["custo_operacional"]

    # Arredondamentos para deixar o CSV limpo
    for col in ["spread_pct", "valor_moeda_estrangeira", "receita_brl", "margem_brl"]:
        df[col] = df[col].round(4)

    return df


# ----------------------------
# Agregações
# ----------------------------
def agrega_por(df: pd.DataFrame, dimensao: str) -> pd.DataFrame:
    """Gera uma tabela agregada por uma dimensão (moeda, segmento, etc.)."""
    agregado = (
        df.groupby(dimensao)
        .agg(
            qtd_operacoes=("id_operacao", "count"),
            volume_total_brl=("valor_brl", "sum"),
            ticket_medio_brl=("valor_brl", "mean"),
            receita_total_brl=("receita_brl", "sum"),
            custo_total_brl=("custo_operacional", "sum"),
            margem_total_brl=("margem_brl", "sum"),
            margem_media_brl=("margem_brl", "mean"),
            spread_medio_pct=("spread_pct", "mean"),
        )
        .reset_index()
    )

    # Margem % sobre o volume
    agregado["margem_pct_sobre_volume"] = (
        agregado["margem_total_brl"] / agregado["volume_total_brl"] * 100
    ).round(3)

    # Arredondamentos
    for col in [
        "volume_total_brl", "ticket_medio_brl", "receita_total_brl",
        "custo_total_brl", "margem_total_brl", "margem_media_brl",
    ]:
        agregado[col] = agregado[col].round(2)

    agregado["spread_medio_pct"] = (agregado["spread_medio_pct"] * 100).round(3)
    agregado["dimensao"] = dimensao

    return agregado


def agrega_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Gera a evolução mensal de volume e margem."""
    df = df.copy()
    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.strftime("%Y-%m")

    agregado = (
        df.groupby("mes")
        .agg(
            qtd_operacoes=("id_operacao", "count"),
            volume_total_brl=("valor_brl", "sum"),
            margem_total_brl=("margem_brl", "sum"),
        )
        .reset_index()
    )

    agregado["volume_total_brl"] = agregado["volume_total_brl"].round(2)
    agregado["margem_total_brl"] = agregado["margem_total_brl"].round(2)
    agregado["dimensao"] = "mes"

    return agregado


# ----------------------------
# Execução principal
# ----------------------------
def main():
    print("🚀 Iniciando análise de rentabilidade...\n")

    # 1. Lê a base bruta
    df = pd.read_csv(INPUT_PATH)
    print(f"📥 {len(df)} operações carregadas de {INPUT_PATH.name}")

    # 2. Calcula margem por operação
    df = calcular_margem(df)
    print("🧮 Margem calculada por operação")

    # 3. Gera as agregações
    agregados = {
        "moeda":    agrega_por(df, "moeda_destino"),
        "segmento": agrega_por(df, "segmento"),
        "cliente":  agrega_por(df, "cliente"),
        "mes":      agrega_por_mes(df),
    }
    print(f"📊 {len(agregados)} agregações geradas: {', '.join(agregados.keys())}")

    # 4. Salva a base detalhada
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DETALHADO, index=False)
    print(f"💾 Base detalhada salva em: {OUTPUT_DETALHADO.relative_to(BASE_DIR)}")

    # 5. Salva cada agregação como uma "aba" no CSV consolidado
    #    (usamos um separador especial pra simular múltiplas tabelas num arquivo)
    with open(OUTPUT_AGREGADO, "w", encoding="utf-8") as f:
        for nome, tabela in agregados.items():
            f.write(f"### {nome.upper()}\n")
            tabela.to_csv(f, index=False)
            f.write("\n")

    print(f"💾 Agregações salvas em: {OUTPUT_AGREGADO.relative_to(BASE_DIR)}")

    # 6. Resumo executivo no terminal
    print("\n" + "=" * 60)
    print("📌 RESUMO EXECUTIVO")
    print("=" * 60)
    print(f"Volume total transacionado: R$ {df['valor_brl'].sum():,.2f}")
    print(f"Margem total:               R$ {df['margem_brl'].sum():,.2f}")
    print(f"Margem média por operação:  R$ {df['margem_brl'].mean():,.2f}")
    print(f"Margem % sobre volume:      {df['margem_brl'].sum() / df['valor_brl'].sum() * 100:.2f}%")
    print(f"Moeda mais rentável:        {agregados['moeda'].sort_values('margem_total_brl', ascending=False).iloc[0]['moeda_destino']}")
    print(f"Segmento mais rentável:     {agregados['segmento'].sort_values('margem_total_brl', ascending=False).iloc[0]['segmento']}")
    print("=" * 60)


if __name__ == "__main__":
    main()