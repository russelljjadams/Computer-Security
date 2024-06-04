## Root-Me.org Challenge Write-Up: Local File Inclusion (Comprehensive Guide)
`https://www.root-me.org/en/Challenges/Web-Server/Local-File-Inclusion`

**Challenge Description:** The "Local File Inclusion" challenge throws down the gauntlet: reach the admin section. It seems simple enough, but a dangerous vulnerability lurks beneath the surface—one that can give attackers access to sensitive files and potentially control over the entire web server. 

**What is Local File Inclusion (LFI)?**

Local File Inclusion (LFI) is a type of web vulnerability that allows attackers to trick an application into including files from the server's file system that it shouldn't be able to access.  Imagine a web application that uses dynamic file inclusion to load content based on user input, like this:

```php
include($_GET['page'] . '.php');
```

This code snippet takes the value from the URL parameter `page` and includes a PHP file with that name. For example, if the URL is `http://example.com/?page=about`, the server would include the file `about.php`.

**The Attacker's Perspective:**

An attacker sees this and thinks, "What if I manipulate the `page` parameter to include something else?"  Instead of `about`, they could try:

```
http://example.com/?page=../../../../etc/passwd
```

If the application doesn't properly sanitize or validate the input, this could trick the server into including the sensitive system file `/etc/passwd`, potentially revealing user information.

**The Root-Me Challenge:**

This challenge likely follows a similar pattern.  Exploring the application, we observe that it uses two URL parameters:

- `files`:  This parameter seems to specify a category or directory.
- `f`:  This parameter determines the specific file to be included within the category.

For instance, a URL like:

```
http://challenge01.root-me.org/web-serveur/ch16/?files=crypto&f=index.html
```

might display the `index.html` file from a "crypto" directory.

**Exploitation Techniques: Directory Traversal**

The core technique for exploiting LFI is **directory traversal**. This involves using sequences like `../` to navigate up the directory structure. By carefully crafting the input, attackers can escape the restricted webroot and access files in other parts of the server. 

**The Winning Formula:**

To reach the admin section, we need to combine our knowledge of LFI, directory traversal, and the application's URL structure.  The correct exploit URL is:

```
http://challenge01.root-me.org/web-serveur/ch16/?files=crypto&f=../../admin/index.php
```

Here's how it works:

- `files=crypto`:  This part might not be strictly necessary, but it sets a base category for the inclusion.
- `f=../../admin/index.php`:  Here's the magic!
    - `../`: We use two `../` sequences to traverse up two directory levels, effectively escaping the restricted webroot.
    - `admin/index.php`: This specifies the target file—the `index.php` file within the `admin` directory.

**Success!** Visiting this crafted URL will likely load the content of the admin section's `index.php`, granting us unauthorized access.

**Remediation: Protecting Against LFI**

Preventing LFI vulnerabilities is crucial for web application security. Here are some key measures:

1. **Validate and Sanitize User Input:**
   - **Whitelisting:** Define a strict whitelist of allowed file names or paths and only include files that match the whitelist.
   - **Sanitization:** Remove or escape characters like `.` (dot) and `/` (slash) from user input to prevent path traversal attempts.

2. **Avoid Dynamic File Inclusion:** 
   - If possible, use static includes whenever you can. This significantly reduces the risk of LFI.

3. **Configure `open_basedir`:** 
   - Utilize the `open_basedir` setting in PHP to restrict file system access for PHP scripts to specific directories. This limits the impact of successful LFI attacks.

4. **Keep Software Updated:** 
   - Regularly update your web server, PHP version, and any relevant libraries or frameworks to patch known vulnerabilities. 

**Key Concepts to Remember:**

- **LFI is About Path Manipulation:** The attacker's goal is to control the file path used for inclusion.
- **Directory Traversal is Powerful:** Master the use of `../` to navigate directories. 
- **Context is King:** Pay close attention to how the application uses URL parameters and how you can manipulate them.
- **Security Implications are Serious:** LFI can allow attackers to:
    - Read sensitive files (configuration files, passwords, source code).
    - Execute arbitrary code on the server (if file upload or other vulnerabilities exist).

**Never Underestimate LFI:** This seemingly simple vulnerability can have devastating consequences. By understanding its mechanics and implementing proper remediation techniques, you can better protect applications and systems from exploitation. 
