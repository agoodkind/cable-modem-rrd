from itertools import cycle
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


if __name__ == "__main__":
    logger.info("Starting refresh cycle")
    
    cycle_count = 0
    
    while cycle_count < 4:
        logger.info("Refresh %d", cycle_count + 1)
        
        with timer():
            refresh()
            
        logger.info("Sleeping for %d seconds", 15)
        
        cycle_count += 1
        
        sleep(15)
        logger.info("Woke up!")
        
    logger.info("Done!")
