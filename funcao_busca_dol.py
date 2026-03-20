#%%
import requests
import pandas as pd
import sqlite3

def buscar_dolar(data_inicio, data_fim):
    url = (
        f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        f"CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
        f"?@dataInicial='{data_inicio}'&@dataFinalCotacao='{data_fim}'"
        f"&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"
    )
    response = requests.get(url)
    dados = response.json()['value']
    return pd.DataFrame(dados)

df_23 = buscar_dolar("01-01-2023", "12-31-2023")
df_24 = buscar_dolar("01-01-2024", "12-31-2024")

df_dolar = pd.concat([df_23, df_24], ignore_index=True)

df_dolar['dataHoraCotacao'] = pd.to_datetime(df_dolar["dataHoraCotacao"])
df_dolar['data'] = df_dolar['dataHoraCotacao'].dt.date

df_dolar = df_dolar.sort_values("dataHoraCotacao").groupby("data").mean().reset_index()

df_dolar = df_dolar.rename(columns={
    "cotacaoCompra": "cotacao_compra",
    "cotacaoVenda": "cotacao_venda"
})[["data", "cotacao_compra", "cotacao_venda"]]

print(df_dolar.head())
print(f"Total de dias: {len(df_dolar)}")

# %%
### POPULANDO A TABELA DE COTAÇÃO ###

con = sqlite3.connect('vendas_23_24.db')
cursor = con.cursor()

sql = "INSERT OR IGNORE INTO cotacao_dolar (data, cotacao_compra, cotacao_venda) VALUES (?, ?, ?)"

cursor.executemany(sql, df_dolar.itertuples(index=False, name=None))
con.commit()
con.close()

print("Cotações inseridas com sucesso!")
# %%
