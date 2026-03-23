#%%
import pandas as pd
import unicodedata
from difflib import get_close_matches
#%%
produtos = pd.read_csv('produtos_raw.csv')
produtos.info()

#%%
# Remover caracteres e converter para 'float' a coluna 'price'
produtos['price'] = produtos['price'].str.replace('R$ ', "", regex=False).astype(float)

#%%
# Verificar quantos nomes de categorias temos escritos de forma diferente
produtos['actual_category'].unique()

#%%
# Normalizar removendo espaços internos, acentos e caixa
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
    
    # Tenta mapa manual primeiro
    if norm in mapa_manual:
        return mapa_manual[norm]
    
    # Tenta match exato após normalização
    if norm in categorias_norm:
        return categorias_norm[norm]
    
    # Tenta similaridade textual
    match = get_close_matches(norm, categorias_norm.keys(), n=1, cutoff=0.6)
    if match:
        return categorias_norm[match[0]]
    
    return None  # Sinaliza o que não foi mapeado para revisão

# Aplicar na coluna
produtos['actual_category'] = produtos['actual_category'].apply(padronizar_categoria)

# Checar se sobrou algum não mapeado
nao_mapeados = produtos[produtos['actual_category'].isna()]
print(f"Não mapeados: {len(nao_mapeados)}")
print(nao_mapeados)
#%%
# Verificar se as categorias estão corrigidas
produtos['actual_category'].unique()

#%%
# Calcular total de duplicados
print(produtos.duplicated().sum())
#%%
# Remover duplicados
produtos = produtos.drop_duplicates()
#%%
produtos.shape
#%%
produtos.to_csv('produtos.csv', index=False, encoding="utf-8-sig")