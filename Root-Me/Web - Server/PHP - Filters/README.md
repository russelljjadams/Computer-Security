## Root-Me.org Challenge Write-Up: PHP - Filters
`https://www.root-me.org/en/Challenges/Web-Server/PHP-Filters`

**Challenge Description:** Our mission is to retrieve the administrator password from this application, with the only clue being a focus on "PHP - Filters."

**Unveiling the Power of `php://filter`**

The challenge's title hints at exploiting PHP's filtering mechanisms, but not in the conventional sense of input validation bypasses. The real key lies in understanding the `php://filter` stream wrapper and its potential for manipulating data streams.

**What is `php://filter`?**

- Think of it as a way to intercept and modify data "on-the-fly" as it's being read or written in PHP.
- It's particularly potent when combined with functions like `include` or `require`, which are often used to dynamically load files based on user input. 

**Crafting the Exploit:**

The application likely uses a vulnerable URL parameter, perhaps something like `inc`, to determine which file to include. Let's assume the default URL looks like this:

```
http://challenge01.root-me.org/web-serveur/ch12/?inc=login.php
```

To exploit this, we'll modify the `inc` parameter to inject a specially crafted `php://filter` URI:

```
http://challenge01.root-me.org/web-serveur/ch12/?inc=php://filter/convert.base64-encode/resource=config.php
```

Let's break down this crafted URL:

1. **`php://filter`:**  This part initiates a filter stream, telling PHP we want to process data through a filter.

2. **`convert.base64-encode`:**  Here, we specify the filter to apply. In this case, we're choosing to encode the data stream using Base64.

3. **`resource=config.php`:** This part defines the target "resource" to be filtered.  We suspect a file named `config.php` might contain the administrator password.

**How the Exploit Works:**

- **Server-Side Interpretation:** The vulnerable server, trying to include the file specified in the `inc` parameter, encounters the `php://filter` URI. 
- **Filter Activation:** Instead of directly including `config.php`, the server reads the file's content and passes it through the Base64 encoding filter. 
- **Encoded Output:** The server then sends the Base64-encoded content of `config.php` as the response to your request. 

**Retrieving the Password:**

1. **Capture the Response:**  You'll receive a Base64-encoded string in your browser.
2. **Decode the String:** Use a Base64 decoding tool or script to decode the response.
3. **Profit!**  The decoded string should reveal the contents of `config.php`, which likely contains the administrator password. 

**Key Takeaways:**

- **Think Outside the (Filter) Box:** PHP filters can be used for more than just input validation. They can manipulate data streams in powerful and potentially dangerous ways.
- **Beware of User-Controlled File Inclusions:** Never trust user input when constructing file paths for inclusion. Sanitization alone is often insufficient. Utilize parameterized queries or avoid dynamic file inclusions altogether whenever possible. 

This challenge highlights the importance of understanding the subtle ways in which PHP features can be misused. By mastering techniques like `php://filter` exploitation, you gain a deeper understanding of web application security and the attacker's mindset. 
