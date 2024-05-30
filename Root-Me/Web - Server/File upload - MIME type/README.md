## Root-Me.org Challenge Write-Up: Web Server - File Upload - MIME Type
`https://www.root-me.org/en/Challenges/Web-Server/File-upload-MIME-type?lang=en`

This write-up dissects the "File Upload - MIME Type" challenge on Root-Me.org, highlighting the importance of thorough file upload validation and showcasing a simple yet effective bypass technique.

### Challenge Description

Similar to the "Double Extensions" challenge, the objective here is to exploit a file upload mechanism to gain unauthorized access to sensitive data – specifically, the contents of a `.passwd` file located at the root of the application.

### Vulnerability: MIME Type Validation Bypass

This challenge emphasizes the significance of verifying both the declared MIME type (Content-Type header) and the actual content of uploaded files.  While checking the MIME type is essential, it's not sufficient to prevent malicious uploads if the server doesn't inspect the file's content to confirm the declared type.

### Exploitation: Manipulating the Content-Type Header

The core vulnerability lies in the application trusting the `Content-Type` header without verifying the actual file content. We can exploit this by:

1. **Crafting the Payload:** We create a PHP file named `exploit.php` (no need for a double extension in this case) containing code to traverse the server's directory structure and retrieve the `.passwd` file. The PHP code is identical to the one used in the "Double Extensions" challenge.

2. **Modifying the Request:** Using an intercepting proxy like Burp Suite, we capture the file upload request.  Within the request body (specifically within the multipart/form-data boundary), we locate the line:
   ```
   Content-Type: application/x-php 
   ``` 
   and change it to:
   ```
   Content-Type: image/jpeg
   ```

3. **Uploading and Exploiting:**  We forward the modified request to the server. Since the application relies solely on the `Content-Type` header, it processes our uploaded PHP file as a JPEG image, bypassing the intended security measure. Accessing the uploaded file's URL then executes our PHP code, granting us access to the `.passwd` file.

### Security Implications and Remediation

This challenge demonstrates that relying solely on MIME type validation for file uploads is a critical vulnerability. Attackers can easily manipulate HTTP headers to bypass such checks while uploading malicious files.

To mitigate this risk, developers should implement multi-layered file upload security:

- **Content Inspection:**  Thoroughly analyze the contents of uploaded files to ensure they match the declared MIME type. This often involves examining file signatures, magic bytes, and performing structural analysis.
- **Whitelist Validation:** Only allow uploads of files with specific, pre-approved extensions, regardless of the declared MIME type.
- **MIME Type Verification (Secondary Check):**  While not foolproof, verifying the MIME type can act as an initial layer of defense.
- **Unique Filenames:**  Generate random and unique filenames for uploaded files to prevent attacks that rely on predictable filenames.
- **Secure Storage:** Store uploaded files outside the webroot directory to prevent direct access through a web browser.

By implementing these robust security measures, developers can significantly reduce the risk associated with file upload functionality and protect their applications from malicious exploitation. 
