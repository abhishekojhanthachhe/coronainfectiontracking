import sqlite3

con = sqlite3.connect('user1.db')
c = con.cursor()

c.execute('''
    CREATE TABLE users(
    userID INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT UNIQUE,
    password TEXT,
    address TEXT, 
    email TEXT,
    phonenumber TEXT,
    infected INTEGER,
    deviceID TEXT UNIQUE
    );
    ''')

c.execute('''
CREATE TABLE places(
    placeID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    address TEXT,
    email TEXT,
    QRCode TEXT
);
''')

c.execute('''
CREATE TABLE hospitals(
    hid INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, 
    password TEXT, 
    address TEXT,
    email TEXT,
    verified BIT
); 
''')

c.execute('''
CREATE TABLE visit(
    visitID INTEGER PRIMARY KEY AUTOINCREMENT,
    user INTEGER,
    place INTEGER,
    entry_date TEXT,
    entry_time TEXT,
    exit_date TEXT,
    exit_time TEXT,
    FOREIGN KEY (user) REFERENCES users(userID) ON DELETE CASCADE,
    FOREIGN KEY (place) REFERENCES places(placeID) ON DELETE CASCADE
); 
''')

c.execute('''
CREATE TABLE agents(
    aid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);
''')

c.execute('''
INSERT INTO agents(username,password) VALUES ('a1','pw');
''')


con.commit() 
con.close()

