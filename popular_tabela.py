
# %%
import pandas as pd
import sqlite3
#%% 
### POPULANDO TABELA DE VENDAS ###

df_vendas = pd.read_csv('Questao_1/vendas.csv')

con = sqlite3.connect('vendas_23_24.db')

cursor = con.cursor()

colunas = ", ".join(df_vendas.columns)
placeholders = ", ".join(['?' for _ in df_vendas.columns])

sql = f"INSERT INTO vendas_novo ({colunas}) VALUES ({placeholders})"

cursor.executemany(sql, df_vendas.itertuples(index=False, name=None))

con.commit()
con.close()

print(f"{cursor.rowcount} linhas inseridas com sucesso!")
# %%

### POPULANDO TABELA DE CUSTOS DE IMPORTAÇÃO ###
df_custos = pd.read_csv('Questao_3/custos_importacao.csv')

con = sqlite3.connect('vendas_23_24.db')

cursor = con.cursor()

colunas = ", ".join(df_custos.columns)
placeholders = ", ".join(['?' for _ in df_custos.columns])

sql = f"INSERT INTO custos_importacao ({colunas}) VALUES ({placeholders})"

cursor.executemany(sql, df_custos.itertuples(index=False, name=None))

con.commit()
con.close()

print(f"{cursor.rowcount} linhas inseridas com sucesso!")

# %%
### POPULANDO TABELA DE CLIENTES ###

df_clientes = pd.read_csv('Questao_5/clientes.csv')

con = sqlite3.connect('vendas_23_24.db')

cursor = con.cursor()

colunas = ", ".join(df_clientes.columns)
placeholders = ", ".join(['?' for _ in df_clientes.columns])

sql = f"INSERT INTO clientes_crm ({colunas}) VALUES ({placeholders})"

cursor.executemany(sql, df_clientes.itertuples(index=False, name=None))

con.commit()
con.close()

print(f"{cursor.rowcount} linhas inseridas com sucesso!")
# %%
### POPULANDO TABELA DE PRODUTOS ###

df_produtos = pd.read_csv('Questao_2/produtos.csv')
# Alterar nome da coluna 'code' para 'id'
df_produtos.rename(columns={'code': 'id'}, inplace=True)
# Alterar ordem das colunas para ficar na ordem que estão na tabela do db
df_produtos = df_produtos[['id', 'name', 'price', 'actual_category']]

con = sqlite3.connect('vendas_23_24.db')

cursor = con.cursor()

colunas = ", ".join(df_produtos.columns)
placeholders = ", ".join(['?' for _ in df_produtos.columns])

sql = f"INSERT INTO produtos_novo ({colunas}) VALUES ({placeholders})"

cursor.executemany(sql, df_produtos.itertuples(index=False, name=None))

con.commit()
con.close()

print(f"{cursor.rowcount} linhas inseridas com sucesso!")

# %%
df_produtos.head()

# %%
