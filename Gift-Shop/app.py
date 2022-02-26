from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import secrets

from werkzeug.utils import redirect

app = Flask(__name__)
app.run(host='0.0.0.0', debug=True)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    e_id = db.Column(db.Integer, primary_key=True)
    e_email = db.Column(db.String(20), nullable=False)
    e_password = db.Column(db.String(25), nullable=False)


class Customer(db.Model):
    ct_id = db.Column(db.Integer, primary_key=True)
    ct_name = db.Column(db.String(20), nullable=False)
    ct_product = db.Column(db.String(25), nullable=False)
    ct_email = db.Column(db.String(30), nullable=False)


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html', title='Home')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["email"]
        passwo = request.form["password"]

        login1 = Employee.query.filter_by(e_email=uname, e_password=passwo).first()
        if login1 is not None:
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/view')
def view():
    return render_template('view.html', title='View', data1=Employee.query.all(), data2=Customer.query.all())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        id = request.form['id']
        email = request.form['email']
        passw = request.form['pass']
        enter = Employee(e_id = id, e_email = email, e_password = passw)
        db.session.add(enter)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")