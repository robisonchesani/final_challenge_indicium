
"""
O gráfico foi limitado aos 10 produtos com maior prejuízo total,
pois as informações de nome e valor de prejuízo de cada produto
ficam incompreensíveis ao mostrarmos todos.
"""

#%%
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Busca os dados do banco
query = """
WITH tb_custo_vigente AS (
    SELECT
        v.id AS id_venda,
        v.id_product,
        v.id_client,
        v.qtd,
        v.total AS receita,
        v.sale_date,
        c.product_name,
        c.brl_price AS custo_unitario,
        ROUND(v.qtd * c.brl_price, 2) AS custo_total,
        ROUND(v.total - (v.qtd * c.brl_price), 2) AS resultado
    FROM vendas_novo v
    LEFT JOIN custos_convertidos c
        ON v.id_product = c.product_id
        AND DATE(c.start_date) = (
            SELECT MAX(DATE(c2.start_date))
            FROM custos_convertidos c2
            WHERE c2.product_id = v.id_product
            AND DATE(c2.start_date) <= DATE(v.sale_date)
        )
)

SELECT
    id_product,
    product_name,
    ROUND(SUM(CASE WHEN resultado < 0 THEN ABS(resultado)
                   ELSE 0 END), 2) AS prejuizo_total
FROM tb_custo_vigente
GROUP BY id_product
HAVING prejuizo_total > 0
ORDER BY prejuizo_total DESC
LIMIT 10;
"""

with sqlite3.connect("vendas_23_24.db") as con:
    df_prejuizo = pd.read_sql(query, con)

# Gráfico
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.barh(
    df_prejuizo["product_name"],
    df_prejuizo["prejuizo_total"],
    color="tomato",
    edgecolor="darkred",
    linewidth=0.5
)

# Adiciona os valores nas barras
for bar, valor in zip(bars, df_prejuizo["prejuizo_total"]):
    ax.text(
        bar.get_width() * 1.01,
        bar.get_y() + bar.get_height() / 2,
        f"R$ {valor:,.2f}",
        va="center",
        fontsize=9
    )

ax.set_title("Prejuízo Total por Produto (10 maiores)", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Prejuízo Total (BRL em milhares)")
ax.set_ylabel("")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"R$ {x/1000000:,.0f}M"))
ax.invert_yaxis()
plt.tight_layout()
plt.show()
# %%
