# DBERT Internship Portal — User Lifecycle Classification Report (MIG-001)

**Generated Date:** 2026-09-23 16:27:23  
**Total Active User Accounts:** 2,230  
**Database:** `internship.db`

## 1. Lifecycle Distribution Summary

| Lifecycle Stage | User Count | Percentage | Operational Meaning |
|---|---|---|---|
| **A — Registered but not applied** | 8 | 0.4% | Account state mapped by DB evidence |
| **B — Application pending (Incomplete signup)** | 388 | 17.4% | Account state mapped by DB evidence |
| **C — Under review** | 413 | 18.5% | Account state mapped by DB evidence |
| **C — Under review (On Hold)** | 12 | 0.5% | Account state mapped by DB evidence |
| **E — Enrollment pending** | 616 | 27.6% | Account state mapped by DB evidence |
| **F — Payment pending / under review** | 3 | 0.1% | Account state mapped by DB evidence |
| **H — Active internship** | 305 | 13.7% | Account state mapped by DB evidence |
| **K — Rejected** | 249 | 11.2% | Account state mapped by DB evidence |
| **L — Inactive / Abandoned** | 236 | 10.6% | Account state mapped by DB evidence |

---

## 2. Category Definitions & Actual Database States

1. **A — Registered but not applied**: Intern accounts with no record in `applications` created recently.
2. **B — Application pending**: Interns who stopped at signup step 1 or 2 (`signup_stage < 3`).
3. **C — Under review**: Candidates whose application status is `'Under Review'` or `'On Hold'`.
4. **D — Selected**: Candidates marked `'Selected'` who have not yet submitted deposit/enrollment.
5. **E — Enrollment pending**: Candidates marked `'Enrollment Pending'`.
6. **F — Payment pending**: Enrolled candidates whose deposit is `'Pending'` or `'Rejected'`.
7. **G — Enrolled**: Payment is `'Accepted'`, orientation/joining date is in the future.
8. **H — Active internship**: Payment is `'Accepted'` and attendance minutes are actively accumulating.
9. **J — Certificate issued**: Intern has satisfied requirements and `intern_certificates` entry exists.
10. **K — Rejected**: Application explicitly rejected.
11. **L — Inactive / Abandoned**: Old registered accounts with zero activity or applications.
