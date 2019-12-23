import sqlite3
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/table/{param}={item_id}")
async def read_table(item_id: int, param: str, q: str = None):
    with sqlite3.connect('db.db') as conn:
        records = conn.execute(f'SELECT * FROM records WHERE {param}={item_id}')    
    return records
