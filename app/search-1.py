@app.route('/search_property', methods=['GET', 'POST'])
def search_property():
    if request.method == 'POST':
        lowprice = request.form['lowprice']
        if lowprice is None:
            lowprice = 0
        highprice = request.form['highprice']
        if highprice is None:
            highprice = 1e9
        whereprice = " AND price >= {} AND price <={}".format(lowprice, highprice)

        area = request.form['area']
        wherearea = ""
        if area is not None:
            whrerearea = " AND area = {}".format(area)

        orderby = request.form['orderby']
        orderbyq = " ORDER BY"
        if orderby is None:
            orderbyq += " property.property_id"
        else:
            orderbyq += " {}".format(orderby)

        sqlcmd = "SELECT property.property_id, status, price, area \
                  FROM property, property_parameter \
                  WHERE property.property_id = property_parameter.property_id"

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sqlcmd + whereprice + wherearea + orderbyq)

    entries = []
    for row in cursor.fetchall():
        entries.append([row[0], row[1], row[2], row[3]])
    cursor.close()

    return render_template('search_property.html', entries=entries)
