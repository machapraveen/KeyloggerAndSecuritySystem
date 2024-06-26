from cryptography.fernet import Fernet

# Load the key from the file
def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher_suite = Fernet(key)

# Decrypt the text log
with open('key_log.txt', 'rb') as file:
    encrypted_data = file.readlines()
    decrypted_data = [cipher_suite.decrypt(line).decode() for line in encrypted_data]
    print("Decrypted Text Log:")
    print("\n".join(decrypted_data))

# Decrypt the JSON log
with open('key_log.json', 'rb') as file:
    encrypted_data = file.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    print("\nDecrypted JSON Log:")
    print(decrypted_data)
