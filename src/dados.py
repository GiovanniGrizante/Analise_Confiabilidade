import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import os, sys, getpass, time, datetime as dt

# Carregar e tratar os dados obtidos pelo SAP
def dados():
    # Diretório dos arquivos
    dir = f'C:\\Users\\{getpass.getuser()}\\Evonik Industries AG\\AME Maintenance - Documentos\\AME_Manutenção\\00 - ORGANIZAÇÃO\\09 - TPT\\Time Evonik\\Giovanni\\Power BI\\Fatos\\Ordens de Serviço'
    # === ORDENS ===
    # Carregamento dos dados de ordens, renomeando as colunas
    try:
        ordens = pd.read_csv(os.path.join(dir, 'Ordens.csv'), sep=',',
                            usecols=['Ordem', 
                                    'Data fim real da ordem', 
                                    'Hora para o fim real',
                                    'Tipo de ordem',
                                    ]).rename(columns={'Data fim real da ordem': 'Data fim', 'Hora para o fim real': 'Hora fim'})

    except PermissionError:
        raise ValueError(
            f"""
        Não há permissão para acessar o arquivo de criticidade.
        Habilite a função "Manter sempre no computador" ou feche o arquivo.

        Caminho do arquivo:
        {os.path.join(dir, 'Ordens.csv')}
        """.strip())
        sys.exit()

    # Remover linhas para ordens preventivas e que não foram finalizadas
    ordens = ordens.dropna(subset=['Data fim'])
    ordens = ordens.drop(ordens[ordens['Tipo de ordem'] == 'PM46'].index).reset_index(drop=True)

    # Tratamento das colunas de data e hora
    ordens['Data fim'] = pd.to_datetime(ordens['Data fim'],errors='coerce')
    ordens['Hora fim'] = pd.to_timedelta(ordens['Hora fim'], errors='coerce')
    ordens['DataHora fim'] = ordens['Data fim'] + ordens['Hora fim']

    # Remoção das colunas desnecessárias
    ordens = ordens.drop(columns=['Data fim', 'Hora fim', 'Tipo de ordem'])

    # === NOTAS ===
    # Carregamento dos dados de notas, renomeando as colunas
    try:
        notas = pd.read_csv(os.path.join(dir, 'Notas.csv'), sep=',',
                            usecols=['Data da nota', 
                                    'Ínício da avaria (hora)', 
                                    'Ordem', 'Local de instalação',
                                    ]).rename(columns={'Data da nota': 'Data início', 'Ínício da avaria (hora)': 'Hora início'})
    except PermissionError:
        raise ValueError(
            f"""
        Não há permissão para acessar o arquivo de criticidade.
        Habilite a função "Manter sempre no computador" ou feche o arquivo.

        Caminho do arquivo:
        {os.path.join(dir, 'Notas.csv')}
        """.strip())
        sys.exit()

    # Tratamento das colunas de data e hora
    notas['Data início'] = pd.to_datetime(notas['Data início'], errors='coerce')
    notas['Hora início'] = pd.to_timedelta(notas['Hora início'], errors='coerce')
    notas['DataHora início'] = notas['Data início'] + notas['Hora início']

    # Remoção das colunas desnecessárias
    notas = notas.drop(columns=['Data início', 'Hora início'])

    # Mescla os DataFrames de ordens e notas com base na coluna 'Ordem'
    df = pd.merge(ordens, notas, on='Ordem', how='inner')
    df = df[['Local de instalação', 'DataHora início', 'DataHora fim']]

    per_ini = df['DataHora início'][0].replace(day=1, month=1, hour=0, minute=0, second=0)
    per_fim = df['DataHora fim'][len(df)-1]
    
    return df, per_ini, per_fim

# Motores que possuam registro no sistema SAP
def especifico(df):
    planta = input('Informe o código da planta (1913 - Orgânicos | 1914 - Sílica | Em branco para geral): ')
    equip = "00" + input('Informe o TAG do equipamento: ')

    # Filtra os dados do DataFrame com base nos filtros fornecidos pelo usuário
    filtros = [planta, equip]
    df = df[
        df['Local de instalação']
        .apply(lambda x: planta in x and equip in x)
    ].reset_index(drop=True)

    if df.empty:
        raise ValueError('Nenhum dado encontrado para os filtros fornecidos.')
        sys.exit()

    if df['Local de instalação'].nunique() > 1:
        raise ValueError('\nAtenção: Existem dados de mais de um local de instalação. Verifique os filtros fornecidos.')
        sys.exit()

    return df

# Motores que possuem nível de criticidade em cada planta
def criticidade(df):
    dir = f'C:\\Users\\{getpass.getuser()}\\Evonik Industries AG\\AME Maintenance - Documentos\\AME_Manutenção\\03 - PREDITIVA\\08- CONTROLE DE AÇÕES'
    
    # Carregamento da tabela de criticidade
    try:
        df_crit = pd.read_excel(os.path.join(dir, 'Calendário Preditivas.xlsx'), sheet_name='MCA', 
        usecols=['Planta', 'TAG', 'Localização', 'Criticidade'])
    except PermissionError:
        raise ValueError(
            f"""
        Não há permissão para acessar o arquivo de criticidade.
        Habilite a função "Manter sempre no computador" ou feche o arquivo.

        Caminho do arquivo:
        {os.path.join(dir, 'Calendário Preditivas.xlsx')}
        """.strip())
        sys.exit()

    # Tratamento da tabela
    df_crit = df_crit.dropna(subset=['TAG'])
    df_crit['TAG'] = df_crit['TAG'].astype(str)

    # Adicionar uma coluna para o código da planta correspondente
    plantas = {'Orgânicos': '1913', 'Sílica': '1914'}
    df_crit['Cod. Planta'] = df_crit['Planta'].map(plantas)

    # Criar as pastas das plantas e criticidades
    estrutura = df_crit[['Planta', 'Criticidade', 'TAG']].drop_duplicates()
    for _, row in estrutura.iterrows():
        caminho = os.path.join(
            'Dados',
            str(row['Planta']),
            str(row['Criticidade']),
            str(row['TAG'])
        )
        os.makedirs(caminho, exist_ok=True)

    # Gerar um dicionário para armazenar os DataFrames filtrados por equipamento
    df_filtrado = {}
    for i in range(1, len(df_crit)):
        planta = df_crit.loc[i, 'Cod. Planta']
        equip = str(df_crit.loc[i, 'TAG'])

        filtros = [planta, equip]

        # Filtrar os dados para o equipamento pesquisado
        df_filtrado[equip] = df[
        df['Local de instalação']
        .apply(lambda x: planta in x and equip in x)
        ].reset_index(drop=True)

        df_filtrado[equip]['Planta'] = df_crit.loc[df_crit['TAG'] == equip, 'Planta'].iloc[0]
        df_filtrado[equip]['Criticidade'] = df_crit.loc[df_crit['TAG'] == equip, 'Criticidade'].iloc[0]

    return df_filtrado

# Executar os comandos
def main():
    while True:
        os.system('cls')
        df, per_ini, per_fim = dados()

        espec = input('Deseja realizar uma análise específica? (S/N): ').strip().upper()
        resp = ['S','N']

        if espec not in resp:
            print('\nResposta inválida. Por favor, responda com "S" para sim ou "N" para não.')
            time.sleep(4)
        elif espec == 'S':
            df = especifico(df)
            return df, per_ini, per_fim, espec
        else:
            df = criticidade(df)
            return df, per_ini, per_fim, espec