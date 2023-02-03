from sqlalchemy import create_engine, text
import pandas as pd

def get_table(table_name, conn):
    table_name = table_name.upper()
    engine = create_engine(conn)
    df = ''
    with engine.connect() as connection:
        df = pd.DataFrame(connection.execute(text('SELECT * FROM PLAYER')))
    return df