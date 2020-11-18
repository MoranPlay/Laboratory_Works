from Cryptodome.Cipher import AES
import hashlib

password = b'kaput'
key = hashlib.md5(password)
print(key)
print(key.hexdigest())
print(key.hexdigest().encode('utf-8'))
#print(key.hexdigest())