# Módulo de limpeza e tratamento de valores ausentes

# Imports
import numpy as np
import pandas as pd


# Calcula o percentual de valores ausentes
def calcPercentualValoresAusentes(df):
    # Calcula o total de células no dataset
    totalCells = np.prod(df.shape)

    # Conta o número de valores ausentes por coluna
    missingCount = df.isnull().sum()

    # Calcula o total de valores ausentes
    totalMissing = missingCount.sum()

    # Calcula o percentual de valores ausentes
    print("O dataset tem", round(((totalMissing / totalCells) * 100), 2),"%", "de valores ausentes.")


# Função que calcula o percentual de linhas com valores ausentes
def calcPercentualValoresAusentesLinha(df):
    # Calcula o número total de linhas com valores ausentes
    missingRows = sum([True for idx, row in df.iterrows() if any(row.isna())])

    # Calcula o número total de linhas
    totalRows = df.shape[0]

    # Calcula a porcentagem de linhas ausentes
    print(round(((missingRows / totalRows) * 100), 2),"%",
          "das linhas no conjunto de dados contêm pelo menos um valor ausente.")


# Função para calcular valores ausentes por coluna
def calcPercentualValoresAusentesColuna(df):
    # Total de valores ausentes
    misVal = df.isnull().sum()

    # Porcentagem de valores ausentes
    misValPercent = 100 * misVal / len(df)

    # Tipo de dado das colunas com valores ausentes
    misValDtype = df.dtypes

    # Cria uma tabela com os resultados
    misValTable = pd.concat([misVal, misValPercent, misValDtype], axis=1)

    # Renomear as colunas
    misValTableRenColumns = misValTable.rename(
        columns={0: 'Valores Ausentes', 1: '% de Valores Ausentes', 2: 'Dtype'})

    # Classifica a tabela por porcentagem de valores ausentes de forma decrescente e remove colunas sem valores faltantes
    misValTableRenColumns = misValTableRenColumns[misValTableRenColumns.iloc[:, 0] != 0].sort_values(
        '% de Valores Ausentes', ascending=False).round(2)

    # Print 
    print("O dataset tem " + str(df.shape[1]) + " colunas.\n"
                                                "Encontrado: " + str(
        misValTableRenColumns.shape[0]) + " colunas que têm valores ausentes.")

    if misValTableRenColumns.shape[0] == 0:
        return

    # Retorna o dataframe com informações ausentes
    return misValTableRenColumns


# Imputação de valores ausentes usando forward fill (preenchimento progressivo)
# method = 'ffill': Ffill ou forward-fill propaga o último valor não nulo observado para frente até que outro valor não nulo seja encontrado
def fixMissingFfill(df, col):
    count = df[col].isna().sum()
    df[col] = df[col].ffill()
    print(f"{count} valores ausentes na coluna {col} foram substituídos usando o método de preenchimento progressivo.")
    return df[col]


# Imputação de valores ausentes usando backward fill (preenchimento reverso)
# method = 'bfill': Bfill ou backward-fill propaga o primeiro valor não nulo observado para trás até que outro valor não nulo seja encontrado
def fixMissingBfill(df, col):
    count = df[col].isna().sum()
    df[col] = df[col].bfill()
    print(f"{count} valores ausentes na coluna {col} foram substituídos usando o método de preenchimento reverso.")
    return df[col]


# Imputação usando a mediana
def fixMissingMedian(df, col):
    median = df[col].median()
    count = df[col].isna().sum()
    df[col] = df[col].fillna(median)
    print(f"{count} valores ausentes na coluna {col} foram substituídos por seu valor de mediana {median}.")
    return df[col]


# Preenche valor NA
def fixMissingValue(df, col, value):
    count = df[col].isna().sum()
    df[col] = df[col].fillna(value)
    if isinstance(value, str):  # Corrigido para usar isinstance
        print(f"{count} valores ausentes na coluna {col} foram substituídos por '{value}'.")
    else:
        print(f"{count} valores ausentes na coluna {col} foram substituídos por {value}.")
    return df[col]


# Drop duplicatas
def dropDuplicates(df):
    old = df.shape[0]
    df.drop_duplicates(inplace=True)
    new = df.shape[0]
    count = old - new
    if count == 0:
        print("Nenhuma linha duplicada foi encontrada.")
    else:
        print(f"{count} linhas duplicadas foram encontradas e removidas.")


# Drop de linhas com valores ausentes
def dropRowsWithMissingValues(df):
    old = df.shape[0]
    df.dropna(inplace=True)
    new = df.shape[0]
    count = old - new
    print(f"{count} linhas contendo valores ausentes foram descartadas.")


# Drop de colunas
def dropColumns(df, columns):
    df.drop(columns, axis=1, inplace=True)
    count = len(columns)
    if count == 1:
        print(f"{count} coluna foi descartada.")
    else:
        print(f"{count} colunas foram descartadas.")
