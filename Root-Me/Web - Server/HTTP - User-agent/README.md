## Root-Me.org Challenge Write-Up: HTTP - User-Agent 
`http://challenge01.root-me.org/web-serveur/ch2/`

**Challenge Description:** This challenge focuses on manipulating the "User-Agent" header in an HTTP request to bypass a simple access control mechanism. When accessing the challenge page, you are greeted with the message: "Wrong user-agent: you are not the "admin" browser!".

**Vulnerability Explanation:**

This challenge highlights a common security pitfall: relying solely on client-side attributes like the User-Agent header for crucial access control decisions. The User-Agent header, typically sent by your web browser, identifies the browser, operating system, and rendering engine to the website.  

The vulnerability here stems from the application's logic, which likely checks for a specific User-Agent string (in this case, "admin") to grant access or display specific content.  

**Exploitation Steps:**

1. **Intercept the Request:**  Utilize a web proxy tool like Burp Suite or OWASP ZAP to intercept the HTTP request sent to the challenge page.  
    * Configure your browser to use the proxy.
    * Navigate to the challenge page. The proxy will capture the request.

2. **Locate the User-Agent Header:** Within the captured request, find the "User-Agent" header. It will look something like this: 

    ```
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 
    ```

3. **Modify the Header:**  Change the value of the User-Agent header to "admin". The modified header will look like this:

    ```
    User-Agent: admin
    ```

4. **Forward the Request:**  Forward the modified request from your proxy to the server.

5. **Observe the Response:** The server, now tricked by the spoofed User-Agent, should grant access to the restricted content or functionality.

**Remediation:**

* **Never rely solely on client-side attributes for critical access control.** User-Agent and other client-side headers can be trivially modified.
* **Implement robust server-side authentication and authorization mechanisms.**  Employ secure methods like sessions, tokens, or OAuth to verify user identities and permissions.
* **Treat all user input as untrusted.** Validate and sanitize any data received from the client, including headers, to prevent injection or manipulation vulnerabilities.

**Conclusion:**

This challenge showcases how easily exploitable vulnerabilities arise from misplaced trust in client-side data. By employing robust server-side security measures, developers can prevent unauthorized access and create more secure applications. 
