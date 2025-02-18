from logger import Logger
from parse import append_cable_data_to_db, parse_to_cable_data
from scrape import scrape_to_bytes

logger = Logger.create_logger()


def refresh():
    """
    Convenience function to scrape, parse, and append data to the database.
    """
    file_bytes = scrape_to_bytes()
    logger.info("Scraped %d bytes", len(file_bytes))
    cable_data = parse_to_cable_data(file_bytes)
    append_cable_data_to_db(cable_data)


if __name__ == "__main__":
    logger.info("Refreshing data")
    refresh()
    logger.info("Done!")
