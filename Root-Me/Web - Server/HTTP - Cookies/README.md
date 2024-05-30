## Root-Me.org Challenge Write-Up: HTTP - Cookies
`https://www.root-me.org/en/Challenges/Web-Server/HTTP-Cookies`

**Challenge Description:**  We encounter a seemingly simple PHP script designed to collect user emails. However, there's a protected section for "saved email addresses," hinting at an access control vulnerability.

**Vulnerability Exploited:** Insecure Cookie Handling for Authorization

**Tools Used:** Burp Suite (or similar web proxy)

**Exploitation Steps:**

1. **Analyze Application Behavior:**  We interacted with the form and noticed a protected link for "saved email addresses," suggesting a need for authentication or authorization.

2. **Intercept the Request:**  Using Burp Suite, we intercepted the GET request when clicking the protected link. The key observation was the presence of a cookie:

    ```
    Cookie: ch7=visiteur; session=eyJhZG1pbiI6ImZhbHNlIiwidXNlcm5hbWUiOiJndWVzdCJ9.ZljThQ.fcDV2F2a_Nyqzrj-ngVGCO5v9es 
    ```

3. **Focus on Suspicious Cookies:**  We identified two cookies:  `ch7` and `session`.  The  `ch7=visiteur` looked particularly interesting. Could "visiteur" imply a regular visitor role?

4. **Modify the Cookie Value:** Based on the "visiteur" hint, we modified the `ch7` cookie value to  `ch7=admin` before forwarding the request.

5. **Bypass Authorization:**  The application granted access to the protected section, revealing the challenge flag! This confirmed that the application relied solely on the client-side cookie value for authorization, a critical flaw.

**Key Takeaways:**

* **Never Trust Client-Side Data:**  Cookies are easily modifiable by the user.  Never rely solely on client-side data like cookies for authorization or storing sensitive information.
* **Server-Side Validation is Crucial:**  Always validate user roles, permissions, and other authorization logic on the server-side.  Do not expose sensitive actions or data without proper server-side checks. 
* **Secure Cookie Practices:**  Use secure flags (HTTPOnly, Secure) for cookies to mitigate risks associated with cross-site scripting (XSS) and man-in-the-middle attacks.

**Remediation:**

The application developers should:

* **Implement robust server-side authorization:** Verify user roles and permissions against a database or other secure storage mechanism before granting access to protected resources.
* **Avoid storing sensitive information in cookies:** If absolutely necessary, encrypt and sign cookie data to prevent tampering.
* **Use appropriate session management techniques:** Employ session tokens and implement proper timeout mechanisms to enhance security.


