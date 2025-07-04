from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Contact
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == os.getenv("ADMIN_USERNAME") and password == os.getenv("ADMIN_PASSWORD"):
            session['admin_logged_in'] = True
            return redirect(url_for('view_contacts'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('login.html')


@app.route('/contacts', methods=['GET'])
def view_contacts():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    contacts = Contact.query.order_by(Contact.id).all()
    return render_template('contacts.html', contacts=contacts)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
