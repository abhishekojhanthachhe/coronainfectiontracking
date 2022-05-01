from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_qrcode import QRcode
import os
import sqlite3 
import models as dbHandler
import secrets
import string
from datetime import datetime



app = Flask(__name__)
app.secret_key= "__privatekey__"
qrcode = QRcode(app)
    
#to generate unique device id for visitors
def generate_id(S, len):
    secure = 'start'

    while secure in S:
        secure = ''.join((secrets.choice(string.ascii_letters + string.digits) for i in range(len)))
    return secure


@app.route('/')
def home():
    return render_template('home.html')


# LOGIN ROUTE
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        
        con = sqlite3.connect("user1.db")
        c = con.cursor()

        #login visitor
        if c.execute("SELECT userID from users WHERE username = ?",(username,)).fetchone():
            user =  c.execute("SELECT password from users WHERE username = ?",(username,)).fetchone()
            pw = user[0]
        
            if pw == password:
                session['visitor'] = username
                flash('Logged In successfully', 'success')
                con.close()
                return redirect(url_for('user_home'))
            else:
                flash('Wrong Password', 'error')
                return render_template('login.html')

        #login place
        elif c.execute("SELECT placeID from places WHERE username = ?",(username,)).fetchone():
            place =  c.execute("SELECT password from places WHERE username = ?",(username,)).fetchone()
            pw = place[0]

            if pw == password:
                flash('Logged In successfully', 'success')
                session['place'] = username
                con.close()
                return redirect(url_for('place_home'))
            else:
                flash('Wrong Password', 'error')
                return render_template('login.html')

        #login hospital
        elif c.execute("SELECT hid from hospitals WHERE name = ?",(username,)).fetchone():
            hospital =  c.execute("SELECT password from hospitals WHERE name = ?",(username,)).fetchone()
            pw = hospital[0]

            if pw == password:
                flash('Logged In successfully', 'success')
                session['hospital'] = username
                con.close()
                return redirect(url_for('hospital_home'))
            else:
                flash('Wrong Password', 'error')
                return render_template('login.html')

        #login agent
        elif c.execute("SELECT aid from agents WHERE username = ?",(username,)).fetchone():
            agent =  c.execute("SELECT password from agents WHERE username = ?",(username,)).fetchone()
            pw = agent[0]

            if pw == password:
                flash('Logged In successfully', 'success')
                session['agent'] = username
                con.close()
                return redirect(url_for('agent_home'))
            else:
                flash('Wrong Password', 'error')
                return render_template('login.html')
        
        else:
            msg = "This user does not exist"
            con.close()
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')



#HOME PAGE USER
@app.route('/user')
def user_home():

    if 'visitor' in session:
        username = session['visitor']
        return render_template('user_home.html', username=username)
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))


#HOME PAGE PLACES
@app.route('/place')
def place_home():
    if 'place' in session:
        place = session['place']

        con = sqlite3.connect("user1.db")
        c = con.cursor()

        c.execute("SELECT * FROM places WHERE username = ?", (place, ))
        result = c.fetchone()

        con.close()

        return render_template('place_home.html', place=result)
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))



#HOME PAGE HOSPITALS
@app.route('/hospital')
def hospital_home():
    if 'hospital' in session:
        hospital = session['hospital']

        con = sqlite3.connect("user1.db")
        c = con.cursor()

        c.execute("SELECT * FROM hospitals WHERE name = ?", (hospital, ))
        result = c.fetchone()
        c.execute('SELECT * FROM users')
        resultu = c.fetchall()

        con.close()

        return render_template('hospital_home.html', hospital=result, users=resultu)
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))


#HOME PAGE AGENTS
@app.route('/agent')
def agent_home():
    if 'agent' in session:
        agent = session['agent']

        con = sqlite3.connect("user1.db")
        c = con.cursor()

        c.execute("SELECT * FROM agents WHERE username = ?", (agent, ))
        result = c.fetchone()
        c.execute('SELECT * FROM users')
        resultu = c.fetchall()
        c.execute('SELECT * FROM hospitals')
        resulth = c.fetchall()
        c.execute('SELECT * FROM places')
        resultp = c.fetchall()

        con.close()

        return render_template('agent_home.html', agent=result, users=resultu, hospitals=resulth, places=resultp)
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))
    


#SIGUNP FOR USER
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    msg = None
    if request.method == "POST":
    
        username = request.form.get('username')
        password = request.form.get('password')
        address = request.form.get('address')
        number = request.form.get('number')
        email = request.form.get('email')

        con = sqlite3.connect("user1.db")
        c = con.cursor()

        #check if user is registered already
        c.execute("SELECT userID FROM users WHERE email = ?", (username, email))
        user = c.fetchone()

        if not user:
            #set of all registered device_id to ensure uniqueness when calling generate_id function
            devices = set()
            devices.add('start')

            c.execute("SELECT userID, deviceID FROM users")
            ans = c.fetchall()

            for index, row in enumerate(ans):
                devices.add(row[0])
            device = generate_id(devices, 32)

            con.close()

            try:
                dbHandler.insertUser(username,password,address,number,email, device)
                flash("Your account has been created", "success")
                return redirect(url_for('home'))
            except:
                msg = "Something went wrong"
        else:
            flash("An account already exists with that email. Log in instead", "error")
            con.close()
            return redirect(url_for('login'))

    return render_template("RegisterUser.html", msg = msg)



#SIGNUP FOR PLACES
@app.route('/signup_place', methods = ['GET', 'POST'])
def signup_place():
    msg = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        email = request.form['email']

        con = sqlite3.connect("user1.db")
        c = con.cursor()

        #check if place is registered already
        c.execute('''
        SELECT placeID FROM places WHERE username= ? OR email = ?''', 
        (username, email))
        place = c.fetchone()

        if not place:
            try:
                dbHandler.insertPlace(username,password,address,email)
            except:
                msg = "Something went wrong!"

            c.execute("SELECT placeID FROM places WHERE username = ?", [username])
            place = c.fetchone()
            id = place[0]

            code = f"http://127.0.0.1:5000/enter/{id}"

            c.execute("UPDATE places SET QRCode = ? WHERE placeID = ?", (code, id))
            con.commit()
            con.close()

            flash("Your Place is registered", "success")
            return redirect(url_for('home'))
        else:
            flash("An account already exists with that name and/or email. Log in instead", "error")
            con.close()
            return redirect(url_for('login'))
    return render_template("RegisterPlace.html", msg = msg)
            

#SIGNUP FOR HOSPITALS
@app.route('/signup_hospital', methods = ['GET', 'POST'])
def signup_hospital():
    msg = None
    if(request.method == "POST"):
        name = request.form['name']
        password = request.form['password']
        address = request.form['address']
        email = request.form['email']
        
        con = sqlite3.connect("user1.db")
        c = con.cursor()

        #check if hospital is registered already
        c.execute("SELECT hid FROM hospitals WHERE name= ? OR email = ?", (name, email))
        user = c.fetchone()
        con.close()

        if not user:
            try:
                dbHandler.insertHospital(name,password,address,email)
                flash("Your account has been created", "success")
                return redirect(url_for('home'))
            except:
                msg = "Something went wrong"
        else:
            flash("A hospital already exists with that name or email. Log in instead", "error")
            return redirect(url_for('login'))

    return render_template("RegisterHospital.html", msg = msg)


#LIST OF ALL REGISTERED PLACES
@app.route("/places")
def all_places():
    if 'visitor' in session:
        con = sqlite3.connect("user1.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM places")
        places = cur.fetchall()
        cur.close()
        return render_template("places.html", places=places)
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))



''' FOR VISITORS TO ENTER A PLACE'''
@app.route("/enter/<int:id>")
def visit(id):
    if 'visitor' in session:
        con = sqlite3.connect("user1.db")
        cur = con.cursor()

        visitor = session['visitor']

        cur.execute("SELECT userID FROM users WHERE username = ?", (visitor, ))
        res = cur.fetchone()

        id = dbHandler.insertVisits(res[0], id)

        session['visits'] = id

        con.close()
        flash("You're in!", "success")
        return render_template('enter.html')
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))


#For hospitals to mark as infected or not infected
@app.route("/update_user_status/<int:id>")
def update_user_status(id):
    if 'hospital' in session:
        con = sqlite3.connect("user1.db")
        cur = con.cursor()
        
        cur.execute("SELECT infected FROM users WHERE userID = ?", (id, ))
        res = cur.fetchone()
        res = 0 if res[0] else 1
        
        cur.execute("UPDATE users SET infected = ? WHERE userID = ?", (res, id))
        con.commit()

        con.close()
        return redirect(url_for('hospital_home'))
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))



#For agents to verify hospitals
@app.route("/update_hospital_status/<int:id>")
def update_hospital_status(id):
    if 'agent' in session:
        con = sqlite3.connect("user1.db")
        cur = con.cursor()
        
        cur.execute("UPDATE hospitals SET verified = 1 WHERE hid = ?", (id,))
        con.commit()

        con.close()
        return redirect(url_for('agent_home'))
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))


#FOR AGENTS TO SEARCH VISITORS TO A PLACE BY DATE
@app.route('/search', methods=['POST'])
def search_by_date():
    if 'agent' in session:
        place = request.form.get('place')
        datefrom = request.form.get('from')
        dateto = request.form.get('to')

        con = sqlite3.connect("user1.db")
        cur = con.cursor()

        cur.execute('SELECT * FROM places WHERE username = ?', (place, ))
        pid = cur.fetchone()

        cur.execute('''
        SELECT u.username, u.address, u.email, u.phonenumber, u.infected FROM visit as vi 
        JOIN users as u
        ON vi.user = u.userID AND vi.place = ? 
        WHERE DATE(entry_date) BETWEEN ? AND ?''', (pid[0], datefrom, dateto))

        users = cur.fetchall()
        con.close()

        return render_template('search.html', dfrom=datefrom, dto=dateto, users=users, place=pid)        
    else:
        flash('Unauthorized access!', 'error')
        return redirect(url_for('home'))



'''LOGOUT ROUTE'''
@app.route("/logout")
def logout():
    if 'visits' in session:
        con = sqlite3.connect("user1.db")
        cur = con.cursor()

        id = session['visits']
        dbHandler.logoutFunction(id)

        session.pop('visits', None)
    if 'visitor' in session:
        session.pop('visitor', None)
    if 'place' in session: 
        session.pop('place', None)
    if 'hospital' in session: 
        session.pop('hospital', None)
    if 'agent' in session:
        session.pop('agent', None)

    return redirect(url_for('home'))