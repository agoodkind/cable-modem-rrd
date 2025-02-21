import uvicorn
from db import async_sqlconn, simple_fetchall_async
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from refresh import refresh
from utils.logger import Logger

logger = Logger.create_logger()
app = FastAPI()


async def get_tables():
    # [
    # ['table1'],
    # ['table2'],
    # ['table3'],
    # ...
    # ]
    # convert to ['table1', 'table2', 'table3', ...]
    tables = await simple_fetchall_async(
        """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public'
            AND table_type='BASE TABLE';
        """
    )

    return [table[0] for table in tables]


async def transform_row(row, columns):
    return {columns[i][0]: row[i] for i in range(len(columns))}


async def get_columns(table_name: str):
    return await simple_fetchall_async(
        f"""
            SELECT
                column_name
            FROM
                information_schema.columns
            WHERE
                table_schema = 'public' AND
                table_name = '{table_name}';
        """
    )


async def get_table(
    table_name: str,
    base_limit: int | None,
    min_ts: int | None = None,
    max_ts: int | None = None,
    offset: int | None = None,
):
    columns = await get_columns(table_name)

    async with async_sqlconn() as db:
        async with db.cursor() as cursor:
        # get the first ~32 rows and find the min & max columnID
            if base_limit is not None:
                await cursor.execute(f"SELECT MAX(Channel) FROM {table_name}")
                max_id = await cursor.fetchone()
                calculated_limit = base_limit * max_id[0]

            select = f"SELECT * FROM {table_name}"
            order_by = " ORDER BY timestamp DESC"

            wheres = []
            if min_ts is not None:
                wheres.append(f"timestamp > {min_ts}")
            if min_ts is not None:
                wheres.append(f"timestamp < {max_ts}")

            sql = select

            if len(wheres) > 0:
                sql += " WHERE " + " AND ".join(wheres)

            sql += order_by

            if base_limit is not None:
                sql += f" LIMIT {calculated_limit}"

            if offset is not None:
                sql += f" OFFSET {offset}"


            await cursor.execute(sql)
            data = await cursor.fetchall()
            return [await transform_row(row, columns) for row in data]


@app.post("/api/dangerous/execute_sql")
async def execute_sql(sql: str) -> list:
    return await simple_fetchall_async(sql)


@app.get("/api/tables/{table_name}/columns")
async def columns(table_name: str):
    if table_name not in await get_tables():
        raise HTTPException(404, f"Table {table_name} not found")
    else:
        return await get_columns(table_name)


@app.get("/api/tables/{table_name}")
async def table(
    table_name: str,
    limit: int,
    min_ts: int,
    max_ts: int,
    offset: int
):
    if table_name not in await get_tables():
        raise HTTPException(404, f"Table {table_name} not found")
    else:
        return await get_table(table_name, limit, min_ts, max_ts, offset)


@app.get("/api/tables", response_model=list)
async def list_tables():
    return await get_tables()


@app.post("/api/scrape")
async def scrape_post():
    # scrape data

    refresh()
    return "Scraped and parsed data"


@app.get("/", response_class=HTMLResponse)
async def index():
    links = (
        "\n".join(
            [
                f'<div><a href="{table_name}">{table_name}</a></div>'
                for table_name in await get_tables()
            ]
        )
        + '<div><a href="/api/tables">List Tables</a><div>'
    )
    return f'<html><body style="background-color: black; color: white"><h1>Tables</h1>{links}</body></html>'

def run():
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True, reload_includes=["src/data/*.py"])
