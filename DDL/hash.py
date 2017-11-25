from werkzeug.security import generate_password_hash, check_password_hash
import csv

file1 = "passo.txt"
file2 = "passh.txt"

with open(file1, 'r') as f1:
    with open(file2, 'w') as f2:
        for key in f1.readlines():
            f2.write("'" + generate_password_hash(key) + "'" + '\n')

# key = "kx#a@fqmH7RKYP2"
# hashed_key = generate_password_hash(key)

# if check_password_hash(hashed_key, key):
# 	print(hashed_key)

# print(len(hashed_key))

