# Community Learning Hub Management System

A command-line management system built in Python for managing members, courses, enrollments, and learning resources with role-based access control (Admin vs. Student/Normal User).

---

## Team Members & Assigned Roles

### Mandatory Functions
* **Wong Li Ting (TP174742):** Resources Management, Main Menu
* **Chin Jun Xiang (TPXXXXXX):** Member Management
* **Lee Jun Xuan (TPXXXXXX):** Course Management
* **Yap Kai Bin (TPXXXXXX):** Enrollment Management

### Additional Features
* **Wong Li Ting (TP174742):** Login Menu, Multi-field Resource Filtering/Searching, Automatic File Backup & Undo (`rr_filebackup.py`)
* **Chin Jun Xiang (TPXXXXXX):** Login Menu (PBKDF2 Password Hashing & Salting), Auto-generated Member IDs (`M0001`, `M0002`, ...)
* **Lee Jun Xuan (TPXXXXXX):** Course Capacity & Maximum Course Limit Check (Max 20 courses)
* **Yap Kai Bin (TPXXXXXX):** Text-file Audit Log of Daily Operations (`activity.log`), Auto-generated Enrollment IDs (`E001`, `E002`, ...)

---

## System Architecture & File Structure

### Python Modules (`.py`)
* **`main.py`**: Entry point and central navigation controller (`mainmenu`) connecting the Member, Course, Enrollment, and Resource modules.
* **`login.py`**: Central authentication and account management module supporting first-time admin setup, student self-registration, student/admin login, password changes, and role verification (`is_admin`).
* **`member.py`**: Handles Member CRUD operations, auto-generated Member IDs, input validation, and PBKDF2-HMAC-SHA256 password hashing.
* **`course.py` & `cmdatabase.py`**: Manages Course CRUD operations, course capacity checks, and persistent storage in `cmstorage.txt`.
* **`enrollment.py`**: Manages student course enrollments, status updates (`Active`, `Completed`, `Withdrawn`), and enrollment searches.
* **`audit_logger.py`**: Records timestamped `ENROLL`, `UPDATE`, and `DELETE` actions to `activity.log`.
* **`resources.py` & `rr_filebackup.py`**: Manages Resource CRUD operations, multi-field filtering, and automatic `_backup.txt` file creation/restoration.

### Data Storage Files (`.txt` / `.log`)
* **`admins.txt`**: Stores administrator usernames, random salts, and PBKDF2 password hashes.
* **`student_accounts.txt`**: Stores student usernames, random salts, and PBKDF2 password hashes.
* **`student_links.txt`**: Maps student usernames to their auto-generated `MemberID`.
* **`members.txt`**: Stores member records (`MemberID|Name|Age|Gender|ContactNumber|Email|StartDate`).
* **`cmstorage.txt`**: Stores course records (`CourseID|Name|Instructor|Duration|Fee|Capacity`).
* **`enrollment.txt`**: Stores enrollment records (`EnrollmentID|MemberID|CourseID|Date|Status`).
* **`resources.txt`**: Stores learning hub resources (`ResourceID|Name|Type|Quantity|Status`).
* **`activity.log`**: Stores timestamped audit logs of enrollment operations.

---

## Role-Based Access Control (Admin vs. Student)

| Module | Administrator Access (`admins.txt`) | Student / Normal User Access (`student_accounts.txt`) |
| :--- | :--- | :--- |
| **Members (`member.py`)** | Full CRUD + Create/Remove Admin Accounts | Read own linked membership profile only |
| **Courses (`course.py`)** | Full CRUD (Add, Edit, Delete, View Courses) | Read-only (View existing courses) |
| **Enrollments (`enrollment.py`)** | Full CRUD + View System Audit Logs | Read-only (View & search enrollments) |
| **Resources (`resources.py`)** | Full CRUD (Create, Read, Update, Delete, Filter) | Read-only (View, Search, and Filter resources) |

---

## How to Run the Program

1. Ensure **Python 3** is installed on your machine (uses only Python standard library modules—no external `pip` packages required).
2. Extract all `.py` files into the same folder.
3. Open a terminal or IDE in that folder and run:
   ```bash
   python main.py