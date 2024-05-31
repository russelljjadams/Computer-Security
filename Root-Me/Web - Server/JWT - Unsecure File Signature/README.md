## Root-Me.org Challenge Write-Up: JWT - Unsecure File Signature 
`https://www.root-me.org/en/Challenges/Web-Server/JWT-Unsecure-File-Signature`

**Challenge Description:** The "JWT - Unsecure File Signature" challenge pits us against a rogue ex-administrator who has replicated the Root-Me website and hidden flags within its depths. Our task: exploit the site's flawed JWT implementation to uncover these hidden treasures.  The hints "(K)ind (I)dentification (D)ance" and the administrator's penchant for replicating the site will be instrumental in our quest.

**Initial Observations and Deductions:**

- **JWT Authentication:** The challenge clearly revolves around manipulating JWTs to gain unauthorized access.
- **Invalid Signature:** Simply changing the payload's content and re-encoding it triggers an "invalid signature" error. This means we need to decipher and circumvent the server's JWT verification process.
- **Focus on `kid`:** The hint "(K)ind (I)dentification (D)ance" strongly suggests that the vulnerability lies within the `kid` (Key ID) parameter of the JWT header.

**Unveiling the "Unsecure File Signature" Vulnerability:**

The challenge's name provides a significant clue: "Unsecure File Signature." This implies that the server handles the `kid` parameter insecurely during the signature verification process, likely involving a flawed file system interaction.

Here's a breakdown of the likely vulnerability:

1. **`kid` as File Path:** The server likely constructs a file path to locate the signing key based directly on the `kid` value received in the JWT header.
2. **Inadequate Sanitization:**  Critically, the server fails to properly sanitize or validate the `kid`, allowing for path traversal and other potentially dangerous path manipulation techniques.
3. **Blind Trust in File Existence:** The server might blindly assume that if a file exists at the constructed path, even if manipulated, it must contain a valid signing key.

**Exploiting `/dev/null` to Bypass Signature Verification:**

The breakthrough in solving this challenge lies in leveraging the `/dev/null` special file to our advantage:

1. **Crafting the `kid`:**  Set the `kid` parameter to `....//....//....//....//....//....//....//dev/null`. The repetitive `../` sequences, while potentially subject to server-side truncation, aim to traverse up the directory structure to reach the `/dev/` directory, where `/dev/null` resides. 
2. **The Magic of `/dev/null`:**  In Unix-like systems, `/dev/null` acts as a "black hole" or "null device." Any data written to it vanishes, and reading from it always returns an empty result. 
3. **Tricking the Server:** By manipulating the `kid` to point to `/dev/null`, the server, in its attempt to load the signing key from the constructed path, effectively reads an empty key from this special file. 
4. **Signature Check Disabled:** With an empty key, the server's signature verification mechanism is rendered useless. Any signature (or even a missing one) will be considered valid.

**Exploitation Steps:**

1. **Obtain the JWT:** Capture the initial JWT token provided by the application.
2. **Craft the Malicious `kid`:** Set the `kid` parameter to `....//....//....//....//....//....//....//dev/null`. 
3. **Modify the Payload:** Alter the JWT payload to grant yourself administrative privileges (e.g., change `"user": "guest"` to `"user": "admin"`).
4. **Resign (Or Not):** Since signature verification is bypassed, you have two options:
   - **Resign with a Blank Key:**  Use a JWT tool to resign the modified JWT using a blank secret key. `https://jwt.io/`
   - **Skip Resigning:**  Some implementations might not even require a signature at this point.
5. **Access `/admin`:** Send the manipulated JWT to the vulnerable `/admin` endpoint and claim your hard-earned flag!

**Remediation:**

- **Secure Key Storage:**  Never store secret keys directly within the file system, especially not in locations accessible via user-controlled input.
- **Whitelist `kid` Values:**  Enforce a strict whitelist of allowed `kid` values to prevent path traversal or other manipulation techniques.
- **Robust Key Management:** Employ a secure key management system or library to handle key storage, retrieval, and rotation securely.

**Conclusion:**

The "JWT - Unsecure File Signature" challenge masterfully demonstrates the serious consequences of insecurely handling file system interactions based on user-supplied data. It emphasizes the critical need for:

- **Thorough Input Sanitization:**  Always sanitize and validate all user input before using it in any server-side operations, especially those involving the file system.
- **Understanding System Quirks:**  Knowledge of system-specific features and potential vulnerabilities, such as the behavior of `/dev/null`, is crucial for both attackers and defenders. 
- **Defense-in-Depth:** Implement multiple layers of security to protect against common vulnerabilities and mitigate the impact of successful attacks. 

By internalizing these lessons and adopting a proactive security mindset, developers can fortify their applications and safeguard sensitive data from exploitation. 
