WITH RECURSIVE dim_datas AS (
    SELECT DATE((SELECT MIN(sale_date) FROM vendas)) AS data
    UNION ALL
    SELECT DATE(data, '+1 day')
    FROM dim_datas
    WHERE data < DATE((SELECT MAX(sale_date) FROM vendas))
),

tb_vendas_diarias AS (
    SELECT
        DATE(sale_date) AS data,
        SUM(total) AS total_dia
    FROM vendas
    GROUP BY DATE(sale_date)
),

tb_calendario AS (
    SELECT
        d.data,
        COALESCE(v.total_dia, 0) AS total_dia,
        CASE STRFTIME('%w', d.data)
            WHEN '0' THEN 'Domingo'
            WHEN '1' THEN 'Segunda-feira'
            WHEN '2' THEN 'Terça-feira'
            WHEN '3' THEN 'Quarta-feira'
            WHEN '4' THEN 'Quinta-feira'
            WHEN '5' THEN 'Sexta-feira'
            WHEN '6' THEN 'Sábado'
        END AS dia_semana,
        STRFTIME('%w', d.data) AS ordem_dia
    FROM dim_datas d
    LEFT JOIN tb_vendas_diarias v
    ON d.data = v.data
),

tb_vendas_dia_semana AS (
    SELECT dia_semana,
            COUNT(*) AS total_dias,
            ROUND(AVG(total_dia), 2) AS media_vendas,
            ROUND(SUM(total_dia), 2) AS faturamento_total
    FROM tb_calendario
    GROUP BY dia_semana, ordem_dia
    ORDER BY media_vendas DESC
)

SELECT * FROM tb_vendas_dia_semana;