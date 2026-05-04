#!/usr/bin/env python3
"""
Encrypt/Decrypt docs/ folder using Fernet symmetric encryption
Usage:
    python encrypt_docs.py encrypt    # Encrypt all docs files
    python encrypt_docs.py decrypt    # Decrypt all docs files
    python encrypt_docs.py genkey      # Generate new encryption key
"""

import os
import sys
import json
from pathlib import Path
from cryptography.fernet import Fernet

DOCS_DIR = Path(__file__).parent / "docs"
KEY_FILE = Path(__file__).parent / ".encryption.key"
MANIFEST_FILE = Path(__file__).parent / ".encrypted_files.json"

def generate_key():
    """Generate and save a new encryption key"""
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    print(f"✅ Encryption key generated: {KEY_FILE}")
    print(f"⚠️  SAVE THIS KEY SAFELY! You'll need it to decrypt on other machines.")
    print(f"🔑 Key: {key.decode()}")

def load_key():
    """Load encryption key from file"""
    if not KEY_FILE.exists():
        print("❌ Key file not found! Generate one with: python encrypt_docs.py genkey")
        sys.exit(1)
    return KEY_FILE.read_bytes()

def encrypt_file(file_path, cipher):
    """Encrypt a single file"""
    try:
        content = file_path.read_bytes()
        encrypted = cipher.encrypt(content)
        file_path.write_bytes(encrypted)
        return True
    except Exception as e:
        print(f"❌ Error encrypting {file_path}: {e}")
        return False

def decrypt_file(file_path, cipher):
    """Decrypt a single file"""
    try:
        content = file_path.read_bytes()
        decrypted = cipher.decrypt(content)
        file_path.write_bytes(decrypted)
        return True
    except Exception as e:
        print(f"❌ Error decrypting {file_path}: {e}")
        return False

def encrypt_docs():
    """Encrypt all files in docs/"""
    if not DOCS_DIR.exists():
        print(f"❌ docs/ directory not found!")
        return
    
    key = load_key()
    cipher = Fernet(key)
    
    encrypted_files = []
    for file_path in DOCS_DIR.rglob("*"):
        if file_path.is_file():
            if encrypt_file(file_path, cipher):
                encrypted_files.append(str(file_path.relative_to(DOCS_DIR)))
                print(f"🔒 Encrypted: {file_path.name}")
    
    # Save manifest
    MANIFEST_FILE.write_text(json.dumps(encrypted_files, indent=2))
    print(f"\n✅ Encrypted {len(encrypted_files)} files in docs/")

def decrypt_docs():
    """Decrypt all files in docs/"""
    if not DOCS_DIR.exists():
        print(f"❌ docs/ directory not found!")
        return
    
    key = load_key()
    cipher = Fernet(key)
    
    decrypted_files = []
    for file_path in DOCS_DIR.rglob("*"):
        if file_path.is_file():
            if decrypt_file(file_path, cipher):
                decrypted_files.append(str(file_path.relative_to(DOCS_DIR)))
                print(f"🔓 Decrypted: {file_path.name}")
    
    print(f"\n✅ Decrypted {len(decrypted_files)} files in docs/")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "genkey":
        generate_key()
    elif command == "encrypt":
        encrypt_docs()
    elif command == "decrypt":
        decrypt_docs()
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
