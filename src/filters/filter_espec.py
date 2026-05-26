from .common import tempos_falha
from ..settings.engine import get_engine

import pandas as pd

def main(planta, tag):
    engine = get_engine()

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
    
    if df.empty:
        return None

    return tempos_falha(df, engine)