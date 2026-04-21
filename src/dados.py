import pandas as pd

# Cálculo dos tempos de falha
def tempos_falha(df, engine):
    def periodos(engine):
        # Data da primeira falha (Gera um dataframe)
        df_ini = pd.read_sql('''
                          SELECT strftime('%Y', MIN(data_hora_inicio)) AS ano_inicio
                          FROM notas_clean''', engine)

        ano_ini = df_ini.loc[0, 'ano_inicio']
        
        #Período inicial
        per_ini = pd.Timestamp(year=int(ano_ini), month=1, day=1)

        # Data da última falha
        df_fim = pd.read_sql('''
                            SELECT MAX(data_hora_fim) AS per_fim
                            FROM ordens_clean''', engine)

        per_fim = pd.to_datetime(df_fim.loc[0, 'per_fim'])

        return per_ini, per_fim

    per_ini, per_fim = periodos(engine)

    # Converte os dados de tempo para não ser string
    df['data_hora_inicio'] = pd.to_datetime(df['data_hora_inicio'])
    df['data_hora_fim'] = pd.to_datetime(df['data_hora_fim'])

    # Cálculo das diferenças entre as bordas e os tempos de inicio e fim
    diff_inicio = round(((df['data_hora_inicio'].iloc[0] - per_ini).total_seconds()/3600), 2)
    diff_fim = round(((per_fim - df['data_hora_fim'].iloc[-1]).total_seconds()/3600), 2)

    # Gerar lista com os tempos de operação
    diff_ordens = (
            (df['data_hora_inicio'].shift(-1) - df['data_hora_fim'])
            .dt.total_seconds()/3600
            ).round(2)[:-1].tolist()
    
    # Se houver 'DataHora fim' > 'DataHora início', não deve ser considerado
    diff_ordens = [x for x in diff_ordens if x > 0]

    data = [diff_inicio] + diff_ordens

    # Se 'DataHora fim' for o período final de análise, não considera
    if diff_fim > 0:
        data.append(diff_fim)

    return data

# Motores que possuam registro no sistema SAP
def especifico(planta, tag):
    engine = get_engine()

    try:
        df = pd.read_sql('''
                SELECT
                    n.data_hora_inicio AS data_hora_inicio,
                    o.data_hora_fim AS data_hora_fim
                FROM ordens_clean o
                INNER JOIN notas_clean n
                    ON o.ordem = n.ordem
                WHERE n.local_instalacao LIKE ?
                AND n.local_instalacao LIKE ?
                ORDER BY n.data_hora_inicio
                ''',
                engine,
                params=(f"%{planta}%", f"%{tag}%")
            )
    except Exception as e:
        raise ValueError('''\nERRO: Atualizar o banco de dados!''') from None
    
    if df.empty:
        return None

    data = tempos_falha(df, engine)
    return data

# Motores que possuem nível de criticidade em cada planta
# def criticidade(df):
#     dir = f'C:\\Users\\{getpass.getuser()}\\Evonik Industries AG\\AME Maintenance - Documentos\\AME_Manutenção\\03 - PREDITIVA\\08- CONTROLE DE AÇÕES'
    
#     # Carregamento da tabela de criticidade
#     try:
#         df_crit = pd.read_excel(os.path.join(dir, 'Calendário Preditivas.xlsx'), sheet_name='MCA', 
#         usecols=['Planta', 'TAG', 'Localização', 'Criticidade'])
#     except PermissionError:
#         raise ValueError(
#             f"""
#         Não há permissão para acessar o arquivo de criticidade.
#         Habilite a função "Manter sempre no computador" ou feche o arquivo.

#         Caminho do arquivo:
#         {os.path.join(dir, 'Calendário Preditivas.xlsx')}
#         """.strip())
#         sys.exit()

#     # Tratamento da tabela
#     df_crit = df_crit.dropna(subset=['TAG'])
#     df_crit['TAG'] = df_crit['TAG'].astype(str)

#     # Adicionar uma coluna para o código da planta correspondente
#     plantas = {'Orgânicos': '1913', 'Sílica': '1914'}
#     df_crit['Cod. Planta'] = df_crit['Planta'].map(plantas)

#     # Criar as pastas das plantas e criticidades
#     estrutura = df_crit[['Planta', 'Criticidade', 'TAG']].drop_duplicates()
#     for _, row in estrutura.iterrows():
#         caminho = os.path.join(
#             'Dados',
#             str(row['Planta']),
#             str(row['Criticidade']),
#             str(row['TAG'])
#         )
#         os.makedirs(caminho, exist_ok=True)

#     # Gerar um dicionário para armazenar os DataFrames filtrados por equipamento
#     df_filtrado = {}
#     for i in range(1, len(df_crit)):
#         planta = df_crit.loc[i, 'Cod. Planta']
#         equip = str(df_crit.loc[i, 'TAG'])

#         filtros = [planta, equip]

#         # Filtrar os dados para o equipamento pesquisado
#         df_filtrado[equip] = df[
#         df['Local de instalação']
#         .apply(lambda x: planta in x and equip in x)
#         ].reset_index(drop=True)

#         df_filtrado[equip]['Planta'] = df_crit.loc[df_crit['TAG'] == equip, 'Planta'].iloc[0]
#         df_filtrado[equip]['Criticidade'] = df_crit.loc[df_crit['TAG'] == equip, 'Criticidade'].iloc[0]

#     return df_filtrado

if __name__ == '__main__':
    from config import get_engine
else:
    from src.config import get_engine