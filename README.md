# Log File Integrity Verification Tool

## Overview

This tool verifies the integrity of log files by utilizing cryptographic hashing algorithms (e.g., SHA-256) to ensure that no unauthorized changes have been made to the files. The tool supports various operations such as initialization, integrity checking, hash updates, and reset functionality. Additionally, it sends email notifications for tampered files and maintains detailed logs of all operations.

## Features

- **Multiple Hash Algorithms**: Support for SHA-256, SHA-512, MD5, and other hashing algorithms.
- **File Integrity Checking**: Detect modifications to log files by comparing current hashes with previously stored ones.
- **Email Notifications**: Receive email alerts when a file is modified or when a hash is updated.
- **Logging**: Detailed logging of all actions, such as initialization, checks, updates, and resets.
- **Re-initialization**: Reset the hash storage and reinitialize integrity checks for log files.
- **Backup/Restore**: Backup and restore the hash storage securely.
- **Permissions Validation**: Ensure that the tool can only access files with the proper permissions.
  
## Requirements

- Python 3.x
- `smtplib` (for email notifications)
- `hashlib` (for hashing algorithms)
- `pickle` (for storing hashes)

## Setup

1. Clone the repository or download the `integrity-check.py` script.
2. Install Python 3.x if you don’t already have it.

```bash
# Clone the repo
git clone https://github.com/peymansohi/integrity-checker.git
cd log-integrity-check

# (Optional) Set up a virtual environment
python3 -m venv venv
source venv/bin/activate
```

## Configuration

Before running the script, you may need to configure the email settings for notifications.

### Email Configuration

In the script, locate the following section and configure the SMTP server and email addresses:

```python
SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port
SENDER_EMAIL = 'you@example.com'  # Replace with your email
RECEIVER_EMAIL = 'receiver@example.com'  # Replace with the recipient's email
```

Replace the placeholder values with your actual email server and credentials.

### Hash Algorithms

The tool supports the following hashing algorithms:

- `sha256`
- `sha512`
- `md5`

You can specify the desired algorithm when running the tool. If not specified, it defaults to `sha256`.

## Usage

The tool supports several commands:

- **`init`**: Initializes and stores hashes of all files in a given directory.
- **`check`**: Checks the integrity of a specific file by comparing its current hash with the stored hash.
- **`update`**: Updates the stored hash of a specific file.
- **`reset`**: Resets the hash storage (useful for re-initialization).

### Initialize Hashes

To initialize the hashes for all log files in a directory:

```bash
./integrity-check init /var/log sha256
```

This will store the hashes of all files in `/var/log` using SHA-256.

### Check File Integrity

To check the integrity of a specific file:

```bash
./integrity-check check /var/log/syslog sha256
```

The output will indicate whether the file has been modified or is unmodified.

### Update File Hash

If a file’s content changes, you can update its stored hash:

```bash
./integrity-check update /var/log/syslog sha256
```

### Reset Hash Storage

If you need to reset the hash storage (for example, after clearing logs or making significant changes):

```bash
./integrity-check reset /var/log sha256
```

This will remove the current hash storage and require re-initialization.

### Email Notifications

When a modification is detected in a file, an email notification will be sent to the recipient specified in the script configuration.

## Log File

All operations are logged in `integrity_check.log`. This log file contains detailed entries for each command execution, including timestamps and any detected changes in log files.

### Example Log Entry:

```
2023-04-01 12:34:56 - File /var/log/syslog has been modified (Hash mismatch).
2023-04-01 12:35:01 - Hash for /var/log/syslog updated successfully.
```

## Commands Summary

| Command         | Description                                                          |
|-----------------|----------------------------------------------------------------------|
| `init <dir>`    | Initializes and stores hashes for all files in the specified directory. |
| `check <file>`  | Checks the integrity of a specific file.                             |
| `update <file>` | Updates the hash for a specific file.                                |
| `reset <dir>`   | Resets the hash storage for the specified directory.                 |

## Example Usage

### Initializing hashes:

```bash
./integrity-check init /var/log sha256
# Hashes stored successfully.
```

### Checking file integrity:

```bash
./integrity-check check /var/log/syslog sha256
# Status: Unmodified
```

```bash
./integrity-check check /var/log/auth.log sha256
# Status: Modified (Hash mismatch)
```

### Updating a file’s hash:

```bash
./integrity-check update /var/log/syslog sha256
# Hash updated successfully.
```

### Resetting hash storage:

```bash
./integrity-check reset /var/log sha256
# Hash storage reset successfully.
```

## Security Considerations

- Ensure the script has appropriate file and directory permissions to prevent unauthorized access.
- The email credentials should be securely stored and not hard-coded in production environments.
- Use strong cryptographic algorithms like SHA-256 or SHA-512 to reduce the risk of hash collisions.
  
## Advanced Features (Optional)

- **Backup/Restore Hashes**: You can back up the `log_hashes.pkl` file to secure storage and restore it later if needed.
- **Multiple Hash Algorithms**: The tool allows you to choose between several hashing algorithms.
- **Permissions Checking**: The script ensures it has the appropriate permissions to access the files and directories.


---

https://roadmap.sh/projects/file-integrity-checker