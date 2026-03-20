-- CREATE TABLE vendas_novo (
--     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     id_client INTEGER NOT NULL,
--     id_product INTEGER NOT NULL,
--     qtd INTEGER,
--     total DECIMAL(10, 2),
--     sale_date DATE,
--     FOREIGN KEY (id_client) REFERENCES clientes_crm(id),
--     FOREIGN KEY (id_product) REFERENCES produtos_novo(id)
-- );

-- CREATE TABLE custos_importacao (
--     product_id INTEGER NOT NULL,
--     product_name VARCHAR(150),
--     category VARCHAR(50),
--     start_date DATE,
--     usd_price DECIMAL(10, 2),
--     FOREIGN KEY (product_id) REFERENCES produtos_novo(id)
-- );

CREATE TABLE cotacao_dolar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL UNIQUE,
    cotacao_compra DECIMAL(2, 5),
    cotacao_venda DECIMAL(2, 5)
);