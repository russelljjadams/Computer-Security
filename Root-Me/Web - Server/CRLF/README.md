## Root-Me.org Challenge Write-Up: Web Server - CRLF Injection
`http://challenge01.root-me.org/web-serveur/ch14/`

**Challenge Description:** The "CRLF" challenge, found in the Web Server category, presents a seemingly simple objective: "Inject false data in the journalisation log." The challenge provides a standard login page with an "authentication log" that displays login attempts, such as successful and failed authentication attempts for various users.

**Vulnerability and Exploitation:**

The challenge name provides a significant clue - "CRLF" stands for Carriage Return (\r) Line Feed (\n). These control characters are used to denote line breaks in numerous network protocols, including HTTP. CRLF injection vulnerabilities emerge when an application fails to sanitize user-supplied data before incorporating it into sensitive headers. 

While one might typically focus on `POST` request parameters for injection, this challenge can be solved by focusing on the `GET` request. By appending a CRLF sequence to the `username` parameter within the URL, it's possible to inject data into the authentication log:

```
GET /web-serveur/ch14/?username=This is injected text.%0d%0atest&password=test HTTP/1.1
```

The server, upon receiving this request, interprets the `%0d%0a` sequence (URL-encoded CRLF) as a line break. This results in the injected text "This is injected text." being displayed on a new line within the authentication log, successfully demonstrating the vulnerability.

**Key Takeaways:**

* **Unconventional Injection Points:** This challenge highlights that CRLF injection is not limited to `POST` requests or form data. An attacker can leverage this vulnerability by injecting malicious payloads into various parts of the HTTP request, including `GET` parameters and headers.
* **Encoding is Key:** Successful exploitation often requires proper encoding of the CRLF characters. Using the URL-encoded equivalents (`%0d%0a`) ensures the server interprets the sequence correctly.
* **Context Determines Impact:** Although this instance demonstrates a seemingly harmless log injection, CRLF vulnerabilities can have far-reaching consequences. Depending on the application's structure and security measures, this vulnerability can be used to perform cross-site scripting attacks, manipulate HTTP headers, or deface websites.

**Recommendations for Further Learning:**

* Explore other potential injection points within the request. Could similar results be achieved by targeting different headers like `Referer`?
* Experiment with various CRLF encoding techniques and bypass methods to understand how different filters might attempt to mitigate this vulnerability.
* Test different payloads beyond simple text injection. Explore the possibility of injecting HTML tags to assess the potential for cross-site scripting vulnerabilities. 

By understanding the mechanics of CRLF injection, penetration testers can effectively identify and exploit this vulnerability in real-world applications. It's crucial to recognize that seemingly minor vulnerabilities can potentially cascade into more severe security breaches if left unaddressed. 

