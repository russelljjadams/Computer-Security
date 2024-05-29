## Root-Me.org Challenge Write-Up: API - Broken Access
`https://www.root-me.org/en/Challenges/Web-Server/API-Broken-Access`

**Challenge Description:** This aptly named "API - Broken Access" challenge on Root-Me.org presents us with a seemingly standard web application offering user management features. However, a critical vulnerability lurks beneath its surface, highlighting the importance of thorough API security testing. We embarked on a winding journey, initially fixated on complex cookie manipulation, only to discover a much simpler solution by embracing a fundamental security principle: reading the documentation!

**What is Broken Access?**

In the context of APIs, "broken access" often refers to vulnerabilities that allow unauthorized users to access restricted resources or perform actions they shouldn't be able to. This can occur due to:

- **Improper Authorization Checks:** The API fails to properly verify if a user is authorized to access a specific resource or perform an action. 
- **IDOR (Insecure Direct Object Reference):** The application uses user-supplied input (e.g., a user ID) to directly access data without proper authorization checks.
- **Missing or Inadequate Rate Limiting:** Attackers can exploit missing or weak rate limiting to brute-force credentials, enumerate resources, or overwhelm the API.

**Our Initial (Misguided) Quest:**

We observed that the application used`user_id=2` when we created an account, likely meaning, at the least, that there is already a user that has the id of `1`. Assuming a classic IDOR vulnerability, we focused on the complex cookie set by the application, specifically a Base64-encoded string within it.

We meticulously analyzed this cookie: decoding, comparing variations, strategically modifying bits and bytes, even uncovering a layer of zlib compression. We battled checksum errors and fought valiantly against what appeared to be stringent server-side cookie validation. Eventually we were even able to modify bits of the cookie to change the user_id in the cookie. Unfortuantely, the server didn't like the modified cookie. 

**The Power of a Step Back: Embracing Documentation**

Frustrated and questioning our approach, we paused and reassessed.  A seemingly insignificant request for `/static/swagger.json` caught our attention.  This file, if present, would contain the application's Swagger/OpenAPI documentation—a potential goldmine of information.

Accessing and examining the JSON documentation provided the "aha!" moment. The `/api/user` endpoint, responsible for fetching user data, declared its `user_id` parameter as **not required** (`"required": false"`) and passed in the URL path (`"in": "path"`).  

**The (Embarrassingly Simple) Solution:**

Armed with this newfound knowledge, the solution became almost trivial.  We could entirely bypass our intricate cookie manipulation attempts and directly construct URLs like this:

- `http://challenge01.root-me.org:59088/api/user/0`
- `http://challenge01.root-me.org:59088/api/user/1` 

The application, blindly trusting the `user_id` value in the URL path, happily returned data for any user ID we specified, completely bypassing any intended authorization checks.

**Remediation: Securing the Access Breach**

To fix this broken access vulnerability, developers should:

1. **Enforce Required Parameters:** Ensure that API endpoints explicitly declare critical parameters like `user_id` as *required*. This prevents accidental reliance on potentially insecure default values.
2. **Implement Robust Authorization Checks:**  **Never** rely solely on client-supplied data for authorization.  Always perform server-side validation to verify that the user making the request has the necessary permissions to access the requested user's data. This could involve:
     -  Verifying session tokens
     -  Validating access tokens (for OAuth-based authentication)
     -  Checking user roles and permissions
3. **Thoroughly Test APIs:** Rigorously test API endpoints with various inputs, including unexpected values and attempts to access resources without proper authorization. 

**Lessons Learned (More Thoroughly Ingrained):**

- **Documentation is Your Ally:**  Embrace API documentation!  It can reveal vulnerabilities and provide valuable insights into the application's logic. 
- **Challenge Your Assumptions:** We fell into the trap of fixating on the cookie.  Regularly re-evaluate your assumptions and consider alternative attack vectors. 
- **Even Small Details Matter:**  The seemingly insignificant `/static/swagger.json` request turned out to be the key. Pay attention to the details!
- **Enjoy the Journey (and the "Aha!" Moments):** Cybersecurity is a continuous learning process.  Celebrate the victories, embrace the challenges, and never stop learning.  

This challenge served as a potent reminder of the importance of thoroughness, attention to detail, and, above all, reading the documentation! The most elegant solutions are often hiding in plain sight, waiting for us to shift our perspective and break free from our self-imposed constraints. 
