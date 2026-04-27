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
                params=(f"%{planta}%", f"%{tag}%"))
    except Exception:
        raise ValueError('\nERRO: Atualizar o banco de dados!') from None
    
    if df.empty:
        return None

    data = tempos_falha(df, engine)
    return data