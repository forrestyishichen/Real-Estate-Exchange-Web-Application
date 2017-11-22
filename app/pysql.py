    


1
    table = 'user'
    cursor.execute("SELECT * from %s" % table)



2

    cursor.execute("SELECT * from user")


3
	cursor.execute("SELECT password from User where Username='" + username + "'")



4
	cursor.execute('''SELECT owner_num FROM owner WHERE ssn = %s''',(username))
	


5
	cursor.execute("SELECT * FROM {} WHERE ssn = '{}'" .format(role, username))

	