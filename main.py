import random
import string

def generate_random_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Generate a random code of 8 characters
random_code = generate_random_code()
print("Your random code:", random_code)
print("hallo")