## Root-Me.org Challenge Write-Up: File Upload - ZIP
`https://www.root-me.org/en/Challenges/Web-Server/File-upload-ZIP`

**Challenge Description:**

This challenge presents a classic scenario: a web application with a file upload feature. The objective is to exploit potential vulnerabilities related to how the server handles ZIP archives to read the content of the `index.php` file.

**Initial Assessment (and Red Herrings):**

1. **The Hints:** The challenge provided two crucial hints: "Unsafe decompression" and "read index.php." 

2. **Classic Directory Traversal (That Didn't Work):**
   -  Initially, we focused on exploiting a vulnerability known as "Zip Slip," where a maliciously crafted ZIP archive containing directory traversal sequences (`../`) could potentially place files outside the intended upload directory. 
   -  However, through careful observation of the file paths in the URLs after upload, we realized that the challenge creators had effectively prevented this type of attack. The uploaded files were always placed within the expected upload directory structure. 

**The Breakthrough: Shifting Focus to Symlinks**

1. **Understanding the Constraint:**  We learned that we couldn't directly execute PHP files outside specific directories.  Therefore, exploiting code execution via directory traversal wasn't viable.

2. **Symlinks as a Data Access Tool:** We realized that while we couldn't directly *execute* files, we might be able to use symlinks to make the server *serve* us the content of `index.php` without relying on code execution.

**The Solution:**

1. **Crafting the Malicious ZIP Archive:**
   - **Symlink Creation:** On our local system, we created a symlink named `index.txt` that pointed to the `index.php` file, using a relative path to exploit the predictable upload directory structure:
     ```bash
     ln -s ../../../index.php index.txt
     ```
   - **ZIP Archive with Symlink Preservation:** We created a ZIP archive named `index.zip`, making sure to preserve the symlink information: 
     ```bash
     zip --symlinks index.zip index.txt
     ``` 

2. **Exploiting Server-Side Extraction:**
   - We uploaded `index.zip` to the challenge.
   - When the server extracted the archive, it created the `index.txt` symlink, pointing to the `index.php` file.

3. **Accessing `index.php` Content:**
   - We accessed the symlink through a URL like this: 
     ```
     http://challenge01.root-me.org/web-serveur/ch51/tmp/upload/[random_dir]/index.txt
     ```
   - The server, following the symlink, served the content of `index.php`, allowing us to complete the challenge!

**Key Takeaways:**

- **Don't Assume Classic Attacks Will Always Work:** Challenge creators often implement security measures to prevent common exploits, forcing you to think outside the box.
- **Symlinks are Powerful:**  Symlinks can be used creatively to access sensitive data or functionality, even when direct access is restricted. 
- **Observation is Key:** Carefully analyze the application's behavior, error messages, and any clues in the challenge description to guide your approach.

**Remediation:**

- **Secure File Handling Libraries:**  Ensure that any libraries or utilities used to handle ZIP archives are up-to-date and patched against known vulnerabilities related to symlink attacks and directory traversal.
- **Validate Extracted Content:** Implement security checks to validate the contents and paths of files extracted from archives, preventing the creation of symlinks pointing to unintended locations. 
- **Principle of Least Privilege:** Run the web server and file handling processes with the least privilege necessary to minimize the impact of potential exploits.


Let me know when you are ready for the next challenge.  I am eager to learn and put my skills to the test alongside you! 
