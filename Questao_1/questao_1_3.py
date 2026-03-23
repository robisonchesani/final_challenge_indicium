#%%
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.parser import parse
#%%
# Carregar arquivo csv
vendas = pd.read_csv('vendas_2023_2024.csv')

vendas.info()
# %%
vendas.head()
# %%
# Alterar tipo de 'sale_date' para datetime
vendas['sale_date'] = vendas['sale_date'].apply(lambda x: parse(x) if pd.notnull(x) else None)

#%%
vendas.shape
#%%
# Verificar a existência de duplicados
print(f"Total de valores duplicados: {vendas.duplicated().sum()}")
#%%
# Verificar a existência de nulos, valores 0 e negativos nas colunas de 'qtd' e 'total'
nulos = vendas[['total', 'qtd']].isnull().sum()

nao_positivos = (vendas[['total', 'qtd']] <= 0).sum()

print(f"Valores nulos em 'total' e 'qtd':\n",nulos)
print(f"Valores nulos em 'total' e 'qtd':\n",nao_positivos)

#%%
# Plotar gráfico boxplot para verificar existência de possíveis outliers
vendas['total'].plot(kind='box')
plt.show()

#%%
# Identificar possíveis outliers 
Q1 = vendas['total'].quantile(0.25)
Q3 = vendas['total'].quantile(0.75)
IQR = Q3 - Q1

lim_inf = Q1 - 1.5 * IQR  # ← corrigido
lim_sup = Q3 + 1.5 * IQR  # ← corrigido

outliers = vendas[(vendas['total'] < lim_inf) | (vendas['total'] > lim_sup)]

print(f"Total de outliers: {len(outliers)}")
print(outliers)

#%%
# Verificar posição dos possíveis outliers (acima ou abaixo dos limites)
print(f"% de outliers: {len(outliers)/len(vendas)*100:.1f}%")

acima = outliers[outliers['total'] > lim_sup]
abaixo = outliers[outliers['total'] < lim_inf]

print(f"Outliers acima do limite superior: {len(acima)}")
print(f"Outliers abaixo do limite inferior: {len(abaixo)}")
#%%
# 10 maiores valores
print(outliers.nlargest(10, 'total')[['id', 'id_client', 'id_product', 'qtd', 'total', 'sale_date']])

#%%
# Comparar média e mediana para verificar o quanto os outliers estão inflando a média
print(f"Média: R$ {vendas['total'].mean():.2f}")
print(f"Mediana: R$ {vendas['total'].median():.2f}")

#%%
# Sumarizando as informações
print(f"Média: R$ {vendas['total'].mean():,.2f}")
print(f"Mediana: R$ {vendas['total'].median():,.2f}")
print(f"Diferença: R$ {vendas['total'].mean() - vendas['total'].median():,.2f}")
print(f"Média {vendas['total'].mean() / vendas['total'].median():.1f}x maior que a mediana")

abaixo_da_media = (vendas['total'] < vendas['total'].mean()).sum()
print(f"% de vendas abaixo da média: {abaixo_da_media/len(vendas)*100:.1f}%")
#%%
vendas.to_csv('vendas.csv', index=False, encoding="utf-8-sig")