#%%
import pandas as pd
import json
from dateutil.parser import parse
#%%
###############
# QUESTÃO 3.1 #
###############
# Carregar aquivos json
with open('custos_importacao.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df_custos = pd.json_normalize(
    data,
    record_path="historic_data",
    meta=["product_id", "product_name", "category"]
)
# Alterar 'start_date' para datetime
df_custos['start_date'] = df_custos['start_date'].apply(lambda x: parse(x) if pd.notnull(x) else None)
# Colocar as colunas na ordem que estão na tabela do banco de dados
df_custos = df_custos[['product_id', 'product_name', 'category', 'start_date', 'usd_price']]

df_custos.head()

#%%
df_custos.to_csv("custos_importacao.csv", index=False, encoding="utf-8-sig")

# %%
###############
# QUESTÃO 3.2 #
###############
# Total de linhas em 'df_custos'
print(len(df_custos))
# %%
