#%%
import pandas as pd
import json
#%%
# Abrir arquivo .json
with open('clientes_crm.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

clientes = pd.json_normalize(data)

clientes.head()
# %%
clientes.info()
# %%
import re

# Lista oficial de UFs para identificação
UFS_VALIDAS = {
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR','PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
}

# Função para separar cidade e estado (tratar coluna 'location')
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

# Checar se sobrou algum não mapeado
nao_mapeados = clientes[clientes["uf"].isna() | clientes["cidade"].isna()]
print(f"\nNão mapeados: {len(nao_mapeados)}")
print(nao_mapeados["location"])
# %%
# Trocar '#' por '@' nos emails
clientes['email'] = clientes['email'].str.replace('#', '@')

# Alterar 'code' para 'id' para popular a tabela no banco de dados
clientes.rename(columns={'code': 'id'}, inplace=True)

# Remover coluna 'location' (já temos duas novas com 'cidade' e 'uf')
clientes.drop(columns='location', inplace=True)

# Colocar as colunas na ordem que estão na tabela
clientes = clientes[['id', 'full_name', 'email', 'cidade', 'uf']]

clientes.head()
# %%
clientes.to_csv('clientes.csv', index=False, encoding="utf-8-sig")