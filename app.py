from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from models import db, Contact
import os
from dotenv import load_dotenv
from flask import jsonify
from utils import get_secondary_contacts, create_contact, format_response

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

@app.route('/identify', methods=['POST'])
def add_or_update_contact():
    phone_number = request.json.get('phoneNumber')
    email = request.json.get('email')

    if not phone_number and not email:
        return jsonify({"error": "Phone number or email is required"}), 400

    phone_contact = Contact.query.filter_by(phoneNumber=phone_number).first() if phone_number else None
    email_contact = Contact.query.filter_by(email=email).first() if email else None

    # Case 1: No existing contacts – create new primary
    if not phone_contact and not email_contact:
        new_contact = create_contact(phone_number, email, 'primary')
        return jsonify(format_response(new_contact)), 200

    # Determine primary contact
    primary_contact = None
    related_contacts = []

    if phone_contact and email_contact:

        # Case 3: Both exist and exactly match – return the same contact
        if phone_contact.id == email_contact.id:
            return jsonify(format_response(phone_contact)), 200
        
    else:
        # Case 2: Only one exists – reuse it as primary, create new secondary
        valid_object = phone_contact or email_contact
        primary_contact_id = valid_object.id if valid_object.linkPrecedence == 'primary' else valid_object.linkedId
        primary_contact = Contact.query.get(primary_contact_id)
        create_contact(phone_number, email, 'secondary', linked_id=primary_contact_id)

        related_contacts = get_secondary_contacts(primary_contact_id)

    return jsonify(format_response(primary_contact, related_contacts)), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
