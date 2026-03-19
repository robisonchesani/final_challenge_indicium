#%%
import pandas as pd

produtos = pd.read_csv('datasets/produtos_raw.csv')
vendas = pd.read_csv('datasets/vendas_2023_2024.csv')

# %%
###############
# QUESTÃO 1.3 #
###############

vendas.info()
# %%
vendas.head()
# %%
from dateutil.parser import parse

vendas['sale_date'] = vendas['sale_date'].apply(lambda x: parse(x) if pd.notnull(x) else None)

vendas.info()

#%%
vendas.shape

vendas.duplicated().sum()
#%%
tem_negativo = (vendas['total'] < 0).any()
print(tem_negativo)
#%%
import matplotlib.pyplot as plt

vendas['total'].plot(kind='box')
plt.show()

#%%
Q1 = vendas['total'].quantile(0.25)
Q3 = vendas['total'].quantile(0.75)
IQR = Q3 - Q1

lim_sup = Q1 - 1.5 * IQR
lim_inf = Q3 - 1.5 * IQR

outliers = vendas[(vendas['total'] < lim_inf) | (vendas['total'] > lim_sup)]

print(outliers)
#%%
#############
# QUESTÃO 2 #
#############

produtos.info()

#%%
produtos['price'] = produtos['price'].str.replace('R$ ', "", regex=False).astype(float)


#%%
produtos['actual_category'].unique()

#%%
import unicodedata
from difflib import get_close_matches

# Normaliza removendo espaços internos, acentos e caixa
def normalizar(texto):
    texto = str(texto).lower().replace(" ", "")
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto

categorias = ["eletrônicos", "propulsão", "ancoragem"]
categorias_norm = {normalizar(c): c for c in categorias}

# Mapeamento manual para abreviações que não têm similaridade suficiente
mapa_manual = {
    normalizar("Prop"): "propulsão",
}

def padronizar_categoria(valor):
    norm = normalizar(valor)
    
    # 1. Tenta mapa manual primeiro
    if norm in mapa_manual:
        return mapa_manual[norm]
    
    # 2. Tenta match exato após normalização
    if norm in categorias_norm:
        return categorias_norm[norm]
    
    # 3. Tenta similaridade textual
    match = get_close_matches(norm, categorias_norm.keys(), n=1, cutoff=0.6)
    if match:
        return categorias_norm[match[0]]
    
    return None  # Sinaliza o que não foi mapeado para revisão

# Aplicar na coluna
produtos['actual_category'] = produtos['actual_category'].apply(padronizar_categoria)

# Checar se sobrou algum None (não mapeado)
nao_mapeados = produtos[produtos['actual_category'].isna()]
print(f"Não mapeados: {len(nao_mapeados)}")
print(nao_mapeados)
#%%
produtos['actual_category'].unique()

#%%
print(produtos.duplicated().sum())
#%%
produtos = produtos.drop_duplicates()
#%%
produtos.shape

# %%
###############
# QUESTÃO 3.1 #
###############

import json

with open('datasets/custos_importacao.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df_custos = pd.json_normalize(
    data,
    record_path="historic_data",
    meta=["product_id", "product_name", "category"]
)

df_custos['start_date'] = df_custos['start_date'].apply(lambda x: parse(x) if pd.notnull(x) else None)

df_custos.head()

#%%
df_custos.info()

#%%
df_custos = df_custos[['product_id', 'product_name', 'category', 'start_date', 'usd_price']]

df_custos.head()

#%%
df_custos.to_csv("custos_importacao.csv", index=False, encoding="utf-8-sig")

# %%
###############
# QUESTÃO 3.1 #
###############

print(len(df_custos))
# %%
#############
# QUESTÃO 4 #
#############
#%% 
# with open('datasets/clientes_crm.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# clientes = pd.json_normalize(data)

# clientes.head()
# # %%
# clientes.info()