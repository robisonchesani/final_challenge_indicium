CREATE VIEW custos_convertidos AS

WITH mediana AS (
    SELECT AVG(cotacao_venda) AS valor_mediana
    FROM (
        SELECT cotacao_venda
        FROM cotacao_dolar
        ORDER BY cotacao_venda
        LIMIT 2 - (SELECT COUNT(*) FROM cotacao_dolar) % 2
        OFFSET (SELECT (COUNT(*) - 1) / 2 FROM cotacao_dolar)
    )
)

SELECT i.*,
       COALESCE(c.cotacao_venda, m.valor_mediana) AS cotacao_venda,
       ROUND(i.usd_price * COALESCE(c.cotacao_venda, m.valor_mediana) , 2) AS brl_price
FROM custos_importacao i
LEFT JOIN cotacao_dolar c ON i.start_date = c.data
CROSS JOIN mediana m
ORDER BY i.product_id, i.start_date;

WITH tb_custo_vigente AS (
    SELECT v.id AS id_venda,
            v.id_product,
            v.id_client,
            v.qtd,
            v.total AS receita,
            v.sale_date,
            c.brl_price AS custo_unitario,
            ROUND(v.qtd * c.brl_price, 2) AS custo_total,
            ROUND(v.total - (v.qtd * c.brl_price), 2) AS resultado
    FROM vendas v
    LEFT JOIN custos_convertidos c
    ON v.id_product = c.product_id
    AND DATE(c.start_date) = (
        SELECT MAX(DATE(c2.start_date))
        FROM custos_convertidos c2
        WHERE c2.product_id = v.id_product
        AND DATE(c2.start_date) <= DATE(v.sale_date)
    )
),

tb_transacoes_prejuizo AS (
    SELECT id_venda,
            id_product,
            id_client,
            qtd,
            receita,
            custo_unitario,
            custo_total,
            resultado
    FROM tb_custo_vigente
    WHERE resultado < 0
    ORDER BY resultado ASC
),

tb_perc_perda AS (
    SELECT
        id_product,
        ROUND(SUM(receita), 2) AS receita_total,
        ROUND(SUM(CASE WHEN resultado < 0 THEN ABS(resultado)
                       ELSE 0 END), 2) AS prejuizo_total,
        ROUND(SUM(CASE WHEN resultado < 0 THEN ABS(resultado)
                       ELSE 0 END) / NULLIF(SUM(receita), 0) * 100, 2) AS percentual_perda
    FROM tb_custo_vigente
    GROUP BY id_product
    ORDER BY percentual_perda DESC
),

tb_prejuizo_total AS (
    SELECT p.actual_category,
            SUM(pp.prejuizo_total) AS prejuizo_total
    FROM produtos p
    LEFT JOIN tb_perc_perda pp
    ON pp.id_product = p.id
    GROUP BY p.actual_category
    ORDER BY prejuizo_total DESC
)

SELECT * FROM tb_perc_perda;