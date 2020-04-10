from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_mail import Message, Mail
from flask import g
from wtforms import Form, TextField, validators

import sqlite3
import os

DATABASE = "./database.db"


mail = Mail()

app = Flask(__name__)

app.secret_key = 'development key'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'passion3193@gmail.com'
app.config['MAIL_PASSWORD'] = 'vandana@7070'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'passion3193@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = True
app.config['DEBUG'] = True

if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE users (subject text, message text)''')
    conn.commit()
    cur.execute("INSERT INTO users VALUES('Greetings!', 'On this ospicious day.We would like to greet you')")
    cur.execute("INSERT INTO users VALUES('Thankyou', 'Thankyou for joining the company')")
    cur.execute("INSERT INTO users VALUES('new year', 'A very happy new year')")
    
    conn.commit()
    conn.close()


# helper method to get the database since calls are per thread,
# and everything function is a new thread when called
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# helper to close
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()






mail.init_app(app)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/index')
def index():
  cur = get_db().cursor()
  res = cur.execute("select * from users")
  return render_template("index.html", users=res)


#class InputForm(Form):
 #   r = TextField(validators=[validators.InputRequired()])

@app.route('/hi', methods=['GET', 'POST'])
def hi():
  cur = get_db().cursor()
  
   
  #form = InputForm(request.form)
  if request.method == 'POST':
      #name=cur.execute("select fname from users")
      #r=name.data
      r = request.form['numb']
      cur.execute("select message from users where subject=?",[r])
      s = cur.fetchall()

      msg = Message(r, sender='passion3193@gmail.com', recipients=['vandanapathare32@gmail.com'])
      msg.body = """
      
      %s
      """ % (s[0])
      mail.send(msg)
      return render_template("view_output.html",users=s)
  else:
      name=cur.execute("select subject from users")
      
      print(name)
      return render_template("view_input.html",name=name)

      


  
if __name__ == '__main__':
  app.run(debug=True)
