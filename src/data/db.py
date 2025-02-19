from contextlib import asynccontextmanager

import aiopg
import pandas as pd
from common import PG_DB, PG_HOST, PG_PASSWORD, PG_PORT, PG_USER
from logger import Logger
from sqlalchemy import create_engine

logger = Logger.create_logger()



# todo convert to sqalchemy
dsn = "dbname=aiopg user=aiopg password=passwd host=127.0.0.1"
dsn = f"dbname={PG_DB} user={PG_USER} password={PG_PASSWORD} host={PG_HOST} port={PG_PORT}"


async def create_pool():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
                ret = []
                async for row in cur:
                    ret.append(row)
                assert ret == [(1,)]
                
@asynccontextmanager
async def async_sqlconn():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            try:
                yield conn
            finally:
                await conn.close()
                
async def simple_fetchall_async(query: str):
    """
    helper for simple fetch all queries
    """
    async with async_sqlconn() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            return await cursor.fetchall()

# todo convert to async
def write_df_to_db(df: pd.DataFrame, table_name: str) -> None:
    engine = create_engine(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")

    # use the

    # with engine.begin() as connection:
    with engine.connect() as connection:
        # Dynamically infer the column names from the DataFrame
        columns = list(df.columns)  
        col_str = ", ".join([f"\"{col.lower()}\"" for col in columns])
        placeholders = ", ".join(["%s"] * len(columns))

        # Construct the SQL insert query dynamically
        insert_query = f"INSERT INTO {table_name} ({col_str}) VALUES ({placeholders})"

        logger.info(f"Inserting data into {table_name}")
        logger.debug(f"Columns: {columns}")
        logger.debug(f"Insert query: {insert_query}")
        
        # Loop through each row in the DataFrame and execute the insert query
        for index, row in df.iterrows():
            logger.debug(f"Inserting row {index}")
            logger.debug(f"Row data: {row}")
            connection.execute(insert_query, tuple(row[col] for col in columns))
