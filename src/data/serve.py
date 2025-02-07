from flask import Flask
from vars import sqlconn

app = Flask(__name__)

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
        columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
        data = conn.execute(f"SELECT * FROM {table_name}").fetchall()

        return [transform_row(row, columns) for row in data]

@app.route('/api/<table_name>')
def table(table_name: str):
    if table_name not in get_tables():
        return f'Table {table_name} not found'
    else:
        return get_columns(table_name)
    
@app.route('/api/listTables')
def listTables():
    return get_tables()
    
@app.route('/')
def index():
    # return list of <a href="table_name">table_name</a>
    links = '\n'.join([f'<div><a href="{table_name}">{table_name}</a></div>' for table_name in get_tables()]) + '<div><a href="/api/listTables">List Tables</a><div>'
    return f"<html><body style=\"background-color: black; color: white\"><h1>Tables</h1>{links}</body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
