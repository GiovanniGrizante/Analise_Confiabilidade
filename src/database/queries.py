import pandas as pd
from pathlib import Path
from src.config import get_engine

# Tratamento dos dados de ordens
def ordens_clean(engine):
    drop = """
    DROP TABLE IF EXISTS ordens_clean;
    """

    create = '''
            CREATE TABLE ordens_clean AS
            SELECT
                Ordem AS ordem,
                datetime([Data fim real da ordem] || ' ' || 
                [Hora para o fim real]) AS data_hora_fim
            FROM ordens_raw
            WHERE [Tipo de ordem] != "PM46"
            AND [Data fim real da ordem] IS NOT NULL'''

    with engine.begin() as conn:
        conn.exec_driver_sql(drop)
        conn.exec_driver_sql(create)

# Tratamento dos dados de notas
def notas_clean(engine):
    drop = """
    DROP TABLE IF EXISTS notas_clean;
    """

    create = '''
            CREATE TABLE notas_clean AS
            SELECT
                Ordem AS ordem,

                datetime([Data da nota] || ' ' || 
                [Ínício da avaria (hora)]) AS data_hora_inicio,

                [Local de instalação] AS local_instalacao
            FROM notas_raw'''


    with engine.begin() as conn:
        conn.exec_driver_sql(drop)
        conn.exec_driver_sql(create)

# Execução das funções
def main():
    engine = get_engine()

    # Executa as funções para geração dos queries
    ordens_clean(engine)
    notas_clean(engine)

if __name__ == '__main__':
    main()