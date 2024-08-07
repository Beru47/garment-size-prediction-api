
from sqlalchemy import inspect
from sqlalchemy.orm import Session

def get_table_info(db: Session, table_name: str):
    inspector = inspect(db.bind)
    if table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_info = {col['name']: str(col['type']) for col in columns}  # Convert type to string
        return {
            "exists": True,
            "columns": column_info
        }
    else:
        return {"exists": False, "columns": []}