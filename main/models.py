import sqlite3 as sql

def insertUser(username,password,address,phone, email, deviceID):
    con = sql.connect("user1.db")
    cur = con.cursor()
    cur.execute('''
    INSERT INTO users(username, password, address, email, phonenumber, infected, deviceID) 
    VALUES (?,?,?,?,?,?, ?)''', (username,password,address,email, phone, 0, deviceID) )
    con.commit()
    con.close()

def insertPlace(username,password,address,email):
    con = sql.connect("user1.db")
    cur = con.cursor()
    cur.execute('''INSERT INTO places(username, password, address, email) 
    VALUES (?,?,?,?)''',(username,password,address,email) )
    con.commit()
    con.close()

def insertHospital(name, password, address, email):
    con = sql.connect("user1.db")
    cur = con.cursor()
    cur.execute('''INSERT INTO hospitals(name, password, address, email, verified) 
    VALUES (?,?,?,?,0)''',(name,password,address,email) )
    con.commit()
    con.close()


def insertVisits(userid, placeid):
    con = sql.connect("user1.db")
    cur = con.cursor()
    cur.execute('''INSERT INTO visit(user, place, entry_date, entry_time) 
    VALUES (?,?, date('now'), time('now', 'localtime'))''',(userid, placeid) )
    con.commit()

    cur.execute("select seq from sqlite_sequence where name='visit'")
    id = cur.fetchone()

    con.close()
    
    return id[0]


def logoutFunction(visitID):
    con = sql.connect("user1.db")
    cur = con.cursor()

    cur.execute('''UPDATE visit SET exit_date=date('now'), exit_time=time('now', 'localtime') WHERE visitID = ?''', 
        (visitID, ))

    con.commit()
    con.close()


def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM users")
	users = cur.fetchall()
	con.close()
	return users