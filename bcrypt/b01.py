import bcrypt

hashed = bcrypt.hashpw('123xyz'.encode('utf8'), bcrypt.gensalt())

print(hashed)