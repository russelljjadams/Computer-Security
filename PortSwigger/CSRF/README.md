# Understanding Cross-Site Request Forgery (CSRF)

Cross-Site Request Forgery (CSRF) is a type of web security vulnerability that can have severe consequences for both users and web applications. This attack exploits the trust that a website has in the user's browser, allowing malicious actors to perform unauthorized actions on behalf of authenticated users. This blog post will delve into the details of CSRF, explain why it works despite certain browser security mechanisms, and walk through the key concepts and practical examples covered in the first three labs of the PortSwigger Academy's CSRF section.

## What is CSRF?

CSRF, also known as XSRF or sea surf, is an attack that forces an end user to execute unwanted actions on a web application in which they are currently authenticated. With a little help from social engineering (such as sending a link via email or chat), an attacker may trick the users of a web application into executing actions of the attacker's choosing.

### Key Conditions for CSRF to Work

For a CSRF attack to be possible, three key conditions must be in place:

1. **A Relevant Action**: There must be an action within the application that the attacker wants to induce. This might be a privileged action (such as modifying permissions for other users) or any action on user-specific data (such as changing the user's own password).

2. **Cookie-Based Session Handling**: Performing the action involves issuing one or more HTTP requests, and the application relies solely on session cookies to identify the user who has made the requests. There is no other mechanism in place for tracking sessions or validating user requests.

3. **No Unpredictable Request Parameters**: The requests that perform the action do not contain any parameters whose values the attacker cannot determine or guess. For example, changing a password would be vulnerable if the function does not require the current password as a parameter.

## Why CSRF Works

A common point of confusion is understanding why a request from a different server is followed and processed by the target server, given that it seems like browsers should be smart enough to block such requests. To clarify this, we need to explore how browsers handle requests and enforce security policies.

### Same-Origin Policy (SOP)

The Same-Origin Policy (SOP) is a fundamental security mechanism that restricts how documents or scripts loaded from one origin can interact with resources from another origin. Two URLs have the same origin if they share the same scheme (protocol), host (domain), and port.

The SOP is designed to prevent malicious scripts on one page from obtaining access to sensitive data on another web page through that page's Document Object Model (DOM). However, SOP does not prevent the browser from sending requests to different origins. This is because web functionality often requires cross-origin requests, such as loading images, stylesheets, or making API calls.

### Automatic Cookie Handling

Cookies are small pieces of data stored by the browser and sent to the server with every request to the domain they belong to. This automatic inclusion of cookies in requests is what makes CSRF possible. When a user is authenticated on a site (e.g., `bank.com`), the browser stores a session cookie. If the user later visits a malicious site (e.g., `attacker.com`), the malicious site can generate a request to `bank.com`, and the browser will include the session cookie with the request.

## Practical Example: Changing Email Address

Let's consider a practical example to illustrate how a CSRF attack works. Suppose a vulnerable web application allows users to change their email addresses via the following endpoint:

```
POST http://vulnerable-website.com/change-email
Body: email=newemail@example.com
```

An attacker can craft a malicious form that targets this endpoint:

```html
<form action="http://vulnerable-website.com/change-email" method="POST">
  <input type="hidden" name="email" value="attacker@example.com">
  <input type="submit" value="Submit">
</form>
```

When an authenticated user visits the attacker's website and submits the form (either manually or automatically using JavaScript), the browser sends the request along with the session cookie to the vulnerable website. The vulnerable website processes the request and changes the user's email address to `attacker@example.com`.

## Mitigating CSRF Attacks

Given the simplicity and potential severity of CSRF attacks, it is crucial for web developers to implement protective measures:

1. **CSRF Tokens**: Include a unique, unpredictable token in each form that is tied to the user's session. Validate this token on the server side before processing the request.

2. **SameSite Cookie Attribute**: Use the `SameSite` attribute for cookies to control their inclusion in cross-origin requests. The `SameSite` attribute can be set to `Lax` or `Strict` to help prevent CSRF by ensuring cookies are not sent with cross-origin requests.

3. **Double Submit Cookies**: Send a CSRF token in both a cookie and a request parameter. The server verifies that both values match.

4. **Referer and Origin Header Checks**: Verify the `Referer` or `Origin` header of incoming requests to ensure they originate from the expected domain.

## Lab Walkthrough: PortSwigger Academy CSRF Labs

Let's walk through the key concepts and practical examples covered in the first three labs of the PortSwigger Academy's CSRF section.

### Lab 1: Basic CSRF Attack

In the first lab, we explored a basic CSRF attack scenario where the attacker wants to change the victim's email address. The lab setup involved a vulnerable application that allowed users to change their email without any additional verification beyond being logged in.

#### Steps to Exploit:
1. **Craft the Malicious Request**: The attacker crafts a request to change the email address.
2. **Host the Malicious Request**: The attacker hosts this request on their website.
3. **Trick the User**: The attacker tricks the victim into visiting the malicious site, causing the request to be sent to the vulnerable application.

Example of a malicious form used in this lab:

```html
<form action="http://vulnerable-website.com/change-email" method="POST">
  <input type="hidden" name="email" value="attacker@example.com">
  <input type="submit" value="Submit">
</form>
```

When an authenticated user visits the attacker's site and submits the form, the user's email address is changed to the attacker's email address.

### Lab 2: Changing Request Type to Bypass CSRF Protection

In the second lab, we learned that some servers are vulnerable because they can process requests of different types (e.g., GET instead of POST) for the same action, potentially bypassing CSRF protections like CSRF tokens.

#### Steps to Exploit:
1. **Identify the Vulnerable Endpoint**: Identify an endpoint that can be accessed using different request methods (GET instead of POST).
2. **Craft the Malicious Request**: Craft a GET request to the vulnerable endpoint.
3. **Trick the User**: The attacker tricks the victim into visiting a URL that performs the action.

Example of a malicious URL used in this lab:

```html
<img src="http://vulnerable-website.com/change-email?email=attacker@example.com" style="display:none;">
```

By embedding this image tag in a malicious webpage, the attacker's request is sent when the page is loaded, bypassing any CSRF tokens that would be required in a POST request.

### Lab 3: Omitting the CSRF Token

In the third lab, we explored a scenario where the server does not validate the CSRF token if it is missing from the request. This vulnerability allows an attacker to omit the CSRF token in their malicious requests.

#### Steps to Exploit:
1. **Identify the Vulnerable Endpoint**: Identify an endpoint that accepts requests without a CSRF token.
2. **Craft the Malicious Request**: Create a form or URL that submits the request without including the CSRF token.
3. **Trick the User**: The attacker tricks the victim into submitting the form.

Example of a malicious form used in this lab:

```html
<form action="http://vulnerable-website.com/change-email" method="POST">
  <input type="hidden" name="email" value="attacker@example.com">
  <input type="submit" value="Submit">
</form>
```

When an authenticated user visits the attacker's site and submits the form, the request is processed even though the CSRF token is omitted.

## Lab 4: CSRF Where Token is Not Tied to User Session

In the fourth lab, we explored a scenario where the application's email change functionality is vulnerable to CSRF despite using CSRF tokens. The vulnerability arises because the tokens are not tied to the user session. This means an attacker can reuse a token obtained from their own session to perform actions on behalf of another user.

### Scenario

The lab setup includes an email change functionality protected by CSRF tokens. However, these tokens are not integrated into the site's session handling system. This oversight allows an attacker to exploit the vulnerability using a token from their own session.

### Steps to Exploit:

1. **Log in to Attacker Account**: First, log in to one of the provided attacker accounts, either `wiener:peter` or `carlos:montoya`.

2. **Intercept the Email Change Request**: Using a tool like Burp Suite, intercept the request when changing the email address. This will allow you to capture a valid CSRF token.

3. **Drop the Request**: After capturing the CSRF token, drop the request to prevent it from being processed.

4. **Craft the Malicious Request**: Use the captured CSRF token to create a malicious HTML form that will submit a request to change the email address of the victim.

5. **Host the Malicious Form**: Host this form on an attacker server or any web page you control.

6. **Trick the Victim**: Trick the victim into visiting the page containing the malicious form.

### Detailed Steps and Example

1. **Log in to Attacker Account**:
   - Use the credentials `wiener:peter` or `carlos:montoya` to log in to the application.

2. **Intercept the Email Change Request**:
   - Navigate to the email change functionality.
   - Enter a new email address and submit the form.
   - Intercept the request using Burp Suite.
   - Copy the CSRF token from the intercepted request.

3. **Drop the Request**:
   - After copying the CSRF token, drop the request to prevent it from being processed by the server.

4. **Craft the Malicious Request**:
   - Create an HTML form that uses the captured CSRF token to change the email address of any user who submits the form.

```html
<form action="http://vulnerable-website.com/change-email" method="POST">
  <input type="hidden" name="csrf_token" value="VALID_CSRF_TOKEN_FROM_ATTACKER_SESSION">
  <input type="hidden" name="email" value="attacker@example.com">
  <input type="submit" value="Change Email">
</form>
```

Replace `VALID_CSRF_TOKEN_FROM_ATTACKER_SESSION` with the actual token you captured.

5. **Host the Malicious Form**:
   - Host this form on your exploit server or any web page you control.

6. **Trick the Victim**:
   - Send a link to the victim, luring them to visit the page with the malicious form.

### Exploiting the Vulnerability

When the victim visits the malicious page and submits the form (either manually or through an automatic script), the request is sent to the vulnerable application with a valid CSRF token. Since the token is not tied to the user's session, the server accepts it and processes the request, changing the victim's email address to `attacker@example.com`.

### Conclusion

This lab highlights the importance of tying CSRF tokens to user sessions. Tokens must be unique per session and validated against the user's session data to prevent reuse across different sessions. Without this, an attacker can exploit the token pool to perform unauthorized actions on behalf of other users. By understanding this vulnerability, developers can implement more robust CSRF protection mechanisms to secure their applications.

## Conclusion

Cross-Site Request Forgery (CSRF) is a potent attack vector that exploits the way browsers handle cookies and cross-origin requests. Despite the protections offered by the Same-Origin Policy, CSRF attacks can still occur because browsers automatically include cookies in cross-origin requests. Understanding the conditions that make CSRF possible and implementing effective mitigation strategies, such as CSRF tokens and the SameSite cookie attribute, are crucial for securing web applications.

By studying practical examples and walking through the labs in the PortSwigger Academy, we gain a deeper understanding of how CSRF attacks work and how to defend against them. Remember, the key to preventing CSRF attacks lies in ensuring that every action requiring user authentication also includes a mechanism to verify the authenticity of the request, such as CSRF tokens or other unpredictable parameters.
