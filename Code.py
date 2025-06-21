import os
import base64
from cryptography.fernet import Fernet
import getpass
import json

KEY_FILE = "key.key"
DATA_FILE = "passwords.json"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()

def load_passwords():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_passwords(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_password():
    account = input("Enter account name: ")
    password = getpass.getpass("Enter password: ")

    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(password.encode())

    data = load_passwords()
    data[account] = encrypted.decode()
    save_passwords(data)
    print("Password saved.")

def get_password():
    account = input("Enter account name: ")
    data = load_passwords()

    if account not in data:
        print("Account not found.")
        return

    key = load_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data[account].encode()).decode()
    print(f"Password for {account}: {decrypted}")

def list_accounts():
    data = load_passwords()
    if not data:
        print("No passwords saved.")
    else:
        print("Saved accounts:")
        for account in data:
            print(f"- {account}")

def main():
    while True:
        print("1. Add Password")
        print("2. Get Password")
        print("3. List Accounts")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            get_password()
        elif choice == "3":
            list_accounts()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
main()
