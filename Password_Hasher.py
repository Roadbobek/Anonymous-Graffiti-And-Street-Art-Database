import bcrypt

# Function to hash the password
def generate_hash(password):
    # bcrypt generates its own salt and includes it in the hash, making it more secure
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8') # Store as a string


# Replace 'Password123' with the actual password you want to use
password_to_hash = """Password123"""

# Hash the password
hashed_pw = generate_hash(password_to_hash)
print(f"Your hashed password: {hashed_pw}")