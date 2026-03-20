SELECT * FROM vendas_novo
LIMIT 5;

SELECT * FROM custos_convertidos
WHERE start_date LIKE "2023%" OR start_date LIKE "2024"
ORDER BY product_id, start_date
LIMIT 5;

WITH tb_vendas_lucro  AS (
    SELECT id_product,
           qtd,
           SUM(total) AS receita_total
    FROM vendas_novo
    GROUP BY id_product
),

tb_custos AS (
    SELECT product_id,
           product_name,
           SUM(brl_price) AS despesa_total
    FROM custos_convertidos
    GROUP BY product_id
),

tb_demonstrativo AS (
    SELECT v.id_product,
           c.product_name,
           v.receita_total,
           c.despesa_total,
           v.receita_total - c.despesa_total AS lucro_liquido
    FROM tb_vendas_lucro v
    LEFT JOIN tb_custos c
    ON v.id_product = c.product_id
)

SELECT * FROM tb_demonstrativo;







-- CREATE VIEW custos_convertidos AS

-- WITH mediana AS (
--     SELECT AVG(cotacao_venda) AS valor_mediana
--     FROM (
--         SELECT cotacao_venda
--         FROM cotacao_dolar
--         ORDER BY cotacao_venda
--         LIMIT 2 - (SELECT COUNT(*) FROM cotacao_dolar) % 2
--         OFFSET (SELECT (COUNT(*) - 1) / 2 FROM cotacao_dolar)
--     )
-- )

-- SELECT i.*,
--        COALESCE(c.cotacao_venda, m.valor_mediana) AS cotacao_venda,
--        ROUND(i.usd_price * COALESCE(c.cotacao_venda, m.valor_mediana) , 2) AS brl_price
-- FROM custos_importacao i
-- LEFT JOIN cotacao_dolar c ON i.start_date = c.data
-- CROSS JOIN mediana m
-- ORDER BY i.product_id, i.start_date;

