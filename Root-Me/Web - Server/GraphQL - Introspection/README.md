## Root-Me.org Challenge Write-Up: GraphQL - Introspection
`https://www.root-me.org/en/Challenges/Web-Server/GraphQL-Introspection?lang=en`

**Challenge Description:** This challenge introduces GraphQL and its introspection capabilities.  We're tasked with exploring a GraphQL schema to potentially uncover hidden functionality or vulnerabilities.

**Vulnerability Exploited:** Insecure Direct Object Reference (IDOR)

**Tools Used:**  Burp Suite (or similar web proxy)

**Exploitation Steps:**

1. **Identify the GraphQL Endpoint:** We began by analyzing network requests and identified the GraphQL endpoint as `/rocketql`.

2. **Initial Introspection:**  Using a simple introspection query, we discovered a hidden query named `IAmNotHere` that wasn't visible in the application's interface:

    ```json
   {"query":"{ __schema { queryType { name fields { name description args { name type { name } } } } } }"} 
    ```

3. **Investigating `IAmNotHere`:** We attempted to query `IAmNotHere` but encountered errors indicating we needed to specify subfields.

4. **Targeted Introspection:** Another introspection query revealed that the `IAmNotHere` query returned a list of objects, each containing the fields `very_long_id` and `very_long_value`:

   ```json
   {"query":"{ __type(name: \"IAmNotHere\") { fields { name } } }"} 
   ```

5. **Crafting the Query:**  We constructed a query to fetch data using the `IAmNotHere` query, providing a test value for `very_long_id`:

   ```json
   {"query":"{ IAmNotHere(very_long_id: 1234567890) { very_long_id, very_long_value } }"}
   ```

6. **IDOR Exploitation:**  We received an empty list initially, suggesting no data for that ID.  However, by systematically manipulating the `very_long_id` value (starting from 1 and incrementing), we discovered that specific IDs returned data, including the hidden flag when we used the ID 17.

**Key Takeaways:**

* **GraphQL Introspection is Powerful:**  It allows attackers to map out the entire schema, including hidden queries and data structures.
* **IDOR is a Common GraphQL Vulnerability:**  Without proper authorization and validation, attackers can manipulate object identifiers to access sensitive information. 
* **Always Validate and Authorize Data Access:**  Never rely on client-side security to restrict data access.  Implement robust server-side validation and authorization to prevent IDOR vulnerabilities.

