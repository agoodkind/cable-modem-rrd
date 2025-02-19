import aiosqlite
import uvicorn
from common import async_sqlconn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from logger import Logger
from refresh import refresh

logger = Logger.create_logger()
app = FastAPI()


async def get_tables():
    async with async_sqlconn() as db:
        # [
        # ['table1'],
        # ['table2'],
        # ['table3'],
        # ...
        # ]
        # convert to ['table1', 'table2', 'table3', ...]
        async with db.execute("SELECT name FROM sqlite_master WHERE type='table'") as cursor:
            tables = await cursor.fetchall()
            return [table[0] for table in tables]


async def transform_row(row, columns):
    return {columns[i][1]: row[i] for i in range(len(columns))}


async def get_columns(table_name: str):
    async with async_sqlconn() as conn:
        async with conn.execute(f"PRAGMA table_info({table_name})") as cursor:
            return await cursor.fetchall()


async def get_table(table_name: str, limit: int = 100):
    columns = await get_columns(table_name)
    
    async with async_sqlconn() as db:
        # get the first ~32 rows and find the min & max columnID
        async with db.execute(f"SELECT MAX(ChannelID) FROM {table_name}") as cursor:
            max_id = await cursor.fetchone()
            calculated_limit = limit * max_id[0]
        async with db.execute(f"SELECT * FROM {table_name} LIMIT {calculated_limit}") as cursor:
            data = await cursor.fetchall()
            return [await transform_row(row, columns) for row in data]


@app.post("/api/dangerous/execute_sql")
async def execute_sql(sql: str):
    async with async_sqlconn() as db:
        async with db.execute(sql) as cursor:
            return await cursor.fetchall()

@app.get('/api/tables/{table_name}/columns')
async def columns(table_name: str):
    if table_name not in await get_tables():
        raise HTTPException(404, f'Table {table_name} not found')
    else:
        return await get_columns(table_name)


@app.get('/api/tables/{table_name}')
async def table(table_name: str, limit: int = 100):
    if table_name not in await get_tables():
        raise HTTPException(404, f'Table {table_name} not found')
    else:
        return await get_table(table_name, limit)


@app.get('/api/tables', response_model=list)
async def listTables():
    return await get_tables()


@app.post('/api/scrape')
async def scrapePost():
    # scrape data

    refresh()
    return 'Scraped and parsed data'


@app.get('/', response_class=HTMLResponse)
async def index():
    # return list of <a href="table_name">table_name</a>
    links = '\n'.join([f'<div><a href="{table_name}">{table_name}</a></div>' for table_name in await get_tables(
    )]) + '<div><a href="/api/tables">List Tables</a><div>'
    return f"<html><body style=\"background-color: black; color: white\"><h1>Tables</h1>{links}</body></html>"

if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=8000, reload=True)
