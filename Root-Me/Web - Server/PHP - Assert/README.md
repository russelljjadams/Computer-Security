## Root-Me.org Challenge Write-Up: PHP - Assert
`https://www.root-me.org/en/Challenges/Web-Server/PHP-assert`

**Challenge Description:** This challenge tasks us with uncovering the contents of the `.passwd` file, hinting at a vulnerability related to the use of PHP's `assert()` function.

**Initial Probe and Vulnerability Identification:**

Begin by attempting a standard Local File Inclusion (LFI) attack, aiming to directly include the target file:

```
http://challenge01.root-me.org/web-serveur/ch47/?page=../../../etc/passwd
```

The server responds with an error message:

```
Warning: assert(): Assertion "strpos('includes/../../../etc/passwd.php', '..') === false" failed in /challenge/web-serveur/ch47/index.php on line 8 Detected hacking attempt!
```

This reveals crucial information:

- **`assert()` Usage:** The application uses `assert()` for input validation, specifically to check for directory traversal attempts (`..`). 
- **Potential for Bypass:** The error message suggests that if we can manipulate the assertion logic itself, we might be able to bypass the security check.

**Exploiting `assert()` for Blind LFI:**

The key to solving this challenge lies in understanding the insecure nature of using `assert()` for security-critical checks and then leveraging it for our benefit.

**Understanding the Risk:**

- **Disabled in Production:** `assert()` is often disabled in production environments, rendering the check useless.
- **Dynamic Code Execution:**  More critically, `assert()` can dynamically execute PHP code embedded within the assertion string. 

**How the Exploit Works: The URL as a Code Injection Vector**

The vulnerable application likely uses a URL parameter, such as `page`, to dynamically include files server-side. The attacker can exploit this by injecting PHP code directly into this parameter. For instance:

```
http://challenge01.root-me.org/web-serveur/ch47/?page=', 'qwer') === false && strlen(file_get_contents('.passwd')) == 1234 && strpos('1
```

Let's break down how this malicious URL works:

1. **Exploiting the `page` Parameter:** The attacker modifies the `page` parameter to include their injected code. 
2. **Bypassing Initial Validation:** The portions before the first `&&` (`', 'qwer') === false`) and after the second `&&` (`strpos('1`) are designed to either evaluate as `TRUE` or be incomplete, ensuring they don't interfere with the intended payload. 
3. **Injecting the Assertion:** The core of the exploit lies within the middle section: `strlen(file_get_contents('.passwd')) == 1234`. This is the PHP code that gets executed by the flawed `assert()` statement.

**Crafting Assertions for Blind Information Disclosure:**

The attacker crafts PHP code that checks for specific conditions related to the target file (`.passwd` in this case) without directly retrieving its content. These checks are embedded within the injected `assert()` statement. Here are some examples:

1. **Checking File Length:**

   ```php
   strlen(file_get_contents('.passwd')) == 1234 
   ```

   - This assertion evaluates to `TRUE` if the length of `.passwd` is exactly 1234 bytes. 
   - The server's response (whether it includes an `assert()` error or not) reveals if the condition was met.

2. **Checking a Specific Character:**

   ```php
   ord(substr(file_get_contents('.passwd'), 0, 1)) == 114
   ```

   - This assertion checks if the ASCII code of the first character in `.passwd` is 114 (corresponding to the letter 'r'). 
   - The server's response, again, acts as an oracle, indicating the success or failure of this check.

**Automating Blind Extraction:**

The provided Python script automates this blind information gathering by:

1. **Generating Payloads:** It systematically crafts assertions to check for different conditions, such as file length and character values at specific positions.
2. **Sending Requests:** It injects these assertions into the `page` parameter and sends requests to the vulnerable URL.
3. **Analyzing Responses:**  It analyzes the server's responses for `assert()` errors (or their absence), effectively treating the error messages as signals to deduce the content of `.passwd`.

**Key Points:**

- The specific error messages and conditions to look for might vary depending on the application code. Careful observation and adaptation are key.
- Blind exploitation is inherently slower than direct retrieval due to the need for multiple requests to extract information piecemeal.

By understanding how to leverage the flawed use of `assert()` for information gathering, we can turn a seemingly simple validation mechanism into a powerful tool for exploitation. This highlights the crucial security principle of never solely relying on client-side validation or using language constructs like `assert()` for security-critical checks. 


