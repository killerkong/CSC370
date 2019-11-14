from hashlib import sha256

h = sha256()
h.update(b'Rz1995227')
hash = h.hexdigest()
print(hash)

password = "Rz1995227"

def hash(value):
    code = ((127*value + 31) % 257) % 254
    return chr(code)

def encode(password):
    code = [ord(char) for char in password]
    encode = [hash(char) for char in code]
    return ''.join([elem for elem in encode])
    
print(encode(password))