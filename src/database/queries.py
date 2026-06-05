import pandas as pd
from pathlib import Path
from ..settings.engine import get_engine

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
        
def criticidade_clean(engine):
    drop = '''
    DROP TABLE IF EXISTS critic_clean;
    '''
    
    create = '''
            CREATE TABLE critic_clean AS
            SELECT
                CASE
                    WHEN TRIM(Planta) = 'Orgânicos' THEN '1913'
                    WHEN TRIM(Planta) = 'Sílica' THEN '1914'
                END AS planta,
                
                CASE
                    WHEN LENGTH(TRIM(TAG)) < 4
                        THEN substr('0000' || TRIM(TAG), -4, 4)
                    ELSE TRIM(TAG)
                END AS tag,

                TRIM(Localização) AS local,

                TRIM(Criticidade) AS criticidade

            FROM criticidade_raw
                '''

    with engine.begin() as conn:
        conn.exec_driver_sql(drop)
        conn.exec_driver_sql(create)
    

# Execução das funções
def main():
    engine = get_engine()

    # Executa as funções para geração dos queries
    ordens_clean(engine)
    notas_clean(engine)
    criticidade_clean(engine)

if __name__ == '__main__':
    main()