import os
import pandas as pd
import geopandas as gpd
import numpy as np
import locale
from datetime import datetime

# Função que realiza leitura do arquivo para dataframe
def leTab(dados):
    path = os.getcwd() + "/planilhas/" + dados
    data = pd.read_csv(path, sep=';', encoding='utf-8')
    data = data.replace(',', '.')
    return data

# Função que retorna intervalos do dataframe 
def dataTab(df, dataInicial, dataFinal):
    posicao_inicial = df[df['Data'] == dataInicial].index[0]
    posicao_final = df[df['Data'] == dataFinal].index[0]
    intervalo = df.iloc[posicao_inicial:posicao_final+1].copy()
    return intervalo

# Função que retorna o mes selecionado do dataframe 
def dataMes(df,mes):
    # Converter a coluna 'Data' para o tipo datetime
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', dayfirst=True)
    # Extrair o dia, mês e ano em colunas separadas
    df['Mês'] = df['Data'].dt.strftime('%m')
    intervalo = df[df['Mês'] == mes]
    return intervalo

# Função que retorna o ano selecionado do dataframe 
def dataAno(df,ano):
    # Converter a coluna 'Data' para o tipo datetime
    df['Data'] = pd.to_datetime(df['Data'])
    # Extrair o dia, mês e ano em colunas separadas
    df['Ano'] = df['Data'].dt.year
    intervalo = df[df['Ano'] == int(ano)]
    return intervalo

# Função que retorna a media
def calc_especifica(intervaloData):
    # Lista contendo variaveis a serem analisadas
    colunas = ['Tx', 'Tn', 'Tmed', 'UR', 'Prec', 'Evap', 'Insolação']
    mean_values = {}
    # Realiza o calculo da media para cada coluna
    for column in colunas:
        coluna = intervaloData[column].str.replace(',', '.') # Substituir todas as vírgulas por pontos em uma coluna específica
        coluna = pd.to_numeric(coluna, errors='coerce') #elimina valores ausentes na coluna
        coluna = coluna.dropna() #Isola a coluna especificada
        if column != 'Evap' and  column != 'Insolação':
            mean = coluna.mean() #Realiza o calculo de media
            mean_values[column] = mean #Nova coluna recebe media
        else:
            mean = coluna.sum()
            mean_values[column] = mean #Nova coluna recebe media
    mean_df = pd.DataFrame(mean_values, index=[0])
    return mean_df

def calc_meses_ano(intervaloData):
    # Lista contendo os meses a serem analisadas
    meses = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    mean_dataframes = [] # Cria uma lista vazia
    for mes in meses:
        intervalo_mes = intervaloData[intervaloData['Mês'] == mes] #Percorre cada mes presente no dataframe 
        mean_df = calc_especifica(intervalo_mes) # chame a função que calcula a media
        mean_df['Mês'] = mes # chame a função que calcula a media
        mean_dataframes.append(mean_df) # Adiciona o DataFrame de média à lista
    result = pd.concat(mean_dataframes)# Concatena os DataFrames de média em um único DataFrame
    return(result)

def calc_anos(intervaloData):
    mean_dataframes = []
    for i in range(1976, 2023):
        intervalo_ano = intervaloData[intervaloData['Ano'] == i] # Filtra o intervalo de dados para o ano atual
        mean_df = calc_especifica(intervalo_ano) # Calcula a média para o intervalo do ano
        mean_df['Ano'] = i # Adiciona uma coluna com o valor do ano
        mean_dataframes.append(mean_df) # Adiciona o DataFrame de média à lista
    result = pd.concat(mean_dataframes) # Concatena os DataFrames de média em um único DataFrame
    return result



