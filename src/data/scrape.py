#!/usr/bin/env python3
import re

import requests
import urllib3
from logger import Logger
from vars import MODEM_HOST, MODEM_PW, cable_info_file

logger = Logger.create_logger()

LOGIN_PAGE_URL = f"https://{MODEM_HOST}/Login.htm"
CABLEINFO_URL = f"https://{MODEM_HOST}/CableInfo.txt"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8,ar;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "null",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}
PAYLOAD = {
    "loginName": "admin",
    "loginPassword": MODEM_PW
}


def retrieve_login_code(session: requests.Session) -> str:
    """
    Fetch the login page and extract the login code.
    """
    response = session.get(LOGIN_PAGE_URL, verify=False)
    if response.status_code != 200:
        raise Exception("Failed to fetch the login page. Status code:",
                        response.status_code)

    # Extract the login code using regex similar to: sed -e 's/.*Login?id=//' -e 's/".*//'
    match = re.search(r'Login\?id=([^"]+)"', response.text)
    if not match:
        raise Exception("Could not extract the login code.")

    code = match.group(1)
    logger.info(f"Login code extracted: {code}")
    return code


def retrieve_cable_info(login_code: str, session: requests.Session) -> bytes:
    """
    Log in to the modem using the login code and retrieve the CableInfo.txt file.
    """
    login_url = f"https://{MODEM_HOST}/goform/Login?id={login_code}"
    login_response = session.post(
        login_url, data=PAYLOAD, headers=HEADERS, verify=False)

    if login_response.status_code != 200:
        raise Exception("Failed to log in. Status code:",
                        login_response.status_code)

    logger.info("Logged in successfully.")

    file_response = session.get(CABLEINFO_URL, headers=HEADERS, verify=False)

    if file_response.status_code == 200:
        return file_response.content
    else:
        raise Exception("Failed to retrieve CableInfo.txt. Status code:",
                        file_response.status_code)


def write_cable_info_to_file(file_bytes: bytes) -> None:
    """
    Write the CableInfo.txt file to disk.
    """
    with cable_info_file(write=True) as file:
        file.write(file_bytes)
        logger.info(
            f"{len(file_bytes)} bytes written to {file.name} successfully.")


def initialize_session() -> requests.Session:
    """
    Initialize a requests session with the necessary settings.
    """
    session = requests.Session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return session


def scrape_to_bytes() -> bytes:
    """
    Scrape the CableInfo.txt file and return its content as bytes.
    """
    session = initialize_session()
    login_code = retrieve_login_code(session=session)
    return retrieve_cable_info(login_code, session=session)


def scrape_to_file():
    """
    Scrape the CableInfo.txt file and write it to disk.
    """
    session = initialize_session()
    login_code = retrieve_login_code(session=session)
    cable_info_bytes = retrieve_cable_info(login_code, session=session)
    write_cable_info_to_file(cable_info_bytes)

if __name__ == "__main__":
    scrape_to_file()
