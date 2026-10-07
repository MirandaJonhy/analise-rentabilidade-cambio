-- ============================================================
-- 01_criar_tabelas.sql
-- Define o schema da tabela principal de operações de câmbio.
-- Compatível com SQLite, PostgreSQL e BigQuery (com pequenos ajustes).
-- ============================================================

DROP TABLE IF EXISTS operacoes;

CREATE TABLE operacoes (
    id_operacao       VARCHAR(10)   PRIMARY KEY,
    data              DATE          NOT NULL,
    cliente           VARCHAR(150)  NOT NULL,
    segmento          VARCHAR(20)   NOT NULL,   -- PF | PME | Corporate
    moeda_origem      VARCHAR(3)    NOT NULL,   -- sempre BRL neste projeto
    moeda_destino     VARCHAR(3)    NOT NULL,   -- USD | EUR | GBP | ARS | JPY
    valor_brl         DECIMAL(18,2) NOT NULL,
    taxa_mercado      DECIMAL(18,6) NOT NULL,   -- taxa de referência (PTAX)
    taxa_aplicada     DECIMAL(18,6) NOT NULL,   -- taxa cobrada do cliente
    custo_operacional DECIMAL(18,2) NOT NULL
);

-- Índices para acelerar as análises mais comuns
CREATE INDEX idx_operacoes_data      ON operacoes (data);
CREATE INDEX idx_operacoes_segmento  ON operacoes (segmento);
CREATE INDEX idx_operacoes_moeda     ON operacoes (moeda_destino);