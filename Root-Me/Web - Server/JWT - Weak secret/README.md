## Root-Me.org Challenge Write-Up: JWT - Weak Secret
`https://www.root-me.org/en/Challenges/Web-Server/JWT-Weak-secret`

**Challenge Description:**  The "JWT - Weak Secret" challenge throws down the gauntlet, daring us to breach its seemingly secure API and uncover its "most valuable secrets." We're greeted with a seemingly innocuous `/hello` endpoint, but the challenge description hints at a deeper game afoot.

**Initial Reconnaissance:**

Accessing the challenge URL (`http://challenge01.root-me.org/web-serveur/ch59/hello`) presents us with a simple JSON message:

```json
{
  "message": "Let's play a small game, I bet you cannot access to my super secret admin section. Make a GET request to /token and use the token you'll get to try to access /admin with a POST request."
}
```

Following the instructions, a GET request to `/token` yields a JWT:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiZ3Vlc3QifQ.4kBPNf7Y6BrtP-Y3A-vQXPY9jAh_d0E6L4IUjL65CvmEjgdTZyr2ag-TM-glH6EYKGgO3dBYbhblaPQsbeClcw
```

Attempting to access `/admin` with a POST request using this token results in a message taunting our inability to "break [the] super crypto" and revealing the use of the HS512 algorithm.

**Exploiting the Weak Secret:**

The challenge hints at a weak secret used for signing the JWT. This presents an opportunity to employ a brute-force attack using a tool like John the Ripper to uncover the secret key.

1. **Preparing the JWT for Cracking:** Save the obtained JWT to a text file (e.g., `jwt.txt`).

2. **Leveraging John the Ripper:** Use the following command to initiate the cracking process, specifying the appropriate hashing algorithm (HMAC-SHA512) and a wordlist:
   `https://blog.pentesteracademy.com/hacking-jwt-tokens-bruteforcing-weak-signing-key-johntheripper-89f0c7e6a87`

   ```
   john jwt.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=HMAC-SHA512 
   ```

   - **Note:**  The `rockyou.txt` wordlist, while often effective, might not contain the specific secret. Consider using more comprehensive wordlists or generating custom lists based on potential patterns hinted at in the challenge.

3. **Obtaining the Secret Key:**  John the Ripper efficiently cracks the weak secret, revealing the key used to sign the JWT.

**Crafting a Privileged JWT:**

Possessing the secret key is only half the battle. We need to modify the JWT's payload to grant us administrative access.  Here's how to do it using the terminal:

1. **Extract and Decode the Payload:** Copy the payload section of the JWT (the middle part between the two dots). Then, use the following command to decode it:

   ```bash
   echo "eyJyb2xlIjoiZ3Vlc3QifQ" | base64 -d
   ```

   This will output the decoded payload, likely something like: `{"role":"guest"}`

2. **Modify the Role:** Edit the decoded payload, changing the role to "admin":

   ```json
   {"role":"admin"}
   ```

3. **Re-encode the Payload:** Pipe the modified payload back into base64 to encode it:

   ```bash
   echo '{"role":"admin"}' | base64
   ```

   This will output the re-encoded payload, for example: `eyJyb2xlIjoiYWRtaW4ifQ==`

4. **Reconstruct the JWT:**  Replace the original payload section of the JWT with the newly encoded "admin" payload. 

**Resigning and Using the JWT:**

1. **Resigning:**  Head over to a site like `https://jwt.io/`, paste your reconstructed JWT, input the cracked secret key, and have the site generate a new valid signature.

2. **Claiming Victory:** Armed with the newly signed JWT, containing the "admin" role, submit a POST request to the `/admin` endpoint. The server, now tricked into believing we possess legitimate administrative privileges, will grant access to the protected resource, revealing the coveted flag.

**Remediation:**

This challenge underscores the critical importance of strong secret keys in JWT implementations:

- **Robust Key Generation:**  Employ cryptographically secure random number generators to create strong, unpredictable secret keys.

- **Key Rotation:** Periodically rotate secret keys to limit the impact of compromised keys.

- **Rate Limiting:** Implement rate limiting on JWT authentication endpoints to hinder brute-force attacks.

- **Intrusion Detection:** Utilize intrusion detection systems to identify and respond to suspicious activities, such as an abnormally high volume of authentication requests. 

**Conclusion:**

The "JWT - Weak Secret" challenge serves as a stark reminder that even seemingly robust security mechanisms like JWT can be compromised if fundamental principles, such as the use of strong and properly managed secret keys, are neglected. By adopting a proactive and multi-layered security approach, developers can strengthen their applications against these ever-present threats. 
