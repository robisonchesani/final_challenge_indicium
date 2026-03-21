#%%
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# %%
# CARREGAMENTO E TRATAMENTO PRÉVIO

vendas = pd.read_csv('vendas.csv')
produtos = pd.read_csv('produtos.csv')
# %%
produtos.head()
# %%
produtos.rename(columns={'code': 'id'}, inplace=True)

produtos = produtos[['id', 'name', 'price', 'actual_category']]
# %%
# MATRIZ DE INTERAÇÃO BINÁRIA ENTRE USUÁRIO E PRODUTO

vendas['comprou'] = 1

matriz_interacao = vendas.pivot_table(
    index='id_client',
    columns='id_product',
    values='comprou',
    aggfunc='max',
    fill_value=0
)

print(f"Dimensão da matriz: {matriz_interacao.shape}")
print(f"Clientes: {matriz_interacao.shape[0]} | Produtos: {matriz_interacao.shape[1]}")
# %%
# SIMILARIDADE DE COSSENO
# Transpor a matriz para que cada produto seja representado pelo
# vetor de clientes que compraram

matriz_T = matriz_interacao.T

similar = cosine_similarity(matriz_T)

df_similar = pd.DataFrame(
    similar,
    index=matriz_T.index,
    columns=matriz_T.index
)

print(f"\nMatriz de similaridade: {df_similar.shape}")
# %%
# RANKING DOS 5 MAIS SILIMARES
# Similaridade com o produto “GPS Garmin Vortex Maré Drift” (id_product = 27)

produto_id = 27

ranking = (
    df_similar[produto_id].drop(produto_id).sort_values(ascending=False)
    .head(5).reset_index()
)

ranking.columns = ['id_product', 'similaridade']
# %%
# MOSTRAR OS NOMES DOS PRODUTOS
# Cruzar com a tabela de produtos para mostrar nome e categoria

ranking = ranking.merge(
    produtos[['id', 'name', 'actual_category']],
    left_on='id_product',
    right_on='id',
    how='left'
)

nome_ref = produtos.loc[produtos['id'] == produto_id, 'name'].values[0]
# %%
# RESULTADO FINAL

print(f"\n{'='*55}")
print(f"Produto de referência: [{produto_id}] {nome_ref}")
print(f"{'='*55}")
print(f"{'#':<4} {'Produto':<35} {'Categoria':<15} {'Similaridade'}")
print(f"{'-'*55}")

for i, row in ranking.iterrows():
    print(f"{i+1:<4} {row['name']:<35} {row['actual_category']:<15} {row['similaridade']:.4f}")

print(f"{'='*55}")
# %%
