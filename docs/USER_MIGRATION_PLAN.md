# DBERT Internship Portal — Active User Data Preservation Plan (MIG-002)

**Document Date:** 2026-09-23  
**Total User Accounts:** 2,230  

## 1. Non-Negotiable Preservation Guarantees

Under no circumstances may any schema or data migration modify, truncate, or overwrite the following records without explicit audit authorization:

| Dimension | Critical Fields | Existing Records | Missing / Corrupt | Preservation Status |
|---|---|---|---|---|
| **1. Identity** | `id`, `visitor_id` | 2,230 accounts | 0 missing IDs | **100% PRESERVED** |
| **2. Auth: Passwords** | `password_hash`, `password_set` | 2,230 hashed | 0 corrupted hashes | **100% PRESERVED** |
| **3. Auth: Legacy No-PW** | `password_set = 0` | 0 legacy accounts | Handled via OTP/legacy | **PRESERVED** |
| **4. Contact: Email** | `email` | 2,230 valid emails | 0 missing | **100% PRESERVED** |
| **5. Contact: Phone** | `phone` | 2,230 captured | Optional field | **100% PRESERVED** |
| **6. Profile: Academic** | `name`, `college`, `course` | 1,971 colleges | Optional field | **100% PRESERVED** |
| **7. Domain / Track** | `domain` | 1,237 domains assigned | Incomplete in signup | **PRESERVED** |
| **8. Applications** | `applications` table | 4,395 applications | Linked to 1,597 users | **100% PRESERVED** |
| **9. Enrollments** | `enrollments` table | 308 enrollments | 308 matching users | **100% PRESERVED** |
| **10. Attendance** | `attendance` table | 458 logs | 172 distinct interns | **100% PRESERVED** |
| **11. Certificates** | `intern_certificates` | 3 certificates | 3 distinct interns | **100% PRESERVED** |
| **12. Interviews** | `interviews` | 576 interviews | 536 candidate emails | **100% PRESERVED** |
| **13. Notifications** | `notifications` | 5,047 notices | 1107 distinct interns | **100% PRESERVED** |
| **14. Messages** | `messages` | 105 messages | Threaded conversations | **100% PRESERVED** |
| **15. Security Deposits**| `security_deposits` | 52 deposits | 52 distinct interns | **100% PRESERVED** |

---

## 2. Golden Migration Invariants

1. **Invariant 1: User IDs Never Shift**: Auto-increment or surrogate keys in `intern_accounts(id)` must remain immutable across all schema migrations.
2. **Invariant 2: Passwords Require No Reset**: PBKDF2/scrypt hashes must authenticate identically before and after any migration.
3. **Invariant 3: Zero Silent Deletes**: If a foreign key is broken or missing, the record is flagged in `DATA_INCONSISTENCIES.csv` for manual resolution — NEVER deleted via `CASCADE`.
