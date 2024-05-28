## Root-Me.org Challenge Write-Up: HTTP - User-Agent 
`http://challenge01.root-me.org/web-serveur/ch2/`

**Challenge Description:** This challenge focuses on manipulating the "User-Agent" header in an HTTP request to bypass a simple access control mechanism. When accessing the challenge page, you are greeted with the message: "Wrong user-agent: you are not the "admin" browser!".

**Vulnerability Explanation:**

This challenge highlights a common security pitfall: relying solely on client-side attributes like the User-Agent header for crucial access control decisions. The User-Agent header, typically sent by your web browser, identifies the browser, operating system, and rendering engine to the website.  

The vulnerability here stems from the application's logic, which likely checks for a specific User-Agent string (in this case, "admin") to grant access or display specific content.  

**Exploitation Steps:**

**Method 1: Using a Web Proxy (Burp Suite, OWASP ZAP)**

1. **Intercept the Request:** Configure your browser to use the proxy and navigate to the challenge page. The proxy will capture the outgoing request. 
2. **Locate the User-Agent Header:**  Find the "User-Agent" header within the captured request.
3. **Modify the Header:** Change the value of the User-Agent header to "admin".
4. **Forward the Request:** Forward the modified request from your proxy to the server. 
5. **Observe the Response:** The server should now grant access or display the restricted content.

**Method 2:  Using Python and the `requests` Module**

```python
import requests

url = 'http://challenge01.root-me.org/web-serveur/ch2/'  # Replace with the actual challenge URL

headers = {
    'User-Agent': 'admin' 
}

response = requests.get(url, headers=headers)

print(response.text)  # This will print the HTML content of the response
```
**Explanation:**

* We import the `requests` library to make HTTP requests.
* The `url` variable stores the challenge URL.
* We create a dictionary `headers` to store our custom headers. Here we set the 'User-Agent' to 'admin'.
* We use `requests.get()` to send a GET request to the URL with our modified headers.
* Finally, we print the response text to view the results. 

**Remediation:**

* **Never rely solely on client-side attributes for critical access control.** User-Agent and other client-side headers can be trivially modified.
* **Implement robust server-side authentication and authorization mechanisms.** Employ secure methods like sessions, tokens, or OAuth to verify user identities and permissions.
* **Treat all user input as untrusted.** Validate and sanitize any data received from the client, including headers, to prevent injection or manipulation vulnerabilities.

**Conclusion:**

This challenge showcases how easily exploitable vulnerabilities arise from misplaced trust in client-side data. By employing robust server-side security measures, developers can prevent unauthorized access and create more secure applications. 

test
