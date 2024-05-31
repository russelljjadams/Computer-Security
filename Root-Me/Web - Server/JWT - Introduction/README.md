## Root-Me.org Challenge Write-Up: JWT - Introduction
`https://www.root-me.org/en/Challenges/Web-Server/JWT-Introduction`

**Challenge Description:** The "JWT - Introduction" challenge on Root-Me.org tasks us with bypassing the authentication mechanism to gain access as an administrator. We are presented with a login form and a "Login as Guest" button. The objective is clear: elevate our privileges to "admin."

**Understanding the Vulnerability: JWT Algorithm Manipulation**

At the heart of this challenge lies a subtle yet impactful vulnerability within the realm of JSON Web Tokens (JWT). JWTs have become a cornerstone of modern web application security, providing a standardized and secure method for transmitting information between parties.  They consist of three core parts:

- **Header:**  Contains information about the token type and the hashing algorithm used.
- **Payload:**  Carries the claims, which are statements about an entity (typically, the user) and their permissions.
- **Signature:**  Ensures the integrity of the token, verifying that it hasn't been tampered with.

The vulnerability exploited in this challenge stems from the fact that the JWT's header often specifies the algorithm used for signing. While this seems innocuous, problems arise when the server blindly trusts the algorithm specified in the header, even if it originates from an untrusted source (the client).

**Exploitation Steps:**

1. **Intercepting the JWT:**
   - Begin by logging in as a guest. This action generates a JWT, which is often stored in your browser's cookies or transmitted within the request headers.
   - Using a web proxy like Burp Suite, intercept the HTTP request containing the JWT.

2. **Analyzing the JWT:**
   - Copy the intercepted JWT.
   - Utilize a JWT parsing tool (many are available online) or a Burp Suite extension like "JWT Editor" to decode the JWT and reveal its header, payload, and signature. To install the extension, refer to the official guide: [https://portswigger.net/burp/documentation/desktop/extensions/installing-extensions](https://portswigger.net/burp/documentation/desktop/extensions/installing-extensions). 

3. **Modifying the Algorithm:**
   - Working with JWT's in Burp Suite >>> `https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts`
   - Within the JWT header, locate the `alg` parameter. This parameter dictates the signing algorithm used by the server to verify the token's integrity.
   - The challenge often relies on a weak or misconfigured server that accepts arbitrary algorithm values. 
   - Experiment by changing the `alg` value to "none" (which indicates no signing at all). In some scenarios, you might even need to bypass weak filters by modifying the casing, such as "nOnE".

4. **Modifying the Payload:**
   - While we have disabled the signature verification by tampering with the `alg` parameter, the server might still rely on the payload to determine user roles or permissions.
   - Within the JWT payload, locate the parameter that governs user roles or privileges (e.g., "role", "isAdmin", "user").
   - Change this parameter's value to "admin" or any other value that signifies administrative privileges.

5. **Forwarding the Modified Request:**
   -  Reassemble the modified JWT, ensuring the header and payload reflect your changes.  The signature is now irrelevant as we've effectively disabled its verification.
   -  Forward the modified request through Burp Suite.

6. **Observing the Results:**
   -  If the server is vulnerable, it will accept the manipulated JWT at face value, granting you access as an administrator, and you will successfully obtain the flag.

**Remediation:**

Preventing JWT algorithm manipulation vulnerabilities demands a multi-pronged approach:

- **Server-Side Validation:**  Implement robust server-side checks to validate the `alg` parameter against a whitelist of approved and secure algorithms.  Do not rely solely on client-supplied data.

- **Algorithm Specificity:** When generating JWTs, explicitly specify the desired algorithm within your server-side code to prevent any ambiguity or potential for manipulation.

- **Disable "none" Algorithm:**  Ensure that your JWT library or implementation has the `none` algorithm explicitly disabled. This is often an option within configuration settings.

- **Up-to-Date Libraries:**  Regularly update your JWT libraries and dependencies to patch known vulnerabilities. Security best practices evolve constantly, and keeping your tools updated is crucial.

**Additional Resources:**

- **PortSwigger Web Academy on JWT Attacks:** [https://portswigger.net/web-security/jwt](https://portswigger.net/web-security/jwt) 

**Conclusion:**

The "JWT - Introduction" challenge provides a valuable lesson in the critical importance of securing every facet of JWT implementation. While JWTs offer a robust security mechanism, failing to properly validate the algorithm used for signing can create a gaping hole, potentially granting unauthorized access to sensitive data or system functionality. By understanding this vulnerability and implementing the outlined remediation steps, developers can fortify their applications against such attacks. 
