## Root-Me.org Challenge Write-Up: File Upload - Null Byte
`https://www.root-me.org/en/Challenges/Web-Server/File-upload-Null-byte`

**Challenge Description:** This challenge focuses on a common yet potentially dangerous vulnerability: insecure file upload handling.  The objective is clear: "Your goal is to hack this photo gallery by uploading PHP code."

**Understanding Null Byte Injection:**

Before delving into the solution, let's dissect the vulnerability that makes this exploit possible: null byte injection.

In many programming languages, a null byte (`%00` when URL encoded) is interpreted as the end of a string. This seemingly innocuous character can have significant security implications when combined with inadequate input validation, particularly in file upload functionalities.

Consider a web application that allows users to upload images but aims to restrict file types to prevent the execution of malicious code. It might achieve this by checking the file extension provided in the request.  

However, if the application uses a null byte to mark the end of the file name during processing, an attacker could potentially bypass this restriction.  By injecting a null byte before an allowed extension (e.g., `malicious.php%00.jpeg`), they could trick the application into accepting the file.  The server, upon encountering the null byte, might prematurely truncate the file name, treating it as `malicious.php` and potentially storing it in a location where PHP files are executed. 

**Exploitation Steps:**

1. **Identifying the Upload Point:** Explore the challenge environment to locate the file upload functionality. In this case, the challenge description mentions a photo gallery with an "upload" link, likely leading to an upload form.

2. **Preparing the Malicious File:** Create a simple PHP file (e.g., `exploit.php`) containing code to achieve the desired outcome.  In a real-world scenario, this might involve creating a backdoor, stealing sensitive information, or defacing the website. For this challenge it doesn't seem like it matters, any PHP code will do. It's just about bypassing the filters to upload the php file.

3. **Initiating the Upload:** Begin uploading the malicious PHP file using the provided form.

4. **Intercepting the Request:** Capture the upload request using a web proxy like Burp Suite before it reaches the server. 

5. **Injecting the Null Byte:** Within the intercepted request, locate the parameter containing the uploaded file's name. Modify the filename by injecting `%00` followed by an allowed extension (e.g., `.jpeg`) before the original extension:

   ```
   Original:  exploit.php
   Modified:  exploit.php%00.jpeg
   ```

6. **Masking the Content Type:** To further evade detection, modify the `Content-Type` header in the request to match the allowed file type. In this scenario, change it from something like `application/x-php` to `image/jpeg`.

7. **Forwarding the Modified Request:** Send the manipulated request to the server. If the vulnerability exists, the application might accept your file, treating it as a JPEG image due to the null byte truncation.

8. **Triggering the Payload:**  Access the uploaded file through the web application (e.g., by navigating to the photo gallery).  If the exploit is successful, your PHP code will be executed.

**Remediation:**

Preventing null byte injection vulnerabilities in file upload functionalities requires stringent security measures:

- **Robust File Type Validation:** Do not solely rely on file extensions or content type headers, as these can be easily manipulated. Implement robust file type validation using techniques like magic number detection (inspecting the file's binary header) or utilizing external libraries specifically designed for secure file type validation.

- **Whitelist Approach:**  Instead of blacklisting specific file extensions, adopt a whitelist approach, explicitly allowing only known safe file types.

- **Safe File Naming:** Avoid using user-supplied file names directly.  Generate a unique, sanitized file name on the server-side to prevent any malicious manipulation of file paths.

- **Secure File Storage:**  Store uploaded files in a directory inaccessible directly through the web browser.  Serve the files through a separate script that enforces appropriate access controls.

**Conclusion:**

The "File Upload - Null Byte" challenge highlights the critical need for developers to handle file uploads with utmost security in mind. By understanding and mitigating vulnerabilities like null byte injection, developers can significantly enhance the security posture of their web applications, protecting them from potentially devastating attacks. 
