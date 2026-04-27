import pandas as pd
from sqlalchemy import inspect
from pathlib import Path
from src.config import get_engine, create_folders


def db_verification(dir_raw, engine):
    inspector = inspect(engine)
    essential_files = {'Notas': 'Específica', 
                       'Ordens': 'Específica',
                       'Criticidade': 'por Criticidade'}
    
    for file, func in essential_files.items():
        if not inspector.has_table(file.lower() + '_raw'):
            print(f'''\nERRO: Devido a falta do arquivo {file},\na função "{func}" dará erro!
            \nAdicionar o arquivo na pasta:\n\n{dir_raw}''')
            input('\nPressione Enter para continar...')

# Leitura e ingestão dos dados na database
def db_ingestion(dir_raw, engine):

    readers_form = {
        '.csv': pd.read_csv,
        '.xlsx': pd.read_excel,
        '.xls': pd.read_excel,
        '.parquet': pd.read_parquet
    }

    # Leitura e ingestão dos dados
    for file in dir_raw.iterdir():
        if file.suffix.lower() not in readers_form:
            print(f'Arquivo "{file.name}" não suportado')
            continue

        reader = readers_form[file.suffix.lower()]

        data = reader(file)

        if 'Ordem' in data.columns:
            data["Ordem"] = data["Ordem"].astype("string")

        data.to_sql(
            name = f'{file.stem.lower()}_raw',
            con = engine,
            if_exists = 'replace',
            index = False
        )

# Definição dos diretórios e criação da database
def main():
    dir_base = Path(__file__).resolve().parent.parent

    # Gera e nomeia o database
    engine = get_engine()

    # Diretório - Raw Data
    dir_raw = dir_base / 'data' / 'raw'

    # Adiciona os dados no database
    db_ingestion(dir_raw, engine)
    db_verification(dir_raw, engine)

if __name__ == '__main__':
    main()