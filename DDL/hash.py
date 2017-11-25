from werkzeug.security import generate_password_hash, check_password_hash
import csv

file1 = "pass-original.txt"
file2 = "pass-hashed.txt"



with open(file1, 'w') as f1:
    with open(file2, 'w') as f2:
        for i in range(100000001, 100000031):
            key = str(i)
            f1.write("'" + key + "'" + '\n')
            h = generate_password_hash(key)
            f2.write("'" + h + "'" + '\n')

# key = "kx#a@fqmH7RKYP2"
# hashed_key = generate_password_hash(key)

# if check_password_hash(hashed_key, key):
# 	print(hashed_key)

# print(len(hashed_key))

