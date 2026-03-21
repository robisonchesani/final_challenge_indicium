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
#%%

print(f"Total de valores duplicados: {vendas.duplicated().sum()}")
#%%
nulos = vendas[['total', 'qtd']].isnull().sum()

nao_positivos = (vendas[['total', 'qtd']] <= 0).sum()

print(f"Valores nulos em 'total' e 'qtd':\n",nulos)
print(f"Valores nulos em 'total' e 'qtd':\n",nao_positivos)

#%%
import matplotlib.pyplot as plt

vendas['total'].plot(kind='box')
plt.show()

#%%
Q1 = vendas['total'].quantile(0.25)
Q3 = vendas['total'].quantile(0.75)
IQR = Q3 - Q1

lim_inf = Q1 - 1.5 * IQR  # ← corrigido
lim_sup = Q3 + 1.5 * IQR  # ← corrigido

outliers = vendas[(vendas['total'] < lim_inf) | (vendas['total'] > lim_sup)]

print(f"Total de outliers: {len(outliers)}")
print(outliers)

#%%
print(f"% de outliers: {len(outliers)/len(vendas)*100:.1f}%")

acima = outliers[outliers['total'] > lim_sup]
abaixo = outliers[outliers['total'] < lim_inf]

print(f"Outliers acima do limite superior: {len(acima)}")
print(f"Outliers abaixo do limite inferior: {len(abaixo)}")
#%%
# Os 10 maiores valores
print(outliers.nlargest(10, 'total')[['id', 'id_client', 'id_product', 'qtd', 'total', 'sale_date']])

#%%
# Ao invés de média, use mediana para métricas de vendas
print(f"Média total:   R$ {vendas['total'].mean():.2f}")
print(f"Mediana total: R$ {vendas['total'].median():.2f}")

# A diferença entre os dois vai te dizer o quanto os outliers estão inflando a média

#%%
# Vamos visualizar isso de forma clara
print(f"Média: R$ {vendas['total'].mean():,.2f}")
print(f"Mediana: R$ {vendas['total'].median():,.2f}")
print(f"Diferença: R$ {vendas['total'].mean() - vendas['total'].median():,.2f}")
print(f"Média {vendas['total'].mean() / vendas['total'].median():.1f}x maior que a mediana")

# Qual percentual das vendas está abaixo da média?
abaixo_da_media = (vendas['total'] < vendas['total'].mean()).sum()
print(f"% de vendas abaixo da média: {abaixo_da_media/len(vendas)*100:.1f}%")
#%%
vendas.to_csv('vendas.csv', index=False, encoding="utf-8-sig")

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
#%%
produtos.to_csv('produtos.csv', index=False, encoding="utf-8-sig")
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
# QUESTÃO 5 #
#############
#%% 
with open('datasets/clientes_crm.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

clientes = pd.json_normalize(data)

clientes.head()
# %%
clientes.info()
# %%
import re

# Lista oficial de UFs para identificação segura
UFS_VALIDAS = {
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR','PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
}

def extrair_uf_cidade(texto):
    if pd.isna(texto):
        return pd.Series({"cidade": None, "uf": None})
    
    # Remove espaços extras e divide pelo separador (vírgula ou hífen)
    texto = str(texto).strip()
    partes = re.split(r"[,\-\/\|]", texto)
    partes = [p.strip() for p in partes if p.strip()]
    
    uf = None
    cidade = None
    
    for parte in partes:
        # Verifica se a parte é uma UF válida (exatamente 2 letras maiúsculas)
        if parte.upper() in UFS_VALIDAS:
            uf = parte.upper()
        else:
            cidade = parte.strip()
    
    return pd.Series({"cidade": cidade, "uf": uf})

# Aplicar no dataframe
clientes[["cidade", "uf"]] = clientes["location"].apply(extrair_uf_cidade)

# Checar resultados
print(clientes[["location", "cidade", "uf"]].head(20))

# Checar se sobrou algum NULL (não mapeado)
nao_mapeados = clientes[clientes["uf"].isna() | clientes["cidade"].isna()]
print(f"\nNão mapeados: {len(nao_mapeados)}")
print(nao_mapeados["location"])
# %%
clientes.head()
# %%
clientes['email'] = clientes['email'].str.replace('#', '@')
clientes.head()
# %%
clientes.rename(columns={'code': 'id'}, inplace=True)
clientes.head()
#%%
clientes.drop(columns='location', inplace=True)
# %%
clientes = clientes[['id', 'full_name', 'email', 'cidade', 'uf']]
# %%
clientes.head()
# %%
clientes.to_csv('clientes.csv', index=False, encoding="utf-8-sig")
# %%
