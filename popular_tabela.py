# import pandas as pd
# import sqlite3

# # 1. Criar dados de exemplo (DataFrame Pandas)
# data = {
#     'Nome': ['Ana', 'Bruno', 'Carla'],
#     'Idade': [25, 30, 22],
#     'Cidade': ['São Paulo', 'Rio de Janeiro', 'Florianópolis']
# }
# df = pd.DataFrame(data)

# # 2. Estabelecer conexão com o banco SQLite (o arquivo será criado se não existir)
# conn = sqlite3.connect('exemplo.db')

# # 3. Popular a tabela SQLite com os dados do DataFrame
# # if_exists: 'replace' (cria/substitui), 'append' (adiciona), 'fail' (erro se existir)
# # index=False: evita que o índice do pandas seja salvo como coluna
# df.to_sql('usuarios', conn, if_exists='append', index=False)

# # 4. Verificar e fechar a conexão
# print("Tabela populada com sucesso!")
# conn.close()


# %%

import pandas as pd

import sqlite3
#%% 
### POPULANDO TABELA DE VENDAS ###

df_vendas = pd.read_csv('vendas.csv')

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
df_custos = pd.read_csv('custos_importacao.csv')

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

df_clientes = pd.read_csv('clientes.csv')

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

df_produtos = pd.read_csv('produtos.csv')

df_produtos.rename(columns={'code': 'id'}, inplace=True)

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
