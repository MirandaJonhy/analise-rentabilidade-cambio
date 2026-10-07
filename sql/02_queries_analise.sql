-- ============================================================
-- 02_queries_analise.sql
-- Queries de análise de rentabilidade das operações de câmbio.
-- Cada query responde uma pergunta de negócio.
-- ============================================================


-- ------------------------------------------------------------
-- 📊 QUERY 1: Spread médio e margem total por moeda
-- Pergunta: qual moeda gera mais margem?
-- ------------------------------------------------------------
SELECT
    moeda_destino,
    COUNT(*)                                              AS qtd_operacoes,
    ROUND(SUM(valor_brl), 2)                              AS volume_total_brl,
    ROUND(AVG((taxa_aplicada - taxa_mercado) / taxa_mercado) * 100, 3) AS spread_medio_pct,
    ROUND(SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_total_brl
FROM operacoes
GROUP BY moeda_destino
ORDER BY margem_total_brl DESC;


-- ------------------------------------------------------------
-- 📊 QUERY 2: Rentabilidade por segmento de cliente
-- Pergunta: qual segmento é mais rentável?
-- ------------------------------------------------------------
SELECT
    segmento,
    COUNT(*)                                 AS qtd_operacoes,
    ROUND(AVG(valor_brl), 2)                 AS ticket_medio_brl,
    ROUND(SUM(valor_brl), 2)                 AS volume_total_brl,
    ROUND(SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_total_brl,
    ROUND(AVG((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_media_brl
FROM operacoes
GROUP BY segmento
ORDER BY margem_total_brl DESC;


-- ------------------------------------------------------------
-- 📊 QUERY 3: Top 10 clientes por margem gerada
-- Pergunta: quem são os clientes mais rentáveis?
-- ------------------------------------------------------------
SELECT
    cliente,
    segmento,
    COUNT(*)                                 AS qtd_operacoes,
    ROUND(SUM(valor_brl), 2)                 AS volume_total_brl,
    ROUND(SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_total_brl
FROM operacoes
GROUP BY cliente, segmento
ORDER BY margem_total_brl DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 📊 QUERY 4: Volume e margem por corredor (par de moedas)
-- Pergunta: qual corredor movimenta mais volume?
-- ------------------------------------------------------------
SELECT
    moeda_origem || ' → ' || moeda_destino          AS corredor,
    COUNT(*)                                         AS qtd_operacoes,
    ROUND(SUM(valor_brl), 2)                         AS volume_total_brl,
    ROUND(AVG(valor_brl), 2)                         AS ticket_medio_brl,
    ROUND(SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_total_brl
FROM operacoes
GROUP BY moeda_origem, moeda_destino
ORDER BY volume_total_brl DESC;


-- ------------------------------------------------------------
-- 📊 QUERY 5: Evolução mensal de volume e margem
-- Pergunta: como a rentabilidade evolui no tempo?
-- ------------------------------------------------------------
SELECT
    strftime('%Y-%m', data)                  AS mes,
    COUNT(*)                                 AS qtd_operacoes,
    ROUND(SUM(valor_brl), 2)                 AS volume_total_brl,
    ROUND(SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_total_brl
FROM operacoes
GROUP BY mes
ORDER BY mes;


-- ------------------------------------------------------------
-- 📊 QUERY 6: Margem média por operação (visão executiva)
-- Pergunta: qual a margem média que a empresa tira por operação?
-- ------------------------------------------------------------
SELECT
    COUNT(*)                                                                  AS total_operacoes,
    ROUND(SUM(valor_brl), 2)                                                  AS volume_total_brl,
    ROUND(SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_total_brl,
    ROUND(AVG((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional), 2) AS margem_media_por_operacao,
    ROUND(
        SUM((taxa_aplicada - taxa_mercado) * (valor_brl / taxa_aplicada) - custo_operacional)
        / SUM(valor_brl) * 100, 3
    )                                                                         AS margem_pct_sobre_volume
FROM operacoes;