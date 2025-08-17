"""
Author : Harsh Chakravarti
"""



# Import regular expressions module for pattern matching and validation logic
import re


# Set of common weak passwords to be rejected immediately.
# This list is product-aware: it blocks passwords that are trivially guessable and often used in attacks.
COMMON_PASSWORDS = {"password", "123456", "qwerty", "letmein", "admin", "iloveyou"}


def has_excessive_repetition(password):

    """
    Reject passwords with excessive repetition (e.g., 'aaaaaaa', '11111111').
    This logic is product-aware: it blocks passwords that show signs of random key smashing or brute-force attempts,
    which are not intentional or human-like.
    """

    # If any character repeats more than half the length, it's likely not intentional
    for char in set(password):
        if password.count(char) > len(password) // 2:
            return True
    return False

def has_keyboard_pattern(password):

    """
    Reject passwords with common keyboard patterns (e.g., 'qwertyuiop', 'asdfghjkl').
    This logic interprets ambiguous guidance: it blocks visually obvious patterns that are easy to guess and not human-like.
    """
    patterns = ["qwerty", "asdfgh", "zxcvbn", "12345", "password"]
    for pat in patterns:
        if pat in password.lower():
            return True
    return False

def has_ambiguous_characters(password):

    """
    Penalize passwords with visually confusing characters (e.g., 'l1I!i', 'O0o').
    This logic is product-aware: it improves usability and reduces user frustration by avoiding ambiguous passwords.
    Only rejects if a group makes up more than half the password, so strong passwords with a few ambiguous characters are still allowed.
    """
    ambiguous_groups = ["l1I", "O0o"]
    for group in ambiguous_groups:
        count = sum(password.count(c) for c in group)
        if count > len(password) // 2:
            return True
    return False

def looks_human_like(password):

    """
    Encourage passwords that look like phrases or combinations of words/numbers/symbols.
    This logic is flexible and product-aware: it allows for evolving requirements and defends usability.
    Requires all three character classes (letters, digits, symbols) to ensure passwords are strong and human-like.
    """

    has_letter = bool(re.search(r"[A-Za-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    return has_letter and has_digit and has_symbol

# --- Password Examples ---
# The following passwords are used to demonstrate the validator's logic.
# Output for each password is a boolean: True (accepted), False (rejected)

# Accepted passwords (should return True):
# These passwords have the following characteristics:
# - Sufficient length (8+ characters)
# - Mix of uppercase, lowercase, digits, and symbols
# - No excessive repetition or keyboard patterns
# - No ambiguous or confusing characters
# - No whitespace
# - Not a common password

# - Mimic human behavior: They look like something a person would create, such as combining words, numbers, and symbols in a memorable way (e.g., a phrase, a name with a year, or a word with a special character).
# Examples:
# 1. StrongPass1!      # Combines a word, uppercase, digit, and symbol
# 2. Valid$Pass2       # Looks like a phrase with a symbol and digit
# 3. MyPass@123        # Mimics a human pattern: word + symbol + numbers
# 4. Test#Pass99       # Two words, symbol, and year-like digits
# 5. Harsh_2025@       # Name, year, and symbol
# 6. Python@321        # Technology, symbol, and sequence
# 7. Good#Pass77       # Positive word, symbol, and double digit
# 8. Secure$Pass88     # Security word, symbol, and double digit
# 9. Alpha@2024        # Word, symbol, and year
# 10. ValidPass#10     # Phrase, symbol, and number

# Rejected passwords (should return False):
# 1. short1!           # Too short
# 2. NoNumber!         # No digit
# 3. nouppercase1!     # No uppercase
# 4. NOLOWERCASE1!     # No lowercase
# 5. NoSpecial123      # No special character
# 6. 1234567890        # Only digits
# 7. password          # Common password
# 8. qwerty123         # Keyboard pattern
# 9. Pass word1!       # Contains whitespace
# 10. onlylowercase    # Only lowercase, no digit or symbol


def is_valid_password(password):

    """
    Product-aware password validator.
    Returns True if password is strong, False otherwise.

    --- Thought Process ---
    This function is designed to balance security and usability, interpreting ambiguous requirements from a product team.
    The logic is modular and flexible, so new rules can be added as requirements evolve.
    Each check is defended with a comment explaining why it is included:
    - Baseline checks ensure passwords are not trivially guessable and have basic strength.
    - Advanced checks block brute-force, key-smashing, keyboard patterns, ambiguous characters, and encourage human-like structure.
    - Output is always boolean: True (accepted), False (rejected).
    """

    # Baseline security checks (standard rules)
    # These rules ensure passwords are not trivially guessable and have basic strength.

    if password in COMMON_PASSWORDS:
        return False  # Defends against trivial passwords
    
    if len(password) < 8:
        return False  # Defends against short passwords
    
    if re.search(r"\s", password):
        return False  # Defends against whitespace confusion
    
    if not re.search(r"[A-Z]", password):
        return False  # Ensures variation (usability)
    
    if not re.search(r"[a-z]", password):
        return False  # Ensures variation (usability)
    
    if not re.search(r"\d", password):
        return False  # Ensures variation (usability)
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False  # Ensures variation (usability)


    # Advanced product-aware checks
    # These rules interpret ambiguous guidance and defend usability and intentionality.

    if has_excessive_repetition(password):
        return False  # Defends against brute-force and key-smashing
    
    if has_keyboard_pattern(password):
        return False  # Defends against easy-to-guess patterns
    
    if has_ambiguous_characters(password):
        return False  # Improves usability
    
    if not looks_human_like(password):
        return False  # Encourages human-like structure


    # If all checks pass, password is valid
    return True



# Accepted passwords (from accepted_passwords.txt):
# These passwords should pass all validation rules and be accepted by the program.
# StrongPass1!, Valid$Pass2, MyPass@123, Test#Pass99, Harsh_2025@, Python@321, Good#Pass77, Secure$Pass88, Alpha@2024, ValidPass#10

# Rejected passwords (from rejected_passwords.txt):
# These passwords should fail one or more validation rules and be rejected by the program.
# short1!, NoNumber!, nouppercase1!, NOLOWERCASE1!, NoSpecial123, 1234567890, password, qwerty123, Pass word1!, onlylowercase



def check_passwords_from_list(passwords, expected_result):
    """
    Checks passwords from a provided list using is_valid_password.
    Prints the password and whether it was accepted or rejected, in aligned columns for clarity.
    This function simulates real-world testing and helps defend the logic of the validator.
    """
    for pwd in passwords:
        result = is_valid_password(pwd)
        print(f"{pwd:<16}  {str(result):<5}  (Expected: {expected_result})")

if __name__ == "__main__":
    # Lists of accepted and rejected passwords for testing
    accepted_passwords = [
        "StrongPass1!", "Valid$Pass2", "MyPass@123", "Test#Pass99", "Harsh_2025@",
        "Python@321", "Good#Pass77", "Secure$Pass88", "Alpha@2024", "ValidPass#10"
    ]
    rejected_passwords = [
        "short1!", "NoNumber!", "nouppercase1!", "NOLOWERCASE1!", "NoSpecial123",
        "1234567890", "password", "qwerty123", "Pass word1!", "onlylowercase"
    ]

    # Simulate real-world testing by checking accepted and rejected passwords from lists
    print("Checking accepted passwords:")
    check_passwords_from_list(accepted_passwords, True)
    print("\nChecking rejected passwords:")
    check_passwords_from_list(rejected_passwords, False)

    # Loop to allow user to validate multiple passwords until they choose to stop
    while True:
        user_pwd = input("\nEnter a password to validate (or type 'exit' to stop): ")
        if user_pwd.lower() == 'exit':
            print("Exiting password validator.")
            break
        is_valid = is_valid_password(user_pwd)
        print(is_valid)
