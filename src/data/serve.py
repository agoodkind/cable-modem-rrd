from refresh import refresh
from quart import Quart, abort
from scrape import scrape_to_bytes
from vars import sqlconn

app = Quart(__name__)

def get_tables():
    with sqlconn() as conn:
        # [
        # ['table1'],
        # ['table2'],
        # ['table3'],
        # ...
        # ]
        # convert to ['table1', 'table2', 'table3', ...]
        return [table[0] for table in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

def transform_row(row, columns):
    return {columns[i][1]: row[i] for i in range(len(columns))}

def get_columns(table_name: str):
    with sqlconn() as conn:
        return conn.execute(f"PRAGMA table_info({table_name})").fetchall()


def get_table(table_name: str):
    columns = get_columns(table_name)
    with sqlconn() as conn:
        data = conn.execute(f"SELECT * FROM {table_name}").fetchall()

        return [transform_row(row, columns) for row in data]


@app.route('/api/tables/<table_name>/columns')
async def columns(table_name: str):
    if table_name not in get_tables():
        abort(404, f'Table {table_name} not found')
    else:
        return get_columns(table_name)


@app.route('/api/tables/<table_name>')
async def table(table_name: str):
    if table_name not in get_tables():
        abort(404, f'Table {table_name} not found')
    else:
        return get_table(table_name)


@app.route('/api/tables')
def listTables():
    return get_tables()


@app.route('/api/scrape', methods=['POST'])
async def scrapePost():
    # scrape data

    refresh()
    return 'Scraped and parsed data'


@app.route('/')
async def index():
    # return list of <a href="table_name">table_name</a>
    links = '\n'.join([f'<div><a href="{table_name}">{table_name}</a></div>' for table_name in get_tables()]) + '<div><a href="/api/listTables">List Tables</a><div>'
    return f"<html><body style=\"background-color: black; color: white\"><h1>Tables</h1>{links}</body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
