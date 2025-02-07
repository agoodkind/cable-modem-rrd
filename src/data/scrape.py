#!/usr/bin/env python3
import re
import requests
import urllib3

# Disable insecure SSL warnings (similar to curl's -k option)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create a session to store cookies
session = requests.Session()

# ---------------------------
# Step 1: Fetch Login Page and Extract Code
# ---------------------------
login_page_url = "https://192.168.100.1/Login.htm"
response = session.get(login_page_url, verify=False)
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

# ---------------------------
# Step 2: Log In Using the Extracted Code
# ---------------------------
login_url = f"https://192.168.100.1/goform/Login?id={code}"
headers = {
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

# The payload containing the login credentials
payload = {
    "loginName": "admin",
    "loginPassword": "royalsky929"
}

login_response = session.post(login_url, data=payload, headers=headers, verify=False)
if login_response.status_code != 200:
    print("Login failed.")
    exit(1)
print("Logged in successfully.")

# ---------------------------
# Step 3: Download CableInfo.txt
# ---------------------------
cableinfo_url = "https://192.168.100.1/CableInfo.txt"
# You can use similar headers as before
file_headers = {
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

file_response = session.get(cableinfo_url, headers=file_headers, verify=False)
if file_response.status_code == 200:
    with open("CableInfo.txt", "wb") as file:
        file.write(file_response.content)
    print("CableInfo.txt downloaded successfully.")
else:
    print("Failed to download CableInfo.txt. Status code:", file_response.status_code)
