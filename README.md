# Projeto — Análise de Vendas, Previsão de Demanda e Recomendação de Produtos

## ⚠️ Pré-requisitos — Leia antes de começar

### 1. Instalar o SQLite

O SQLite deve estar instalado na máquina antes de qualquer execução.

**Windows:**
Baixe o binário em https://www.sqlite.org/download.html e adicione ao PATH.

**Linux/macOS:**
```bash
# Linux
sudo apt-get install sqlite3

# macOS
brew install sqlite3
```

Verifique a instalação:
```bash
sqlite3 --version
```

---

### 2. Criar o banco de dados e as tabelas

As tabelas devem ser criadas **antes** de rodar qualquer script Python de inserção de dados. Execute o arquvo "criacao_tabelas.sql"

## Instalação do ambiente Python

### 1. Clone o repositório e acesse a pasta

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Ordem de execução recomendada

Siga esta sequência para garantir que os dados estejam disponíveis antes de cada etapa:

```
1. Criar as tabelas no SQLite          (conforme instruções acima)
2. Tratar e padronizar os CSVs         (limpeza de categorias, localidades)
3. Popular as tabelas com os CSVs      (clientes, produtos, vendas)
4. Extrair cotações do dólar (API BCB) e popular cotacao_dolar
5. Gerar custos_convertidos            (cruzamento USD × cotação)
6. Executar as análises SQL            (faturamento, ticket médio, prejuízo)
7. Rodar o modelo preditivo            (previsão de demanda)
8. Rodar o motor de recomendação       (similaridade de cosseno)
```

---

## Bibliotecas utilizadas

| Biblioteca   | Uso                                              |
|--------------|--------------------------------------------------|
| pandas       | Manipulação e tratamento de dataframes           |
| matplotlib   | Visualizações e gráficos                         |
| scikit-learn | Similaridade de cosseno (modelo de recomendação) |
| sqlalchemy   | Conexão segura com SQLite via Python             |
| requests     | Consumo da API do Banco Central do Brasil        |
| sqlite3      | Inserções SQL nativas (nativo do Python)         |
| difflib      | Similaridade textual para limpeza de categorias  |
| unicodedata  | Normalização de strings e remoção de acentos     |

> `sqlite3`, `difflib` e `unicodedata` são bibliotecas nativas do Python — não precisam ser instaladas via pip.

---

## Fonte de dados externa

**API do Banco Central do Brasil (PTAX)**
- Endpoint: `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/`
- Dados: cotação diária do dólar comercial (compra e venda)
- Autenticação: não necessária
- Período utilizado: 01/01/2023 a 31/12/2024

---

## Observações importantes

- Nunca utilize `to_sql()` com `if_exists="replace"` em tabelas com schema definido — isso apaga PKs e FKs. Use sempre `INSERT` explícito via `executemany`.
- Prefira o context manager `with sqlite3.connect(...) as con:` para evitar o erro `database is locked`.
- O modelo preditivo usa `shift(1)` antes do `rolling` para evitar data leakage.
- O modelo de recomendação é baseado em filtragem colaborativa implícita (presença/ausência de compra) — produtos com poucas vendas podem ter similaridade distorcida.
