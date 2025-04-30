import os
import hashlib
import pickle
import sys

HASH_FILE = 'log_hashes.pkl'

# Function to compute SHA-256 hash of a file
def compute_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# Function to initialize hash storage
def init(directory):
    log_hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            log_hashes[file_path] = compute_hash(file_path)
    
    with open(HASH_FILE, 'wb') as f:
        pickle.dump(log_hashes, f)
    
    print("Hashes stored successfully.")

# Function to check the integrity of a single log file
def check(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    try:
        with open(HASH_FILE, 'rb') as f:
            stored_hashes = pickle.load(f)
    except FileNotFoundError:
        print("Error: Hash storage file not found. Please initialize first.")
        return
    
    current_hash = compute_hash(file_path)
    stored_hash = stored_hashes.get(file_path, None)
    
    if stored_hash is None:
        print(f"Error: No stored hash for {file_path}. Please initialize first.")
    elif current_hash == stored_hash:
        print(f"Status: Unmodified")
    else:
        print(f"Status: Modified (Hash mismatch)")
        print(f"Stored hash: {stored_hash}")
        print(f"Current hash: {current_hash}")

# Function to update the hash of a file
def update(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return
    
    try:
        with open(HASH_FILE, 'rb') as f:
            stored_hashes = pickle.load(f)
    except FileNotFoundError:
        print("Error: Hash storage file not found. Please initialize first.")
        return
    
    current_hash = compute_hash(file_path)
    stored_hashes[file_path] = current_hash
    
    with open(HASH_FILE, 'wb') as f:
        pickle.dump(stored_hashes, f)
    
    print("Hash updated successfully.")

# Main function to handle command-line arguments
def main():
    if len(sys.argv) < 3:
        print("Usage: ./integrity-check <command> <file_or_directory>")
        sys.exit(1)

    command = sys.argv[1]
    file_or_directory = sys.argv[2]

    if command == 'init':
        init(file_or_directory)
    elif command == 'check':
        check(file_or_directory)
    elif command == 'update':
        update(file_or_directory)
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == '__main__':
    main()
