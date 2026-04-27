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