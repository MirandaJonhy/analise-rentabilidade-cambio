"""
carregar_sqlite.py
-------------------
Carrega a base de operações de câmbio (CSV) em um banco SQLite,
executa o schema e roda as queries de análise, exibindo os resultados.

Entradas:
- data/raw/operacoes.csv
- sql/01_criar_tabelas.sql
- sql/02_queries_analise.sql

Saída:
- data/cambio.db (banco SQLite)
"""

import sqlite3
from pathlib import Path

import pandas as pd

# ----------------------------
# Caminhos do projeto
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "raw" / "operacoes.csv"
DB_PATH = BASE_DIR / "data" / "cambio.db"
SCHEMA_PATH = BASE_DIR / "sql" / "01_criar_tabelas.sql"
QUERIES_PATH = BASE_DIR / "sql" / "02_queries_analise.sql"


# ----------------------------
# Funções auxiliares
# ----------------------------
def ler_sql(caminho: Path) -> str:
    """Lê o conteúdo de um arquivo .sql."""
    return caminho.read_text(encoding="utf-8")


def dividir_queries(sql: str) -> list[str]:
    """
    Divide um arquivo .sql em queries individuais,
    ignorando linhas de comentário (--).
    """
    linhas_limpas = [
        linha for linha in sql.splitlines()
        if not linha.strip().startswith("--")
    ]
    sql_limpo = "\n".join(linhas_limpas)

    return [q.strip() for q in sql_limpo.split(";") if q.strip()]


def criar_banco() -> sqlite3.Connection:
    """Cria o banco, executa o schema e insere os dados do CSV."""
    # Remove o banco antigo, se existir (pra rodar do zero toda vez)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)

    # 1. Executa o schema
    print("🏗️  Criando tabela e índices...")
    schema_sql = ler_sql(SCHEMA_PATH)
    conn.executescript(schema_sql)

    # 2. Carrega o CSV e insere na tabela
    print("📥 Carregando dados do CSV...")
    df = pd.read_csv(CSV_PATH)
    df.to_sql("operacoes", conn, if_exists="append", index=False)
    print(f"✅ {len(df)} operações inseridas na tabela 'operacoes'.\n")

    return conn


def rodar_queries(conn: sqlite3.Connection) -> None:
    """Executa cada query de análise e exibe o resultado formatado."""
    queries = dividir_queries(ler_sql(QUERIES_PATH))

    for i, query in enumerate(queries, start=1):
        print("=" * 70)
        print(f"📊 QUERY {i}")
        print("=" * 70)

        try:
            df_resultado = pd.read_sql_query(query, conn)
            print(df_resultado.to_string(index=False))
        except Exception as e:
            print(f"❌ Erro ao executar a query: {e}")

        print()


def main():
    print("🚀 Iniciando carga do banco de câmbio...\n")
    conn = criar_banco()

    try:
        rodar_queries(conn)
    finally:
        conn.close()
        print(f"💾 Banco salvo em: {DB_PATH}")


if __name__ == "__main__":
    main()