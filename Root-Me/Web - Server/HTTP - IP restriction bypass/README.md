## Web-Server Challenge: HTTP - IP restriction bypass
`https://www.root-me.org/en/Challenges/Web-Server/HTTP-IP-restriction-bypass`

### Description

This challenge simulates a common scenario where access to a web application is restricted to users connected to the internal Local Area Network (LAN). A message on the login page indicates that authentication isn't required for users already on the LAN.

### Vulnerability

The vulnerability here lies in the assumption that the web application relies solely on the client's IP address to determine their network location. By manipulating the HTTP headers sent in our request, we can spoof our IP address and trick the server into thinking we are on the LAN.

### Solution

1. **Identifying the relevant HTTP header:** Most web servers look for the `X-Forwarded-For` (XFF) header to determine the client's original IP address. Some servers might also use `Client-IP`.

2. **Spoofing the IP address:** We need to add the XFF header to our request and set it to a private IP address, typically in the ranges:
    * `10.0.0.0` - `10.255.255.255`
    * `172.16.0.0` - `172.31.255.255`
    * `192.168.0.0` - `192.168.255.255`

   Here's how you can do this using curl:
   ```bash
   curl -H "X-Forwarded-For: 192.168.1.100" http://challenge-url
   ```
   There's also an accompanying Python file that does the same thing.

### How to Find This Information

1. **HTTP Headers References:** You can learn more about HTTP headers from the official Mozilla documentation:
    * [MDN Web Docs: HTTP headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

2. **Private IP Addresses:** Information about private IP address ranges can be found on:
    * [Wikipedia: Private network](https://en.wikipedia.org/wiki/Private_network)

### Additional Notes

* **Real-World Impact:** This vulnerability highlights the importance of not relying solely on IP-based restrictions for security. In real-world scenarios, an attacker might be able to exploit this to gain unauthorized access to sensitive internal resources.

* **Mitigation:**  A more robust solution would involve stronger authentication mechanisms like usernames/passwords or multi-factor authentication.
