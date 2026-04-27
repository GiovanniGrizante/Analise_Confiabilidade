from pathlib import Path
from sqlalchemy import create_engine
import os

def get_engine():
    dir_base = Path(__file__).resolve().parent.parent
    dir_db = dir_base / "data" / "database" / "manutencao.db"
    dir_db.parent.mkdir(parents=True, exist_ok=True)
    
    return create_engine(f"sqlite:///{dir_db}")

def create_folders(dir_base):
    os.system('cls')
    os.makedirs(dir_base / 'data' / 'raw', exist_ok=True)
    os.makedirs(dir_base / 'images', exist_ok=True)
    print(f'Pastas criadas em \n\n{dir_base}')
    print('\nInsira os arquivos do banco de dados na pasta "raw"')
    input('\nPressione Enter para continuar...')
    return