SELECT COUNT(*) AS total_linhas FROM vendas;

SELECT COUNT(*) AS total_colunas
FROM pragma_table_info('vendas');

SELECT SUBSTR(MIN(sale_date), 1, 10) AS data_minima,
       SUBSTR(MAX(sale_date), 1, 10) AS data_maxima
FROM vendas;

SELECT ROUND(MAX(total), 2) AS valor_maximo
FROM vendas;

SELECT ROUND(MIN(total), 2) AS valor_minimo
FROM vendas;

SELECT ROUND(AVG(total), 2) AS valor_medio
FROM vendas;