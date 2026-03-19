CREATE TABLE vendas_novo (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    Quantidade INTEGER,
    Valor_total DECIMAL(10, 2),
    Data_venda DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes_crm(id),
    FOREIGN KEY (id_produto) REFERENCES produtos_novo(id)
);

