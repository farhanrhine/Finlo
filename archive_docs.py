#!/usr/bin/env python3
"""
Create encrypted archive of docs/ folder
Usage:
    python archive_docs.py create   # Create encrypted docs.tar.gz.encrypted
    python archive_docs.py extract  # Extract docs.tar.gz.encrypted and decrypt
"""

import os
import sys
import tarfile
import shutil
from pathlib import Path
from cryptography.fernet import Fernet

DOCS_DIR = Path(__file__).parent / "docs"
KEY_FILE = Path(__file__).parent / ".encryption.key"
ARCHIVE_NAME = "docs.tar.gz"
ENCRYPTED_ARCHIVE = "docs.tar.gz.encrypted"

def load_key():
    """Load encryption key from file"""
    if not KEY_FILE.exists():
        print("❌ Key file not found! Run encrypt_docs.py genkey first")
        sys.exit(1)
    return KEY_FILE.read_bytes()

def create_archive():
    """Create encrypted tar.gz archive of docs/"""
    if not DOCS_DIR.exists():
        print(f"❌ docs/ directory not found!")
        return
    
    # Step 1: Decrypt docs if they are encrypted
    print("🔓 Decrypting docs (if needed)...")
    os.system(f"uv run encrypt_docs.py decrypt 2>/dev/null")
    
    # Step 2: Create tar.gz
    print(f"📦 Creating {ARCHIVE_NAME}...")
    with tarfile.open(ARCHIVE_NAME, "w:gz") as tar:
        tar.add(DOCS_DIR, arcname="docs")
    print(f"✅ Archive created: {ARCHIVE_NAME}")
    
    # Step 3: Encrypt the archive
    print(f"🔒 Encrypting archive...")
    key = load_key()
    cipher = Fernet(key)
    
    with open(ARCHIVE_NAME, "rb") as f:
        archive_data = f.read()
    
    encrypted_data = cipher.encrypt(archive_data)
    
    with open(ENCRYPTED_ARCHIVE, "wb") as f:
        f.write(encrypted_data)
    
    # Step 4: Clean up
    os.remove(ARCHIVE_NAME)
    print(f"✅ Encrypted archive created: {ENCRYPTED_ARCHIVE}")
    print(f"⚠️  Now run: git add {ENCRYPTED_ARCHIVE} && git commit -m 'Add encrypted docs archive'")

def extract_archive():
    """Extract and decrypt docs.tar.gz.encrypted"""
    if not Path(ENCRYPTED_ARCHIVE).exists():
        print(f"❌ {ENCRYPTED_ARCHIVE} not found!")
        return
    
    key = load_key()
    cipher = Fernet(key)
    
    print(f"🔓 Decrypting {ENCRYPTED_ARCHIVE}...")
    with open(ENCRYPTED_ARCHIVE, "rb") as f:
        encrypted_data = f.read()
    
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        return
    
    # Write to temporary tar file
    with open(ARCHIVE_NAME, "wb") as f:
        f.write(decrypted_data)
    
    # Extract
    print(f"📦 Extracting {ARCHIVE_NAME}...")
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    
    with tarfile.open(ARCHIVE_NAME, "r:gz") as tar:
        tar.extractall()
    
    # Cleanup
    os.remove(ARCHIVE_NAME)
    print(f"✅ docs/ folder extracted and ready to use!")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "create":
        create_archive()
    elif command == "extract":
        extract_archive()
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
