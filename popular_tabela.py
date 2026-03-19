import pandas as pd
import sqlite3

# 1. Criar dados de exemplo (DataFrame Pandas)
data = {
    'Nome': ['Ana', 'Bruno', 'Carla'],
    'Idade': [25, 30, 22],
    'Cidade': ['São Paulo', 'Rio de Janeiro', 'Florianópolis']
}
df = pd.DataFrame(data)

# 2. Estabelecer conexão com o banco SQLite (o arquivo será criado se não existir)
conn = sqlite3.connect('exemplo.db')

# 3. Popular a tabela SQLite com os dados do DataFrame
# if_exists: 'replace' (cria/substitui), 'append' (adiciona), 'fail' (erro se existir)
# index=False: evita que o índice do pandas seja salvo como coluna
df.to_sql('usuarios', conn, if_exists='replace', index=False)

# 4. Verificar e fechar a conexão
print("Tabela populada com sucesso!")
conn.close()
