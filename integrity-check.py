import os
import hashlib
import pickle
import sys
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurations
HASH_FILE = 'log_hashes.pkl'
LOG_FILE = 'integrity_check.log'
ALGORITHMS = ['sha256', 'sha512', 'md5']
SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port
SENDER_EMAIL = 'you@example.com'  # Replace with your email
RECEIVER_EMAIL = 'receiver@example.com'  # Replace with the recipient's email

# Logger setup
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to compute hash based on selected algorithm
def compute_hash(file_path, algorithm='sha256'):
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

# Function to send email notification
def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, 'your_password')  # Replace with your email password
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        logging.info(f"Email sent to {RECEIVER_EMAIL} regarding {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Function to initialize hash storage
def init(directory, algorithm='sha256'):
    log_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            log_hashes[file_path] = compute_hash(file_path, algorithm)
    
    with open(HASH_FILE, 'wb') as f:
        pickle.dump(log_hashes, f)
    
    logging.info(f"Initialization completed for directory: {directory} with {algorithm} hashing.")
    print("Hashes stored successfully.")
    send_email('Log Integrity Initialized', f"Hashes for logs in {directory} have been successfully initialized.")

# Function to check the integrity of a log file
def check(file_path, algorithm='sha256'):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    try:
        with open(HASH_FILE, 'rb') as f:
            stored_hashes = pickle.load(f)
    except FileNotFoundError:
        print("Error: Hash storage file not found. Please initialize first.")
        return
    
    current_hash = compute_hash(file_path, algorithm)
    stored_hash = stored_hashes.get(file_path, None)
    
    if stored_hash is None:
        print(f"Error: No stored hash for {file_path}. Please initialize first.")
    elif current_hash == stored_hash:
        print(f"Status: Unmodified")
        logging.info(f"File {file_path} is unmodified.")
    else:
        print(f"Status: Modified (Hash mismatch)")
        print(f"Stored hash: {stored_hash}")
        print(f"Current hash: {current_hash}")
        logging.warning(f"File {file_path} has been modified (Hash mismatch).")
        send_email('Log File Modified', f"File {file_path} has been modified. Hash mismatch detected.")

# Function to update the hash of a file
def update(file_path, algorithm='sha256'):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    try:
        with open(HASH_FILE, 'rb') as f:
            stored_hashes = pickle.load(f)
    except FileNotFoundError:
        print("Error: Hash storage file not found. Please initialize first.")
        return
    
    current_hash = compute_hash(file_path, algorithm)
    stored_hashes[file_path] = current_hash
    
    with open(HASH_FILE, 'wb') as f:
        pickle.dump(stored_hashes, f)
    
    print("Hash updated successfully.")
    logging.info(f"Hash for {file_path} updated successfully.")
    send_email('Log File Hash Updated', f"The hash for {file_path} has been updated.")

# Function to reset hashes
def reset(directory, algorithm='sha256'):
    os.remove(HASH_FILE)
    print("Hash storage reset successfully.")
    logging.info(f"Hash storage reset for directory: {directory}. Re-initialization needed.")
    send_email('Log Integrity Reset', f"Hash storage has been reset. Please reinitialize the integrity check.")

# Main function to handle command-line arguments
def main():
    if len(sys.argv) < 3:
        print("Usage: ./integrity-check <command> <file_or_directory> [algorithm]")
        sys.exit(1)

    command = sys.argv[1]
    file_or_directory = sys.argv[2]
    algorithm = sys.argv[3] if len(sys.argv) > 3 else 'sha256'

    if algorithm not in ALGORITHMS:
        print(f"Error: Unsupported algorithm '{algorithm}'. Supported algorithms are {ALGORITHMS}.")
        sys.exit(1)

    if command == 'init':
        init(file_or_directory, algorithm)
    elif command == 'check':
        check(file_or_directory, algorithm)
    elif command == 'update':
        update(file_or_directory, algorithm)
    elif command == 'reset':
        reset(file_or_directory, algorithm)
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == '__main__':
    main()
