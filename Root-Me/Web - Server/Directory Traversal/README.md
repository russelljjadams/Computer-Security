## Root-Me.org Challenge Write-Up: Directory Traversal
`https://www.root-me.org/en/Challenges/Web-Server/Directory-traversal`

**Challenge Description:** This challenge aims to expose a common web security vulnerability known as Directory Traversal. The goal is straightforward: "Find the hidden section of the photo gallery."

**Understanding Directory Traversal:**

Before we dive into the solution, it's crucial to grasp the underlying concept of directory traversal vulnerabilities.  These vulnerabilities exploit flaws in how a web application handles user-supplied input when constructing file paths on the server.  

Imagine a scenario where a web application uses a parameter in the URL to determine which image to display from a directory on the server. A typical URL might look like this:

```
https://www.example.com/images?image=cute_kitten.jpg
```

The server takes the value from the `image` parameter (`cute_kitten.jpg`) and appends it to the base path (`/images/`) to fetch and display the requested image.

Now, consider what happens if an attacker modifies the URL to include directory traversal sequences like `../`:

```
https://www.example.com/images?image=../../../../etc/passwd
```

If the application fails to sanitize the user input properly, the server might interpret this manipulated URL as a command to navigate up multiple directory levels (using `../`) and access the sensitive system file `/etc/passwd`. 

**Exploitation Steps:**

1. **Initial Probe:** Start by accessing the challenge URL, which will likely follow a similar structure:

   ```
   http://challenge01.root-me.org/web-serveur/ch15/ch15.php?galerie=categories 
   ```

   This initial URL might load a default view of the photo gallery. 

2. **Testing for Directory Traversal:**  Attempt to manipulate the URL by replacing the value of the vulnerable parameter (in this case, `galerie`) with a single forward slash `/`. This technique instructs the server to navigate one directory level up from the intended directory:

   ```
   http://challenge01.root-me.org/web-serveur/ch15/ch15.php?galerie=/ 
   ```

3. **Identifying Hidden Content:** If the server is susceptible to directory traversal, you might encounter a listing of files and directories that were not meant to be publicly accessible.  

4. **Spotting Anomalies:**  Examine the directory listing or any displayed content for unusual or unexpected file names. These anomalies could hold the key to uncovering hidden sections of the application. In this specific challenge, a file or directory with an uncommon name like `86hwnX2r` might stand out.

5. **Manipulating the Path:** Append the identified anomaly to the URL, aiming to access its contents:

   ```
   http://challenge01.root-me.org/web-serveur/ch15/ch15.php?galerie=86hwnX2r/
   ```

   If successful, this might grant you access to the hidden section or reveal further clues. 

6. **Unveiling the Flag:** Continue to explore the revealed directory. The challenge objective often involves finding a specific file, such as `password.txt`, which typically contains the flag or sensitive information.

**Automating Directory Traversal with Burp Suite:**

Burp Suite, a powerful web security testing tool, can significantly streamline the process of discovering and exploiting directory traversal vulnerabilities. 

1. **Intercepting the Request:**  Configure Burp Suite as your browser's proxy and initiate a request to the target URL. 

2. **Sending to Intruder:** Within Burp Suite, forward the intercepted request to the "Intruder" tool.

3. **Setting Attack Parameters:**  Highlight the vulnerable parameter in the request (e.g., `galerie=categories`) and mark it as a payload position.

4. **Configuring Payloads:** Create a payload list containing common directory traversal sequences (e.g., `../`, `....//`, `%2f..%2f`, etc.). You can find pre-made lists online (also included) or within Burp Suite's payload options. 

5. **Launching the Attack:** Initiate the attack. Burp Suite will send multiple requests, each with a different traversal sequence, and analyze the responses for clues of successful exploitation, such as changes in HTTP status codes, content length, or error messages.

**Remediation:**

The most effective way to prevent directory traversal vulnerabilities is to implement robust input validation and sanitization:

- **Whitelist Allowed Values:** When possible, restrict user input to a predefined set of allowed values or patterns.
- **Neutralize Traversal Sequences:**  Sanitize user input to remove or escape potentially dangerous characters, such as `.` and `/`, or URL-encode them to prevent misinterpretation.
- **Validate File Paths:** Before accessing any file on the server, verify that the constructed path falls within the intended application directory.

**Conclusion:**

Directory traversal vulnerabilities, though potentially severe, can be mitigated with secure coding practices. By understanding the mechanics of this attack vector and employing the outlined remediation steps, developers can fortify their applications and safeguard sensitive data from unauthorized access. 
