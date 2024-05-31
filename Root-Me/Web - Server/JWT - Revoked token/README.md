## Root-Me.org Challenge Write-Up: JWT - Revoked Token
`https://www.root-me.org/en/Challenges/Web-Server/JWT-Revoked-token`

**Challenge Description:** This challenge presents an intriguing twist on the concept of JSON Web Token (JWT) security.  Instead of typical vulnerabilities like algorithm manipulation, we're faced with a scenario where tokens are seemingly revoked immediately upon creation.  Our mission:  outsmart the system and gain access to the `/admin` route.

**Understanding the Challenge:**

The challenge provides us with the application's source code, offering valuable insights into its inner workings. Here's a breakdown of the key elements:

- **Login Endpoint (`/login`):**  Accepts username and password credentials, generating and returning a JWT upon successful authentication.
- **Admin Endpoint (`/admin`):**  Protected by the `@jwt_required` decorator, requiring a valid JWT for access.
- **Token Revocation:** A `blacklist` set is used to store revoked tokens.  Critically, the login endpoint adds the generated JWT to this blacklist *immediately*.
- **Background Token Cleanup:** A background task periodically removes expired tokens from the `blacklist`.

**Initial Hurdle: Obtaining a Valid Token**

The first step is to acquire a JWT. Sending a properly formatted POST request to `/login` with the credentials `"admin:admin"` will yield a token:

```
POST /web-serveur/ch63/login HTTP/1.1
Host: challenge01.root-me.org
Content-Type: application/json 

{"username":"admin","password":"admin"} 
```

However, attempting to access `/admin` using this token in the `Authorization` header will result in a "Token is revoked" message due to the immediate blacklisting.

**Unveiling the Vulnerability: Base64 Padding and Strict Comparison**

A meticulous examination of the source code and the behavior of base64 encoding unveils the vulnerability:

1. **Base64 Padding:** Base64 encoding often uses `=` characters for padding to ensure the encoded data aligns with byte boundaries.  Trailing `=` characters are sometimes omitted if the encoded data length is already a multiple of 4.

2. **Strict Blacklist Comparison:** The application likely performs a strict string comparison when checking if a token is present in the `blacklist`.  This means a token with padding (`ey...token...=`) is considered distinct from its unpadded counterpart (`ey...token`).

**The Exploit: Appending the Padding Character**

The exploit capitalizes on this discrepancy:

1. **Obtain a Token:**  Send the POST request to `/login` to get a JWT.

2. **Append the `=`:** Simply add an `=` character to the end of the received JWT.

3. **Bypass the Blacklist:**  The modified token, now with padding, won't match the unpadded version stored in the `blacklist`, allowing you to bypass the revocation mechanism.

**Constructing the Successful GET Request:**

```
GET /web-serveur/ch63/admin HTTP/1.1
Host: challenge01.root-me.org
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MTcxNzU0OTMsIm5iZiI6MTcxNzE3NTQ5MywianRpIjoiM2E0MTQ4YTgtZDA4NS00ODZkLWIzMjktMDQ5NDIzNjg5ZDQyIiwiZXhwIjoxNzE3MTc1NjczLCJpZGVudGl0eSI6ImFkbWluIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.Fev4GbW6YcW6vmroje7vqZ1WMX679DQjnH-I9e3gqXY= 
```

**Remediation:**

To prevent this vulnerability, the application should normalize JWT tokens before performing blacklist checks. This can be achieved by:

- **Stripping Trailing Padding:** Removing any trailing `=` characters from the token before comparison.
- **Canonicalization:** Using a JWT library or function to convert tokens into a standardized (canonical) form, ensuring consistent representation regardless of padding variations.

**Key Takeaways:**

- **Subtlety of Security Flaws:**  This challenge highlights how seemingly minor details like base64 padding, combined with application logic oversights, can lead to exploitable vulnerabilities.
- **Importance of Data Encoding:** Understanding data encoding mechanisms and potential inconsistencies is crucial for identifying and mitigating security risks. 
- **Value of Source Code Review:** Access to source code provides invaluable insights into application behavior and can reveal vulnerabilities that might not be apparent through black-box testing alone. 
