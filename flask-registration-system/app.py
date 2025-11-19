from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf import CSRFProtect
from datetime import datetime, timedelta
import random
import string
import re
import requests
import os

# -------------------
# Flask App Config
# -------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Load secrets from environment variables for better security
app.secret_key = os.environ.get("SECRET_KEY", "a-simple-flask-key-12345")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True  # This is usually the default for port 587

app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = ('AuthApp', os.environ.get("MAIL_USERNAME"))

# Load RECAPTCHA keys from the environment
app.config['RECAPTCHA_SECRET'] = os.environ.get("RECAPTCHA_SECRET")
app.config['RECAPTCHA_SITE_KEY'] = os.environ.get("RECAPTCHA_SITE_KEY")

# -------------------
# Security Extensions
# -------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)
csrf = CSRFProtect(app)

# -------------------
# Init Extensions
# -------------------
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# -------------------
# Database Model
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(300))
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    otp_hash = db.Column(db.String(200), nullable=True)  # Hashed OTP
    otp_expiry = db.Column(db.DateTime, nullable=True)
    otp_attempts = db.Column(db.Integer, default=0)      # Limit attempts

# -------------------
# Utility Functions
# -------------------
def is_strong_password(password):
    """Check password strength."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def verify_recaptcha(response_token):
    """Verify Google reCAPTCHA, securely retrieving the secret key from app.config."""
    
    # --- THIS LINE MUST BE ADDED OR FIXED ---
    secret_key = app.config.get("RECAPTCHA_SECRET") 
    
    if not secret_key:
        print("ERROR: RECAPTCHA_SECRET is missing from app.config.")
        return False

    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    
    # This line now works because 'secret_key' is defined:
    payload = {'secret': secret_key, 'response': response_token} 
    r = requests.post(verify_url, data=payload)
    result = r.json()
    return result.get('success', False)

# -------------------
# Routes
# -------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        confirm_password = request.form['confirm_password']
        phone = request.form['phone']
        gender = request.form['gender']

        # Verify reCAPTCHA
        if not verify_recaptcha(request.form.get('g-recaptcha-response')):
            flash("Please complete the CAPTCHA to continue.", "danger")
            return redirect(url_for('register'))

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for('register'))

        # Confirm password match
        if password_input != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('register'))

        # Validate password strength
        if not is_strong_password(password_input):
            flash("Password must be at least 8 characters long, include uppercase, lowercase, digit, and special character.", "danger")
            return redirect(url_for('register'))
        
        #  Server-side phone validation
        if not re.fullmatch(r"\d{10}", phone):
            flash("Phone number must be exactly 10 digits", "danger")
            return redirect(url_for('register'))

        # Hash password
        password = bcrypt.generate_password_hash(password_input).decode('utf-8')

        # Generate and hash OTP (mix of uppercase letters + digits)
        characters = string.ascii_uppercase + string.digits
        otp_plain = ''.join(random.choices(characters, k=6))
        otp_hash = bcrypt.generate_password_hash(otp_plain).decode('utf-8')
        expiry_time = datetime.utcnow() + timedelta(minutes=5)

        # Create user
        user = User(email=email, password=password, phone=phone, gender=gender,
                    otp_hash=otp_hash, otp_expiry=expiry_time)
        db.session.add(user)
        db.session.commit()

        # Send OTP email
        msg = Message("Your OTP Code", recipients=[email])
        msg.body = f"Hi,\n\nYour OTP code is: {otp_plain}\nIt will expire in 5 minutes."
        mail.send(msg)

        flash("Registration successful! Check your email for the OTP.", "success")
        return redirect(url_for('verify_otp', email=email))

    return render_template('register.html')

@app.route('/verify', methods=['GET', 'POST'])
@limiter.limit("5 per 10 minutes")
def verify_otp():
    email = request.args.get('email') or request.form.get('email')

    if request.method == 'POST':
        otp_entered = request.form['otp'].strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid credentials or verification code.", "danger")
            return redirect(url_for('register'))

        # Check reCAPTCHA
        if not verify_recaptcha(request.form.get('g-recaptcha-response')):
            flash("Please complete the CAPTCHA to continue.", "danger")
            return redirect(url_for('verify_otp', email=email))

        # Expiry check
        if not user.otp_expiry or datetime.utcnow() > user.otp_expiry:
            flash("OTP expired. Please register again.", "danger")
            return redirect(url_for('register'))

        # Attempt limit
        if user.otp_attempts >= 5:
            flash("Too many OTP attempts. Please register again.", "danger")
            return redirect(url_for('register'))

        # Check OTP
        if user.otp_hash and bcrypt.check_password_hash(user.otp_hash, otp_entered):
            user.is_verified = True
            user.otp_hash = None
            user.otp_expiry = None
            user.otp_attempts = 0
            db.session.commit()
            flash("Email verified successfully! You can now log in.", "success")
            return redirect(url_for('login'))
        else:
            user.otp_attempts += 1
            db.session.commit()
            flash("Invalid OTP.", "danger")

    return render_template('verify.html', email=email)

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        # Verify reCAPTCHA
        if not verify_recaptcha(request.form.get('g-recaptcha-response')):
            flash("Please complete the CAPTCHA to continue.", "danger")
            return redirect(url_for('login'))

        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            if user.is_verified:
                session.clear()  # clear old session to prevent fixation
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash("Please verify your email with the OTP sent.", "warning")
                return redirect(url_for('verify_otp', email=email))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', email=user.email)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('login'))

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# -------------------
# Run App
# -------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5001)
