
Here are specific measures for each pillar:

##  Confidentiality Measures

Confidentiality is about ensuring **only authorized users** can view sensitive data. The primary methods revolve around access control and making data unreadable to outsiders.

| Measure | Description | Example/Tool |
| :--- | :--- | :--- |
| **Encryption** | Scrambling data into an unreadable format using a key. This should be applied to data both **at rest** (stored) and **in transit** (moving across networks). | **AES-256** for data at rest; **TLS/SSL** for data in transit (e.g., HTTPS). |
| **Access Control** | Restricting who can access resources based on identity and privileges, often using the **Principle of Least Privilege (PoLP)**. | **Role-Based Access Control (RBAC)**; Linux file **`chmod`/`chown`** permissions. |
| **Authentication** | Verifying a user's identity before granting access. Passwords alone are often insufficient. | **Multi-Factor Authentication (MFA/2FA)**; Biometrics; Strong password policies. |
| **Data Classification**| Systematically categorizing data (e.g., Public, Internal, Confidential, Restricted) to apply appropriate security controls. | Marking documents as **"Internal Use Only"** and encrypting all files in the **"Restricted"** category. |

---

##  Integrity Measures

Integrity is about ensuring data is **accurate, complete, and trustworthy**, protecting it from unauthorized or accidental modification.

| Measure | Description | Example/Tool |
| :--- | :--- | :--- |
| **Hashing & Checksums**| Using cryptographic algorithms to create a unique digital fingerprint of a file. Any change to the file results in a different hash. | **SHA-256** to verify a software download; **Checksums** for checking data transmission errors. |
| **Auditing & Logging** | Keeping detailed, tamper-proof records of all changes, access attempts, and administrative actions. | **Audit Trails/Transaction Logs** on a database; **`/var/log/secure`** on Linux. |
| **Version Control** | Tracking and managing changes to code or configuration files, allowing administrators to roll back to a known-good state. | Using tools like **Git** for source code; Configuration backups for system files. |
| **Input Validation** | Checking data submitted by users to ensure it adheres to expected formats and ranges, preventing accidental or malicious data corruption. | Checking that a birth date field contains a valid date, not code. |

---

##  Availability Measures

Availability ensures that systems and data are **accessible to authorized users when needed**, even in the face of hardware failure, attacks, or disasters.

| Measure | Description | Example/Tool |
| :--- | :--- | :--- |
| **Redundancy** | Duplicating critical hardware or services so that if one fails, the other can take over immediately. | **RAID** (redundant array of inexpensive disks) for storage; **Clustering/Failover** systems for critical application servers. |
| **Disaster Recovery (DR)** | Having a detailed plan and resources to restore business operations after a major disaster. | Offsite/Cloud **Backup and Recovery** solutions; Defined **Recovery Time Objectives (RTO)**. |
| **Load Balancing** | Distributing incoming network traffic across multiple servers to prevent any single server from being overwhelmed. | **Application Load Balancers (ALBs)** in cloud environments or network devices to handle high traffic. |
| **Patching & Maintenance**| Regularly updating software and hardware to fix bugs, close security vulnerabilities, and prevent performance degradation. | **Automated Patch Management** systems; **Regular monitoring** (e.g., `top`, `df -h`) to detect resource issues early. |

---

