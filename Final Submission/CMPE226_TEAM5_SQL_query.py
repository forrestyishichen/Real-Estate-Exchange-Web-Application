#Retrieve property_id, property status for admin site to perform updates
cursor.execute("SELECT property_id, status FROM property")

#Retrieve offer_num, offer status for admin site to perform updates
cursor.execute("SELECT offer_num, status FROM offer")

#Update property status
conn.autocommit(False)
try:
    cursor.execute("UPDATE property SET status = '{}' \
                    WHERE property_id ='{}'" .format(update,id))
    conn.commit()
    cursor.close()
    flash('Updated!')
except:
    error = 'There are some errors!'
    conn.rollback()

#Update offer status
conn.autocommit(False)
try:
	cursor.execute("UPDATE offer SET status = '{}' \
                    WHERE offer_num ='{}'" .format(update, id))
    conn.commit()
    cursor.close()
    flash('Updated!')
except:
    error = 'There are some errors!'
    conn.rollback()

#Import data from files
conn.autocommit(False)
try:
    cursor.execute("Source {}" .format(path))
    conn.commit()
    cursor.close()
    flash('You have import some data!')
except:
    error = 'There are some errors!'
    conn.rollback()

#Retrieve property data to load search page with initial data
cursor.execute("SELECT property.property_id, property.status, \
        property.price, property_parameter.area from property inner \
        join property_parameter on property.property_id = \
        property_parameter.property_id")

#Property search feature
myquery = "SELECT property.property_id, property.status, property.asking_price, property_parameter.area \
                      FROM property, property_parameter \
                      WHERE property.property_id = property_parameter.property_id"

            if lowprice == '':
                lowprice = 0

            if highprice == '':
                highprice = 999999999

            priceq = " AND price >= {} AND price <= {}".format(lowprice, highprice)
            myquery = myquery + priceq  

            if area != '':
                addsq = " AND area = '{}'".format(area)
                myquery = myquery + addsq

            if room_num != '':
                addsq = " AND property_parameter.room_num = {}".format(room_num)
                myquery = myquery + addsq

            if bath_num != '':
                addsq = " AND property_parameter.bath_num = {}".format(bath_num)
                myquery = myquery + addsq

            if garage_num != '':
                addsq = " AND property_parameter.garage_num = {}".format(garage_num)
                myquery = myquery + addsq

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(myquery)

#Open house search feature
myquery = "SELECT open_house.oh_num, open_house.property_id, \
                       open_house.start_date, open_house.end_date, property.asking_price \
                      FROM open_house, property, property_parameter\
                      WHERE open_house.property_id = property.property_id \
                      AND property.property_id = property_parameter.property_id"

            if lowprice == '':
                lowprice = 0

            if highprice == '':
                highprice = 999999999

            priceq = " AND property.price >= {} AND property.price <= {}".format(lowprice, highprice)
            myquery = myquery + priceq

            if area != '':
                addsq = " AND property_parameter.area = '{}'".format(area)
                myquery = myquery + addsq

            if room_num != '':
                addsq = " AND property_parameter.room_num = {}".format(room_num)
                myquery = myquery + addsq

            if bath_num != '':
                addsq = " AND property_parameter.bath_num = {}".format(bath_num)
                myquery = myquery + addsq

            if garage_num != '':
                addsq = " AND property_parameter.garage_num = {}".format(garage_num)
                myquery = myquery + addsq

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(myquery)

#Buyer open house visiting
conn.autocommit(False)
try:
    cursor.execute("INSERT INTO oh_visit (buyer_num, agent_num, \
        oh_num) VALUES('{}', '{}', '{}' \
        )" .format(session['roleid'], myagent, oh_num))
    conn.commit()
    cursor.close()
    flash('Thank you for visiting!')
except:
    flash('There are some errors!')
    conn.rollback() 

#Retrieve data from views for market report
cursor.execute("SELECT * FROM report_sold")
cursor.execute("SELECT * FROM report_onsale")

#Retrieve property record for login owner
cursor.execute("SELECT property_id, status, list_date \
	from property where owner_num = '{}'" .format(session['roleid']))

#Owner new property registration
conn.autocommit(False)
try:
    cursor.execute("INSERT INTO property (property_id, status, \
        asking_price, list_date, owner_num) VALUES('{}', 'On Sale', \
        '{}', '{}', '{}')" .format(property_id, asking_price, list_date, session['roleid']))
    cursor.execute("INSERT INTO property_parameter (property_id, \
        room_num, bath_num, garage_num, lot_size, zip_code, area) \
        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')" .format(property_id, \
        room_num, bath_num, garage_num, lot_size, zip_code, area))
    conn.commit()
    cursor.close()
    flash('You Home were registered!')
except:
    error = 'There are some errors!'
    conn.rollback()

#Retrieve offer record for login owner
cursor.execute("SELECT offer.property_id, offer.offer_num, offer.price, \
    offer.offer_date, offer.agent_num, offer.status \
    from offer inner join property on offer.property_id = property.property_id \
    where property.owner_num = '{}'".format(session['roleid']))

#Retrieve open house record for login agent
cursor.execute("SELECT oh_num, property_id, start_date, end_date  \
            FROM open_house WHERE agent_num = '{}'".format(session['roleid']))

#Agent new open house registration
conn.autocommit(False)
try:
    cursor.execute("INSERT INTO open_house (agent_num, oh_num, \
        start_date, end_date, property_id) VALUES('{}', '{}', \
        '{}', '{}', '{}')" .format(session["roleid"], \
        ('oh_' + str(num[0] + 1)), start_date, end_date, property_id))
    conn.commit()
    cursor.close()
    flash('You Open House were registered!')
    return redirect(url_for('agent_openhouse'))
except:
    error = 'There are some errors!'
    conn.rollback()

#Retrieve commission record for login agent
cursor.execute("SELECT count(offer.status)\
            FROM offer WHERE offer.agent_num = '{}' \
            AND offer.status = 'Deal'".format(session['roleid']))

cursor.execute("SELECT total_commission FROM agent \
            where agent_num = '{}'" .format(session['roleid']))

#Retrieve offer record for login buyer
cursor.execute("SELECT offer_num, property_id, price, offer_date, status, agent_num \
            FROM offer WHERE buyer_num = '{}'".format(session['roleid']))

#Buyer new offer registration
conn.autocommit(False)
try:
    cursor.execute("INSERT INTO offer (buyer_num, offer_num, \
        price, status, offer_date, property_id, agent_num) VALUES('{}', '{}', \
        '{}', 'Progress', '{}', '{}', '{}')" .format(session["roleid"], \
        ('offer_' + str(num[0] + 1)), price, offer_date, property_id, agent_num))
    conn.commit()
    cursor.close()
    flash('You Offer were registered!')
    return redirect(url_for('buyer_offer'))
except:
    error = 'There are some errors!'
    conn.rollback()

#Retrieve open house visiting record for login buyer
cursor.execute("SELECT property_id, oh.agent_num, end_date \
            FROM open_house oh, oh_visit ohv\
            WHERE oh.agent_num = ohv.agent_num \
                AND oh.oh_num = ohv.oh_num \
                AND ohv.buyer_num = '{}'".format(session['roleid']))

#User new role registration
cursor.execute("CALL role_check('{}','{}')" .format(role,session['ssn']))
cursor.execute("CALL role_insert('{}','{}','{}')" .format(role,session['roleid'],session['ssn']))

#New user registration
conn.autocommit(False)
try:
    cursor.execute("INSERT INTO user (ssn, user_name, password, bdate, \
        address, email) VALUES('{}', '{}', '{}', '{}', '{}', '{}')" .format(ssn \
        , username, hashed_password, bdate, address, email))
    cursor.execute("INSERT INTO name (user_name, fname, minit, lname \
        ) VALUES('{}', '{}', '{}', '{}')" .format(username, fname, minit, lname))
    conn.commit()
    cursor.close()
    flash('You were registered, %s' % escape(username))
    return redirect(url_for('login'))
except:
    error = 'There are some errors!'
    conn.rollback()

#Retrieve property detail for detail page
cursor.execute("SELECT property.property_id, property.status, \
        property.price, property_parameter.room_num, property_parameter.bath_num, \
        property_parameter.garage_num, property_parameter.lot_size, \
        property_parameter.zip_code, property_parameter.area from property inner \
        join property_parameter on property.property_id = \
        property_parameter.property_id where property.property_id = '{}'" .format(property_id))

#Accept offer update to relate tables
conn.autocommit(False)
try:
    cursor.execute("UPDATE property SET status = 'Sold', price = '{}' \
        WHERE property_id ='{}'" .format(newprice,newid))
    cursor.execute("UPDATE offer SET status = 'Deal' \
        WHERE offer_num ='{}'" .format(offer_num))
    if newagent is not None:
        cursor.execute("UPDATE agent SET total_commission = {} \
            WHERE agent_num ='{}'" .format(newtotal,newagent))
    conn.commit()
    cursor.close()
    flash('Congratulations, %s!' % escape(username))
except:
    flash('There are some errors!')
    conn.rollback()