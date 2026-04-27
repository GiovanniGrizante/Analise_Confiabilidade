# Motores que possuem nível de criticidade em cada planta
def criticidade():
    engine = get_engine()

    try:
        df = pd.read_sql('''
                SELECT *
                FROM criticidade_raw''',
                engine)
    except Exception:
        raise ValueError('\nERRO: Atualizar o banco de dados!') from None

    #for tag in df['TAG']:
        

    print(df)
    sys.exit()
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