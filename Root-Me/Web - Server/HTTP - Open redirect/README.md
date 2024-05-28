## Root-Me.org Challenge Write-Up: HTTP - Open Redirect 

**Challenge Description:** This challenge delves into exploiting an "Open Redirect" vulnerability, but with an added layer of security. The challenge page displays three buttons leading to social media sites (Facebook, Twitter, and Slack) with URLs structured as follows: `http://challenge01.root-me.org/web-serveur/ch52/?url=https://facebook.com&h=a023cfbf5f1c39bdf8407f28b60cd134`

**Vulnerability Explanation:** An Open Redirect vulnerability arises when a web application, instead of properly validating and sanitizing a user-provided URL, accepts it and redirects the user to that URL. This vulnerability can be exploited to redirect users to potentially malicious websites designed for activities like phishing or malware distribution. 

**Exploitation Steps:**

1. **Deconstructing the URL:** The provided URL utilizes two key parameters:
    - `url`: This parameter contains the intended target URL for redirection (e.g., `https://facebook.com`).
    - `h`: This parameter houses an MD5 hash of the complete URL specified in the `url` parameter. This hash acts as a basic security measure to prevent trivial URL manipulation.

2. **Generating the Correct Hash:**  Let's assume we aim to force a redirect to `https://www.yahoo.com`.  To do this, we need the MD5 hash of this entire URL. Utilizing readily available online MD5 hash generators (search for "MD5 hash generator" in your search engine), we find the hash for `https://www.yahoo.com` is `99e8a2cb4638bb798cf9167e5af5b83b`.

3. **Crafting the Exploit URL:** Now, construct the complete malicious URL:
    ```
    http://challenge01.root-me.org/web-serveur/ch52/?url=https://www.yahoo.com&h=99e8a2cb4638bb798cf9167e5af5b83b
    ```

4. **Observing the Redirect:** When this crafted URL is accessed, the application will verify the hash against the provided URL. If they match, the redirect to `https://www.yahoo.com` will occur.

**Remediation:**

While the MD5 hash adds a layer of complexity, it doesn't eliminate the inherent Open Redirect vulnerability. Developers should adopt these practices:

* **Minimize reliance on user-provided data for redirects.** If unavoidable, implement rigorous validation.
* **Whitelist approved domains** for redirection.  Only allow redirects to URLs matching the whitelist.
* **Transition to more robust hashing algorithms** like SHA-256 or stronger, as MD5 is considered cryptographically broken.
* **Employ security headers** such as `X-Frame-Options` and `Content-Security-Policy` to restrict how the application can be embedded and mitigate potential attack vectors.
* **Educate users** about the dangers of clicking on suspicious links, regardless of their apparent source.

**Conclusion:**

The addition of an MD5 hash in this challenge highlights that even seemingly simple security measures can be bypassed. By understanding the mechanics of the vulnerability and following recommended remediation steps, developers can significantly enhance the security of their applications and protect users from falling victim to Open Redirect attacks. 
