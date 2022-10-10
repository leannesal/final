import os
import sqlite3 as sql
from functools import wraps
from flask import (Flask, flash, redirect, render_template, request,session, url_for)
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

#model for contract employee table
class Contract_employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.Text)
    joined = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Text, nullable=False)


#model for non-contract employee table
class Non_contract_employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    contact = db.Column(db.Text)
    role = db.Column(db.Text, nullable=False)

#User and admin Login
@app.route('/') 
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["pass"]
        con=sql.connect("db_users.db")
        curs=con.cursor()
        curs.execute("select * from users where EMAIL=? and PASS=?",(email,password))
        account=curs.fetchone()
        if account:
            session['logged_in']=True
            session['id']=account[1]
            flash('Login is successful')
            return redirect('home')
        else:
            flash('Login is invalid')
    return render_template("login.html")
  
#Check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized')
			return redirect(url_for('login'))
	return wrap
  
#User Registration where is_admin attribute takes value False
@app.route('/registration',methods=['POST','GET'])
def registration():
    if request.method=='POST':
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["pass"]
        is_admin=False
        con=sql.connect("db_users.db")
        curs=con.cursor()
        curs.execute("insert into users(NAME,PASS,EMAIL,is_admin) values(?,?,?,?)",(name,password,email,is_admin))
        con.commit()
        flash('User registration is successful')
        return redirect('login')
    return render_template("registration.html")

#admin registration where is_admin attribute takes value True
@app.route('/create_admin',methods=['POST','GET'])
def create_admin():
    if request.method=='POST':
        name=request.form["name"]
        email=request.form["email"]
        password=request.form["pass"]
        is_admin=True
        con=sql.connect("db_users.db")
        curs=con.cursor()
        curs.execute("insert into users(NAME,PASS,EMAIL,is_admin) values(?,?,?,?)",(name,password,email,is_admin))
        con.commit()
        flash('Admin registration is successful')
        return redirect('login')
    return render_template("admin_registration.html")

#Home page
@app.route("/home")
@is_logged_in
def home():
    contract_employee=Contract_employees.query.all()
    non_contract_employee=Non_contract_employees.query.all()
    return render_template("home.html",no_contract_info=non_contract_employee,employees_info=contract_employee)

#Add a new contract employee
@app.route("/new_contract_employee",methods=['POST','GET'])
def new_contract_employee():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        address=request.form['address']
        joined=request.form['joined']
        role=request.form['role']
        employee=Contract_employees(firstname=firstname,
                                lastname=lastname, 
                                email=email, 
                                address=address, 
                                joined=joined, 
                                role=role)
        db.session.add(employee)
        db.session.commit()
        flash('Employee has been added')
        return redirect(url_for("home"))
    return render_template("new_contract_employee.html")

#Add a new non-contract employee
@app.route("/new_no_contract_employee",methods=['POST','GET'])
def new_no_contract_employee():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        contact=request.form['contact']
        role=request.form['role']
        employee=Non_contract_employees(firstname=firstname,
                                    lastname=lastname, 
                                    email=email, 
                                    contact=contact, 
                                    role=role)
        db.session.add(employee)
        db.session.commit()
        flash('No contract employee has been added')
        return redirect(url_for("home"))
    return render_template("new_no_contract_employee.html")

#Edit contract employee
@app.route("/edit_employee/<string:id>",methods=['POST','GET'])
def edit_employee(id):
    employee=Contract_employees.query.get_or_404(id)
    if request.method=='POST':
        employee.firstname=request.form['Firstname']
        employee.lastname=request.form['Lastname']
        employee.email=request.form['Email']
        employee.address=request.form['Address']
        employee.joined=request.form['Joined']
        employee.role=request.form['Role']
        db.session.add(employee)
        db.session.commit()
        flash('Employee has been updated')
        return redirect(url_for("home"))
    return render_template("edit_employee.html",employees_info=employee)

#Edit non-contract employee
@app.route("/edit_no_contract_employee/<string:id>",methods=['POST','GET'])
def edit_no_contract_employee(id):
    employee=Non_contract_employees.query.get_or_404(id)
    if request.method=='POST':
        employee.firstname=request.form['Firstname']
        employee.lastname=request.form['Lastname']
        employee.email=request.form['Email']
        employee.contact=request.form['Contact']
        employee.role=request.form['Role']
        db.session.commit()
        flash('No contract employee has been updated')
        return redirect(url_for("home"))
    return render_template("edit_no_contract_employee.html",no_contract_info=employee)

#Delete a contract emoployee   
@app.route("/delete_employee/<int:id>",methods=['GET','POST'])
def delete_employee(id):
        employee=Contract_employees.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        flash('Employee Deleted')
        return redirect(url_for("home"))

#Delete a non-contract emoployee 
@app.route("/delete_no_contract_employee/<int:id>",methods=['GET','POST'])
def delete_no_contract_employee(id):
    employee=Non_contract_employees.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Non contract employee Deleted')
    return redirect(url_for("home"))


#Logout
@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))
    
if __name__=='__main__':
    app.run(debug=True)

