from logging import log
import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')


conn = psycopg2.connect(database='megausers', user='postgres', password='1', host='localhost', port='5432')
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM tableusers WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor.execute("insert into tableusers (name,login,password) values (%s,%s,%s)",
                       (str(name), str(login), str(password)))
        conn.commit()
        return redirect("/login/")
    return render_template('registration.html')
