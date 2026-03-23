WITH tb_faturamento AS (
    SELECT c.id,
            c.full_name,
            SUM(v.total) AS faturamento_total
    FROM clientes_crm c
    LEFT JOIN vendas v
    ON c.id = v.id_client
    GROUP BY c.id
    ORDER BY faturamento_total DESC
),

tb_transacoes AS (
    SELECT c.id,
            c.full_name,
            COUNT(v.id) AS transacoes
    FROM clientes_crm c
    LEFT JOIN vendas v
    ON c.id = v.id_client
    GROUP BY c.id
    ORDER BY transacoes DESC
),

tb_ticket_medio AS (
    SELECT f.id,
            f.full_name,
            ROUND((f.faturamento_total / t.transacoes), 2) AS ticket_medio
    FROM tb_faturamento f
    LEFT JOIN tb_transacoes t
    ON f.id = t.id
    GROUP BY f.id
    ORDER BY ticket_medio DESC
),

tb_categoria AS (
    SELECT c.id,
            c.full_name,
            COUNT(DISTINCT(p.actual_category)) AS n_categorias
    FROM clientes_crm c
    LEFT JOIN vendas v ON c.id = v.id_client
    LEFT JOIN produtos p ON v.id_product = p.id
    GROUP BY c.id
    ORDER BY n_categorias DESC
),

tb_elite AS (
    SELECT t.id,
            t.full_name,
            t.ticket_medio,
            c.n_categorias
    FROM tb_ticket_medio t
    LEFT JOIN tb_categoria c ON t.id = c.id
    GROUP BY t.id
    HAVING c.n_categorias >= 3
    ORDER BY t.ticket_medio DESC
    LIMIT 10
),

tb_categoria_dominante AS (
    SELECT p.actual_category,
            SUM(v.qtd) AS total_itens
    FROM vendas v
    LEFT JOIN produtos p
    ON v.id_product = p.id
    WHERE v.id_client IN (SELECT id FROM tb_elite)
    GROUP BY p.actual_category
    ORDER BY total_itens DESC
    LIMIT 1
)

SELECT * from tb_categoria_dominante;


-- VALIDANDO QUERY DA CATEGORIA --
-- query para conferir, cliente por cliente, se todos realmente compraram das 3 categorias
SELECT
    c.full_name,
    p.actual_category,
    COUNT(*) AS compras_na_categoria
FROM vendas v
LEFT JOIN clientes_crm c
ON c.id = v.id_client
LEFT JOIN produtos p
ON v.id_product = p.id
WHERE v.id_client = 31  -- trocar pelo id de um cliente específico
GROUP BY c.full_name, p.actual_category;

