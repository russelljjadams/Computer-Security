## Root-Me.org Challenge Write-Up: JWT - Header Injection

**Challenge Description:** The "JWT - Header Injection" challenge confronts us with the enigmatic Keymaster who guards access to his domain.  Our mission: decipher the cryptic hints, "Give him the right key" and "The Keymaster now has his own site. He will only let you in if you give him the right secret and key," to unlock the secrets within.

**Initial Reconnaissance:**

Upon navigating to the challenge URL (likely `http://challenge01.root-me.org:59082/key`), we're likely presented with a login form. Intercepting the initial GET request using Burp Suite reveals an example JWT key.

**Exploiting Header Injection:**

The challenge hints suggest that we need to manipulate the JWT to gain access. However, simple payload modification won't suffice. The crux of this challenge lies in **injecting our own public key into the JWT header**.

**Exploitation Steps:**

1. **Burp Suite Setup:**
   - **Install JWT Editor:** Enhance Burp Suite's capabilities by installing the "JWT Editor" extension from the BApp store. This extension provides invaluable tools for crafting and analyzing JWTs.
   - **Intercept Initial Request:** Use Burp Suite to intercept the GET request to the login page and copy the provided example JWT key.

2. **Login Attempt and Key Generation:**
   - **Submit Example Key:** Enter the copied JWT key into the login form and intercept the resulting POST request with Burp Suite.
   - **Send to Repeater:**  Forward the intercepted request to Burp's Repeater tool for further manipulation.
   - **Generate RSA Key Pair:** In Burp's main tab bar, navigate to the "JWT Editor Keys" tab. Click "New RSA Key," then "Generate" to create a new RSA key pair. Save the key.

3. **JWT Manipulation:**
   - **Modify Payload:** In Burp Repeater, switch to the "JSON Web Token" tab (provided by the JWT Editor extension). Within the payload, change the `user` parameter from its default value (e.g., "Trinity") to the desired target user (e.g., "Neo").
   - **Inject Public Key:** At the bottom of the "JSON Web Token" tab, click "Attack" and select "Embedded JWK." Choose your newly generated RSA key when prompted.  Observe that a `jwk` (JSON Web Key) parameter has been added to the JWT header, containing your public key.

4. **Claiming Victory:**
   - **Send the Request:**  Forward the manipulated request containing the modified payload and injected public key.
   - **Observe the Outcome:** If the exploit is successful, the server will use your provided public key to verify the JWT signature, granting you access as the target user ("Neo" in this case).  The flag or password should now be revealed. 

**Understanding the Vulnerability:**

This challenge exploits a weakness in how some JWT implementations handle key management. 

- **Blind Trust in `jwk`:**  The vulnerable server likely blindly trusts the public key provided in the `jwk` header without validating its origin or association with a legitimate user. 
- **Key Confusion:** By injecting our own public key, we effectively replace the server's intended key with ours.  The server then uses our key to verify a signature that we've crafted, granting us unauthorized access.

**Remediation:**

- **Secure Key Management:** Implement robust key management practices. Avoid relying solely on client-supplied keys for signature verification.
- **Key Validation:**  Validate `jwk` values against a whitelist of trusted keys or use a dedicated key management system to securely store and retrieve keys.
- **Principle of Least Privilege:** Ensure that user roles and permissions are properly enforced to limit the impact of successful header injection attacks.

**Conclusion:**

The "JWT - Header Injection" challenge highlights the importance of securing all aspects of JWT implementations. Failing to validate and manage keys securely can create a significant vulnerability, potentially allowing attackers to bypass authentication and gain unauthorized access. By understanding this vulnerability and employing the recommended remediation steps, developers can build more resilient applications and protect against such attacks. 
