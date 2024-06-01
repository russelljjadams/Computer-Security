## Root-Me.org Challenge Write-Up: PHP - Register Globals
`https://www.root-me.org/en/Challenges/Web-Server/PHP-register-globals`

**Challenge Description:** This challenge hints at a common security oversight: "It seems that the developer often leaves backup files around..." Our objective is to retrieve the administrator password.

**Unearthing the Developer's Oversight:**

Before we can exploit any vulnerability, we need to find the backup file containing the application's source code. Developers often leave backup files with predictable names and extensions. Let's start our hunt by trying some common possibilities:

**Common Backup File Names:**

- `index.php.bak`
- `config.php.bak`
- `login.php.bak`
- `admin.php.bak`
- `database.sql.bak`
- `users.sql.bak`

**Common Backup File Extensions:**

- `.bak`
- `.old`
- `.backup`
- `.orig`
- `.tmp` 

In this case, `index.php.bak` is the correct backup file. Downloading and examining it reveals the authentication logic. Pay close attention to the code, as it holds the key to exploiting a vulnerability. 

**Understanding the Peril of `register_globals`**

The code in `index.php.bak` exposes a critical security flaw: It relies on the `register_globals` setting, which is notoriously insecure and has been deprecated in modern PHP versions. 

**Let's Recap `register_globals`**

- **The (Bad) Idea:** In older PHP versions, `register_globals` was enabled by default. This meant that any data passed through a URL (query parameters) or form submissions (POST or GET variables) would automatically become global variables within the PHP script. 
- **The Security Risk:**  This practice creates a gaping hole because attackers can directly inject values into a script's global namespace, potentially overriding existing variables or introducing malicious code.

**The Vulnerability in Plain Sight:**

Examine the code carefully. The crucial section is within an `if` block that checks whether `register_globals` is enabled:

```php
if (!ini_get('register_globals')) {
    $superglobals = array($_SERVER, $_ENV,$_FILES, $_COOKIE, $_POST, $_GET);
    if (isset($_SESSION)) {
        array_unshift($superglobals, $_SESSION);
    }
    foreach ($superglobals as $superglobal) {
        extract($superglobal, 0 );
    }
}
```

The `extract()` function is used to essentially re-create the behavior of `register_globals` by pulling variables from superglobal arrays like `$_POST`, `$_GET`, and `$_SESSION`. 

**Exploiting the Global Variable Injection:**

The authentication logic relies on the `logged` variable within the `$_SESSION` array.  If we can directly set this variable, we can bypass the authentication system.  

Here's the key to exploiting this:

- **URL Parameter Manipulation:**  Because `register_globals` is effectively being re-enabled, we can manipulate the `$_SESSION` array by setting a value in the URL itself:

   ```
   http://challenge01.root-me.org/web-serveur/ch17/?_SESSION[logged]=1
   ```

   - By setting `_SESSION[logged]=1`, we directly inject a value into the script's global namespace, forcing the authentication check to succeed.

**Claiming Your Prize:**

Visit the modified URL, and the administrator password will be revealed!

**Remediation is Key:**

- **Disable `register_globals`:** This is a critical step for any PHP application. It's the most important security measure against this vulnerability. 
- **Always Validate Input:**  Sanitize and validate all user input rigorously, particularly for sensitive data like passwords.
- **Avoid Superglobal Manipulation:**  Don't use `extract()` to create global variables from superglobal arrays. Access them directly using their names (e.g., `$_SESSION['logged']`).

**The Takeaway:** This challenge serves as a stark reminder that even seemingly innocuous configuration settings can have major security implications.  Understanding outdated configurations and practices like `register_globals` is crucial for any security professional. Additionally, knowing common backup file naming conventions is essential for uncovering vulnerable code. 
