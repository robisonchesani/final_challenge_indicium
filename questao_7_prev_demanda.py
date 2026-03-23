#%%
import pandas as pd
from sklearn.metrics import mean_absolute_error
# %%
# GERAR DATAFRAME

df_geral = pd.read_csv('Questao_1/vendas.csv')

# filtrando somente o produto 'Motor de Popa Yamaha Evo Dash 155HP' (product_id = 54)

df = (df_geral[df_geral["id_product"] == 54].groupby("sale_date")["qtd"].sum().reset_index())

df.head()
#%%
df.info()
#%%
# CONVERTER 'SALE_DATE' PARA DATETIME

df["sale_date"] = pd.to_datetime(df["sale_date"])

#%%
# GERAR CALENDARIO COMPLETO
# garantir que dias sem venda apareçam com valor 0

data_min = df["sale_date"].min()
data_max = df["sale_date"].max()

calendario = pd.DataFrame({
    "sale_date": pd.date_range(start=data_min, end=data_max, freq="D")
})

df = calendario.merge(df, on="sale_date", how="left").fillna(0)

# %%
df.head()

# %%
# SEPARAÇÃO DE TREINO E TESTE

# definir ponto de corte para evitar data leakage
corte = '2023-12-31'

df_train = df[df["sale_date"] <= corte].copy()
df_test = df[(df["sale_date"] >= '2024-01-01') &
             (df["sale_date"] <= '2024-01-31')]
# %%
# CÁLCULO DO BASELINE (média móvel)

df_completo = df[df["sale_date"] <= '2024-01-31'].copy()

df_completo["media_movel_7d"] = (
    df_completo["qtd"].shift(1).rolling(window=7, min_periods=1).mean().round()
)

df_test = df_completo[
    (df_completo["sale_date"] >= '2024-01-01') &
    (df_completo["sale_date"] <= '2024-01-31')
].copy()
# %%
# AVALIAÇÃO COM MAE (média de unidades erradas por dia)

mae = mean_absolute_error(
    df_test["qtd"],
    df_test["media_movel_7d"]
)

print(f"MAE do baseline (Média Móvel 7 dias):")
print(f"{mae:.2f} unidades/dia")
# %%
# RESULTADO (previsões diárias para janeiro de 2024)

df_resultado = df_test[["sale_date", "qtd", "media_movel_7d"]].copy()

df_resultado.columns = ["data", "vendas_reais", "previsao"]

df_resultado["erro_absoluto"] = (
    df_resultado["vendas_reais"] - df_resultado["previsao"]
).abs()

print("Previsão diária — Janeiro 2024:")
print(df_resultado)
# %%
print(df_resultado['previsao'].sum())
# %%
print(df_resultado['vendas_reais'].sum())

# %%
# SOMA TOTAL DAS PREVISÕES DE VENDA (primieira semana de janeiro)
semana_1 = df_resultado[
    (df_resultado["data"] >= "2024-01-01") &
    (df_resultado["data"] <= "2024-01-07")
]

print(semana_1['previsao'].sum())
# %%
