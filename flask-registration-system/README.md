Here’s a clean **`README.md`** for your Flask register/login OTP app that’s GitHub-ready and safe to push.

---

````markdown
# Flask Register/Login App with Email OTP Verification

A secure Flask web application that provides:
- **User registration** with email verification via OTP
- **Secure password storage** using Bcrypt
- **reCAPTCHA integration** for bot prevention
- **Rate limiting** to prevent brute-force attacks
- **CSRF protection** for form submissions

---

## 🚀 Features
- Email OTP verification (expires in 5 minutes)
- Strong password policy enforcement
- reCAPTCHA validation on forms
- Secure session handling
- Rate limiting for OTP and login attempts
- Phone number validation (10 digits)
- Environment-based configuration (no hardcoded secrets)

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/register_login.git
cd register_login
````

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Mac/Linux

pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
RECAPTCHA_SECRET=your_recaptcha_secret
DATABASE_URI=sqlite:///database.db
```

### 4. Run the Application

```bash
python app.py
```

The app will run at:
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 📦 Project Structure

```
register_login/
│── app.py                # Main Flask app
│── templates/            # HTML templates
│── static/               # CSS, JS, Images
│── instance/              # Database storage (ignored in Git)
│── .env                   # Environment variables (ignored in Git)
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation
```

---

## 🔒 Security Features

* **Password Hashing**: Bcrypt used for secure password storage
* **CSRF Protection**: Enabled with Flask-WTF
* **reCAPTCHA**: Prevents automated bot attacks
* **Rate Limiting**: Limits OTP and login attempts
* **Environment Variables**: Secrets are never hardcoded
* **Phone Validation**: Ensures valid 10-digit numbers

---

## 📧 Email OTP Flow

1. User registers → OTP generated and emailed
2. OTP expires in 5 minutes
3. User can attempt OTP entry only 5 times before re-registration is required


## 📝 License

This project is for **educational purposes only**. Use it at your own risk in production environments.

