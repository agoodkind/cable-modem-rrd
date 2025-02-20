from time import sleep

from logger import Logger
from parse import append_cable_data_to_db, parse_to_cable_data
from scrape import scrape_to_bytes
from timer import timer

logger = Logger.create_logger()


def refresh():
    """
    Convenience function to scrape, parse, and append data to the database.
    """
    file_bytes = scrape_to_bytes()
    logger.info("Scraped %d bytes", len(file_bytes))
    cable_data = parse_to_cable_data(file_bytes)
    append_cable_data_to_db(cable_data)

def refresh_with_cycle(num_cycles: int | None = None, sleep_time_secs: int | None = None):
    """
    Convenience function to scrape, parse, and append data to the database
    with a timer.
    """
    logger.info("Starting refresh cycle")
    
    if not num_cycles:
        num_cycles = 1
    if not sleep_time_secs:
        sleep_time_secs = 0

    cycle_count = 0

    while cycle_count < num_cycles:
        logger.info("Refresh %d", cycle_count + 1)

        with timer():
            refresh()

        cycle_count += 1

        if sleep_time_secs:
            logger.info("Sleeping for %d seconds", sleep_time_secs)
            sleep(sleep_time_secs)
            logger.info("Woke up!")

    logger.info("Done!")

