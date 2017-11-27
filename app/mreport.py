@app.route('/marketreport', methods=['GET'])
def market_report():
    q = []
    # total properties
    q.append("SELECT Count(*) FROM property")

    # onsale
    q.append("SELECT Count(*) FROM property WHERE status = 'On Sale'")
    # lowest onsale price
    q.append(
        "SELECT price FROM property WHERE status = 'On Sale' ORDER BY price LIMIT 1")
    # highest onsale price
    q.append(
        "SELECT price FROM property WHERE status = 'On Sale' ORDER BY price DESC LIMIT 1")
    # average onsale price
    q.append("SELECT Avg(price) FROM property WHERE status = 'On Sale'")

    # recentsold
    q.append("SELECT Count(*) FROM property WHERE status = 'Sold'")
    # lowest sold price
    q.append("SELECT price FROM property WHERE status = 'Sold' ORDER BY price LIMIT 1")
    # highest sold price
    q.append(
        "SELECT price FROM property WHERE status = 'Sold' ORDER BY price DESC LIMIT 1")
    # average sold price
    q.append("SELECT Avg(price) FROM property WHERE status = 'Sold'")

    # openhouses
    q.append("SELECT Count(*) FROM open_house")

    conn = mysql.connect()
    cursor = conn.cursor()
    res = []
    for sq in q:
        cursor.execute(sq)
        r = cursor.fetchone()
        if r is None:
            r = ""
        res.append(r)

    return render_template('market_report.html', entries=res)
