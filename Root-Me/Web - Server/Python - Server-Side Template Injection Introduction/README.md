## Root-Me.org Challenge Write-Up: Python - Server-Side Template Injection Introduction
`https://www.root-me.org/en/Challenges/Web-Server/Python-Server-side-Template-Injection-Introduction`

**Challenge Description:**

This challenge presents a web service allowing users to generate a webpage with custom titles and content. The objective is to exploit potential vulnerabilities in this service to read a hidden flag file.

**Vulnerability Identification:**

1. **Suspecting Server-Side Template Injection (SSTI):**

   - The challenge description and the web interface, with its "title" and "page content" input fields, strongly suggested the use of server-side templates to dynamically generate web pages.
   - This raised immediate concerns about potential Server-Side Template Injection (SSTI) vulnerabilities, where an attacker might be able to inject malicious code into template variables.

2. **Confirming SSTI:**

   - We injected specific payloads into the "page content" input field to test for SSTI:
     - `{{ 7*7 }}`: This payload, if executed within a template engine, should output `49`.  
     - `{{ self.__dict__ }}`: This payload aims to access and display the internal properties of the template object, potentially revealing sensitive information.

3. **Identifying the Template Engine:**

   - The output from `{{ self.__dict__ }}` revealed elements from the `jinja2.utils` module, strongly indicating the use of the Jinja2 templating engine.

**Exploitation:**

1. **Achieving Remote Code Execution (RCE):**

   - Armed with the knowledge that Jinja2 was likely in use, we crafted a payload to execute arbitrary Python code on the server:
     - `{{ lipsum.__globals__["os"].popen('id').read() }}`
     - This payload leverages Jinja2's syntax to access the global Python namespace (`__globals__`), obtain a reference to the `os` module, and execute the `id` command. 
   - The successful execution of the `id` command confirmed our ability to execute arbitrary code on the server.

2. **Locating the Flag:**

   - We systematically explored the server's filesystem using various commands within our payload:
     - `{{ lipsum.__globals__["os"].popen('ls /').read() }}`: Listed the root directory.
     - `{{ lipsum.__globals__["os"].popen('ls /home').read() }}`: Listed the "home" directory.
     - `{{ lipsum.__globals__["os"].popen('find / -name "flag*" 2>/dev/null').read() }}`: Searched for files containing "flag" in their names. 

3. **Unveiling the Flag:**

   - After attempting to list hidden files with `ls -a /` (which did not reveal the flag file), we discovered that the `.passwd` file existed in the current working directory.
   - The payload `cat .passwd` successfully displayed the contents of this file, which contained the flag.

**Key Findings:**

- **Server-Side Template Injection:** The application was vulnerable to SSTI, allowing us to inject and execute arbitrary code.
- **Jinja2 Template Engine:** The specific templating engine used was Jinja2.
- **Remote Code Execution (RCE):** We achieved RCE by exploiting the SSTI vulnerability.
- **Filesystem Access:** We gained access to the server's filesystem through command execution.
- **Non-Standard Flag Location:** The flag was located in a hidden file (`.passwd`) in the current working directory.

**Lessons Learned:**

- **Thoroughness in Exploration:**  Always systematically explore potential vulnerabilities and the target system.
- **Understanding the Technology Stack:** Identifying the specific technologies used (like the templating engine) is crucial for crafting effective exploits.
- **Attention to Detail:** Pay close attention to error messages, unexpected behavior, and even seemingly insignificant details, as they can provide valuable clues.

**Remediation:**

- **Sanitize User Input:** Implement strict input validation and sanitization to prevent attackers from injecting malicious code.
- **Principle of Least Privilege:** Run the web server and application with the least privilege necessary to minimize the impact of potential exploits.
- **Keep Software Updated:** Regularly update all software components, including the templating engine and its dependencies, to patch known vulnerabilities. 
