
## Root-Me.org Challenge Write-Up: API - Mass Assignment (via User Update)
`http://challenge01.root-me.org/web-serveur/ch90/`

**Challenge Description:** This challenge revisits the API from the previous IDOR challenge, now fortified against direct note manipulation. The goal is to gain administrative privileges, hinted at by the "API - Mass Assignment" title and the introduction of an "admin" role.

**Vulnerability Explanation:** While the Swagger documentation explicitly details a GET request for `/api/user` to retrieve user information, it doesn't explicitly forbid a PUT request for the same endpoint. This oversight creates a Mass Assignment vulnerability, allowing attackers to update user data, including sensitive attributes like `status`.

**Exploitation Steps:**

1. **User Account Creation:** Create a regular user account on the platform. This step is crucial for obtaining a valid user ID and session token.

2. **Retrieve User Information:** Issue a GET request to `/api/user` using your valid session cookie. Note your `userid` for the next step. 

3. **Craft Malicious PUT Request:** Construct a PUT request to `/api/user` with the following JSON payload, replacing placeholders with your actual details:

   ```json
   {
     "note": "My note",
     "status": "admin",
     "userid": [Your User ID],
     "username": "[Your Username]"
   }
   ```

4. **Send the Request:** Issue the crafted PUT request. If successful, your user account's `status` should be updated to "admin".

5. **Access the Flag:** Attempt to access the `/api/flag` endpoint. With your elevated privileges, you should now receive the flag!

**Remediation:**

To prevent this vulnerability, developers should:

* **Explicitly Define Allowed Methods:** In API documentation and implementation, clearly define permissible HTTP methods (GET, POST, PUT, DELETE, etc.) for each endpoint.
* **Implement Strong Input Validation:**  Never trust client-side data. Validate all incoming data against a strict schema, whitelisting acceptable fields and values. 
* **Use Dedicated Update Endpoints:**  If possible, provide separate endpoints for updating different parts of the user object (e.g., `/api/user/profile` for updating basic information and `/api/user/security` for sensitive settings).
* **Apply the Principle of Least Privilege:** Update user objects with only the data necessary for the specific operation, avoiding blanket updates based on user input.

**Key Takeaways:**

This challenge emphasizes:

* **The Importance of Thorough Testing:** Security testing should encompass not only documented functionality but also explore potential loopholes and edge cases.
* **The Value of Secure Coding Practices:** Adhering to secure coding principles and carefully validating user input can prevent many common vulnerabilities.
* **The Need for Continuous Vigilance:** Security is an ongoing process. Regularly reviewing and updating code, documentation, and security practices is essential in our ever-evolving threat landscape. 

