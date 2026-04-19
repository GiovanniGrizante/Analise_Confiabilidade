from pathlib import Path
from sqlalchemy import create_engine

def get_engine():
    dir_base = Path(__file__).resolve().parent.parent
    dir_db = dir_base / "data" / "database" / "manutencao.db"
    dir_db.parent.mkdir(parents=True, exist_ok=True)
    
    return create_engine(f"sqlite:///{dir_db}")

