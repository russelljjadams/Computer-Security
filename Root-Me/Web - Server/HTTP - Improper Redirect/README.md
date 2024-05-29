## Root-Me.org Challenge Write-Up: HTTP - Improper Redirect
`https://www.root-me.org/en/Challenges/Web-Server/HTTP-Improper-redirect`

**Challenge Description:** This challenge focuses on exploiting an "Improper Redirect" vulnerability, highlighting the importance of proper script termination in web applications, particularly in PHP. 

**Vulnerability Explanation:**

Improper redirect vulnerabilities occur when a web application issues a redirect (e.g., using `header('Location: ...');` in PHP) without properly terminating script execution afterward. If sensitive operations are performed after the redirect but before termination, an attacker might be able to bypass security measures or access protected resources.

**Challenge Breakdown:**

1. **Initial Observations:**
   - The challenge provides a login form with a `redirect` parameter in the URL (`login.php?redirect`).
   - Intercepting requests and responses does not immediately reveal any obvious redirects (e.g., 302 status codes or `Location` headers) when interacting with the login form normally.

2. **Analyzing the Hint:**
   - The provided white paper emphasizes the importance of using `exit();` or `die();` after redirecting in PHP to prevent further script execution.

3. **Hypothesis:**
   - The challenge might involve a scenario where the `redirect` parameter is used to redirect the user, but the script continues to execute sensitive code afterward.

4. **Exploitation Steps:**

   - **Bypassing Browser Redirects:**  Use Burp Suite's Repeater tool to send modified requests and observe raw server responses, as the browser would automatically follow redirects, masking the vulnerability.

   - **Crafting the Exploit:**
     1. Modify the initial GET request to target `index.php` instead of `login.php`, but keep the `redirect` parameter:
        ```
        GET /web-serveur/ch32/index.php?redirect HTTP/1.1
        ``` 
     2. Send this request through Burp Suite's Repeater.

5. **Results:**
   - The server responds with a 302 redirect (`Location: ./login.php?redirect`), as expected.
   - **Crucially, the response also includes the HTML content of `index.php`, which contains the challenge flag!** This confirms that the script continued executing after the redirect.

**Code Analysis (Hypothetical):**

While we don't have the exact source code, the behavior suggests the following logic in the PHP script:

```php
<?php
// ... (some logic, maybe checking for a login session)

// Redirect the user (but don't exit)
if (isset($_GET['redirect'])) {
    header("Location: " . $_GET['redirect']); 
} 

// ... (sensitive code that should only be accessible after authentication)
// This is where the flag and other content from index.php would be.
?>
```

**Key Takeaways:**

- **Always Terminate After Redirects:** In PHP (and many other languages), use `exit();` or `die();` immediately after issuing a redirect (`header('Location: ...');`) to prevent vulnerabilities. 
- **Beware of User-Controlled Redirects:** Carefully validate and sanitize any user-supplied input used in redirects to prevent open redirect vulnerabilities, which can be chained with improper redirect vulnerabilities for greater impact.
- **Test with Raw Responses:** Tools like Burp Suite's Repeater are essential for uncovering vulnerabilities masked by the browser's default behavior.

**Remediation:**

- **Add `exit();`:** The primary fix is to simply add `exit();` immediately after the `header('Location: ...');` line in the vulnerable code.
- **Code Review and Security Testing:**  Regularly review code for improper redirect vulnerabilities and perform thorough security testing, including using a web proxy to analyze requests and responses. 
