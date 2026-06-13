import bcrypt

def hash_password(password):
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash



def is_password_valid(password):
    # Check if password contains at least:
    # - 8 characters
    # - 1 upper and lower case character each
    # - 1 special character
    # - 1 number
    password_error = []

    if len(password) < 8:
        password_error.append("Password must be at least 8 characters")
    if not any(char.isdigit() for char in password):
        password_error.append("Password must contain at least 1 number")
    if not any(char.isupper() for char in password):
        password_error.append("Password must contain at least 1 upper case letter")
    if not any(char.islower() for char in password):   
        password_error.append("Password must contain at least 1 lower case letter")
    special_char = """!#$%&'()"*+,-./:;<=>?@[\]^_`{|}~""" 
    if not any(char in special_char for char in password):
        password_error.append("Password must contain at least 1 special character")
    
    if password_error:    
        return False, password_error
    else:
        return True, []