      
import requests

url = 'http://challenge01.root-me.org/web-serveur/ch2/' #  Replace with the actual challenge URL

headers = {
    'User-Agent': 'admin'  #  Remember,  pick an IP that looks like it's on their LAN
}

response = requests.get(url, headers=headers)

print(response.text)  # This will print the HTML content of the response
