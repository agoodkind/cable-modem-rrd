# todo write me
# remove all __name__ == "__main__" blocks
# and instead use this file with cli entrypoints
import os

import click
from parse import parse_from_file
from refresh import refresh_with_cycle
from scrape import scrape_to_bytes, scrape_to_file


@click.group()
# @click.option("--cm_password", help="Password for the cable modem.", type=str, required=False)
# @click.option("--cm_host", help="Host for the cable modem.", type=str, required=False)
# @click.option("--pg_password", help="Password for the PostgreSQL database.", type=str, required=False)
# @click.option("--pg_user", help="User for the PostgreSQL database.", type=str, required=False)
# @click.option("--pg_host", help="Host for the PostgreSQL database.", type=str, required=False)
# @click.option("--pg_port", help="Port for the PostgreSQL database.", type=str, required=False)
# @click.option("--pg_db", help="Database for the PostgreSQL database.", type=str, required=False)
def cli(): 
    pass
#     cm_password: str | None,
#     cm_host: str | None,
#     pg_password: str | None,
#     pg_user: str | None,
#     pg_host: str | None,
#     pg_port: str | None,
#     pg_db: str | None,
# ):
#     if cm_password:
#         os.environ["MODEM_PW"] = cm_password
#     if cm_host:
#         os.environ["MODEM_HOST"] = cm_host
#     if pg_password:
#         os.environ["PG_PASSWORD"] = pg_password
#     if pg_user:
#         os.environ["PG_USER"] = pg_user
#     if pg_host:
#         os.environ["PG_HOST"] = pg_host
#     if pg_port:
#         os.environ["PG_PORT"] = pg_port
#     if pg_db:
#         os.environ["PG_DB"] = pg_db


@cli.command()
@click.option("--cycles", help="Refresh cycle count.", type=int, required=False)
@click.option("--sleep", help="Time to sleep between cycles.", type=int, required=False)
def refresh(cycles: int | None, sleep: int | None):
    args = {}

    if cycles:
        args["num_cycles"] = cycles
    if sleep:
        args["sleep_time_secs"] = sleep

    refresh_with_cycle(**args)


@cli.command()
@click.option("--file", help="Path to the file to parse.", type=str, required=False)
def parse(file: str | None):
    parse_from_file(file)


@cli.command()
@click.option(
    "--file", help="Path to the file to save scraping data.", type=str, required=False
)
def scrape(file: str | None):
    if file:
        scrape_to_file(file)
    else:
        bytes = scrape_to_bytes()
        print(bytes)

cli.add_command(refresh)
cli.add_command(parse)
cli.add_command(scrape)

if __name__ == "__main__":
    cli()
