## Root-Me.org Challenge Write-Up: Insecure Code Management
`https://www.root-me.org/en/Challenges/Web-Server/Insecure-Code-Management`

**Challenge Description:** This challenge presents a seemingly straightforward objective: retrieve the admin password in plain text.  However, the path to the solution leads us through a captivating exploration of Git's internal workings, the dangers of insecure development practices, and the subtle art of uncovering hidden information within a target environment.

**Vulnerability Exploited:** Insecure Code Management (Exposure of `.git` Repository)

**Tools Used:** 
- Web Browser (for reconnaissance)
- `wget` (or similar download tool)
- `git` command-line tools

**Exploitation Methodology:**

1. **Reconnaissance and Research - A Blended Approach:**  
   - **Initial Reconnaissance:**  We began with a standard reconnaissance approach, attempting to use directory enumeration tools like `gobuster` and `dirb` to uncover hidden directories and files. However, we quickly realized that Root-Me.org's security measures prevented the use of such automated scanners. 
   - **Leveraging Challenge Clues:** This roadblock prompted us to rely more heavily on information provided within the challenge description itself.  The phrases "insecure code management" and "code management server" strongly suggested that we should investigate potential misconfigurations related to version control systems.
   -  **Targeted Research:**  We conducted focused research using search queries like "insecure code management" + "code management server" and similar variations.  This research highlighted common misconfigurations, including the accidental exposure of `.git` directories on web servers.
   `https://blog.secuna.io/insecure-source-code-management/`

2. **Manual Verification - The `.git` Folder Emerges:** Armed with this knowledge, we manually attempted to access the `/.git/` directory on the challenge server using our web browser. To our advantage, the directory was indeed accessible, indicating a potential vulnerability.

3. **Partial Exposure - Git Objects, Not Structure:**  Upon closer inspection, we realized the server didn't expose a typical `.git` folder structure directly. Instead, we could only access specific Git objects (blobs, trees, commits) via hash-based URLs: 
    -  `http://challenge-url/.git/objects/<first_two_hash_characters>/<remaining_hash_characters>` 

4. **Understanding Git's Content-Addressable Storage:** This revelation forced us to delve deeper into Git's internal storage system:
   - Git doesn't store file changes as diffs or snapshots. Every version of a file, directory, or commit is treated as a unique "blob" (binary large object) identified by its SHA-1 hash. 
   -  These blobs reside within the `.git/objects` directory, organized efficiently using the first two characters of their hash for faster lookup.

5. **Reconstructing History from Commit Messages:**  We examined the exposed `.git/logs/HEAD` file (or downloaded commit objects) to piece together the commit history. Crucially, commit messages provided valuable context:
    - References to password changes ("secure auth with md5", "changed password") and hashing algorithm updates suggested that earlier commits might hold the password in a less secure form.

6. **Manually Downloading and Reconstructing:**  We used the commit hashes from the history to download specific Git objects (commits, trees, blobs) using `wget`. 
    - We then manually reconstructed these objects within a local Git repository, initialized using `git init <repo-name>`, effectively mimicking Git's internal object database structure.

7. **Utilizing `git cat-file` for Extraction:** With the objects in place, we leveraged the `git cat-file -p <full_hash>` command to view their contents: 
    - Commit objects pointed to their associated tree objects (directory structures). 
    - Tree objects revealed the blob hashes of files within them.
    - Ultimately, we retrieved the contents of the `config.php` blob from our target commit, which exposed the flag (the admin password in plain text).
The following URL provides a detailed walkthrough of the approach needed: `https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Insecure%20Source%20Code%20Management`

**Key Takeaways:**

- **Defense In Depth:**  Root-Me.org's platform security measures effectively demonstrated the importance of having layered defenses in place. Our inability to rely solely on automated scanners highlighted the need for adaptability and a multi-faceted approach to penetration testing.
- **Research and Deduction:**  We successfully overcame the scanner restrictions by carefully analyzing the challenge description, conducting targeted research, and making educated guesses about potential vulnerabilities.
- **Git Internals are Essential:** Understanding how Git functions internally, especially its content-addressed storage system, is crucial for uncovering and exploiting vulnerabilities related to exposed Git repositories.

This challenge masterfully illustrated that successful penetration testing requires a blend of technical skills, research prowess, and the ability to think critically and adapt to unexpected constraints. 


