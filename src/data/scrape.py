#!/usr/bin/env python3
import re
import requests
import urllib3
from vars import MODEM_PW, cable_info_file, MODEM_HOST


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

# ---------------------------
# Step 1: Fetch Login Page and Extract Code
# ---------------------------

def fetch_login_page():
    assert session is not None, "Session not initialized."
    response = session.get(LOGIN_PAGE_URL, verify=False)
    if response.status_code != 200:
        print("Failed to fetch the login page.")
        exit(1)

    # Extract the login code using regex similar to: sed -e 's/.*Login?id=//' -e 's/".*//'
    match = re.search(r'Login\?id=([^"]+)"', response.text)
    if not match:
        print("Could not extract the login code.")
        exit(1)
    code = match.group(1)
    print("Login code extracted:", code)
    return code

# ---------------------------
# Step 2: Log In Using the Extracted Code
# ---------------------------




# The payload containing the login credentials


def login(code):
    login_url = f"https://{MODEM_HOST}/goform/Login?id={code}"
    login_response = session.post(login_url, data=PAYLOAD, headers=HEADERS, verify=False)
    if login_response.status_code != 200:
        print("Login failed.")
        exit(1)
    print("Logged in successfully.")

# ---------------------------
# Step 3: Download CableInfo.txt
# ---------------------------

# You can use similar headers as before


def download_cable_info():
    file_response = session.get(CABLEINFO_URL, headers=HEADERS, verify=False)
    if file_response.status_code == 200:
        with cable_info_file(write=True) as file:
            file.write(file_response.content)
        print("CableInfo.txt downloaded successfully.")
    else:
        print("Failed to download CableInfo.txt. Status code:", file_response.status_code)

def initialize_session():
    global session
    session = requests.Session()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape():
    initialize_session()
    code = fetch_login_page()
    login(code)
    download_cable_info()

if __name__ == "__main__":
    scrape()