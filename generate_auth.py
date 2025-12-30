import bcrypt
import getpass
import os

def generate_htpasswd(username, password):
    # Determine the salt and hash the password
    # Nginx basic auth supports crypt(), md5, sha1, and bcrypt (in newer versions)
    # But standard Apache htpasswd uses md5 or crypt. 
    # For generated files compatible with most systems, we can use the 'apache2-utils' format.
    # However, to be dependency-free in python is harder for apr1-md5.
    # Let's use bcrypt which is supported by Nginx (auth_basic_user_file).
    
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return f"{username}:{hashed.decode('utf-8')}"

def main():
    print("Generate .htpasswd file for Nginx Basic Auth")
    username = input("Enter Username: ").strip()
    if not username:
        print("Username cannot be empty")
        return
        
    password = getpass.getpass("Enter Password: ")
    if not password:
        print("Password cannot be empty")
        return
        
    entry = generate_htpasswd(username, password)
    
    os.makedirs("nginx", exist_ok=True)
    with open("nginx/.htpasswd", "w") as f:
        f.write(entry + "\n")
        
    print(f"Success! Credentials for user '{username}' written to nginx/.htpasswd")

if __name__ == "__main__":
    try:
        import bcrypt
    except ImportError:
        print("Error: bcrypt module is missing.")
        print("Please run: pip install bcrypt")
        exit(1)
    main()
