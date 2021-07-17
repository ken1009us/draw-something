import os

from cs50 import SQL
from helper import apology, login_required
from flask import Flask, render_template, redirect, flash, jsonify, session, request
from tempfile import mkdtemp
from werkzeug.exceptions import HTTPException, InternalServerError, default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///draw.db")


# Index page
@app.route("/")
@login_required
def index():
    return render_template("index.html")


# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        if not db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            username = request.form.get("username")
            hash_pw = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", username, hash_pw)

        else:
            return apology("Username already used")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route('/token')
@login_required
def generate_token():
    # get credentials from environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')
    sync_service_sid = os.getenv('TWILIO_SYNC_SERVICE_SID')
    username = db.execute("SELECT username FROM users WHERE id=:user_id", user_id=session["user_id"])[0]["username"]

    # create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity=username)
    # create a Sync grant and add to token
    sync_grant = SyncGrant(sync_service_sid)
    token.add_grant(sync_grant)
    return jsonify(identity=username, token=token.to_jwt().decode())


# Log in page
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    # submit the form
    username = request.form.get("username")
    password = request.form.get("password")

    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Log out page
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        if not request.form.get("old_password"):
            return apology("Must provide password", 400)
        elif not request.form.get("new_password"):
            return apology("Must provide password", 400)
        elif not request.form.get("confirmed_password"):
            return apology("Must provide password", 400)

        old_pw = request.form.get("old_password")
        new_pw = request.form.get("new_password")
        com_pw = request.form.get("confirmed_password")

        current_pw = db.execute("SELECT hash FROM users WHERE id=:user_id", user_id=session["user_id"])[0]["hash"]

        if check_password_hash(current_pw, old_pw) == False:
            return apology("Must provide your correct current password", 400)

        elif check_password_hash(current_pw, new_pw) == True:
            return apology("Password is already used currently", 400)

        elif new_pw != com_pw:
            return apology("Password and confirmation password do not match", 400)

        hash_pw = generate_password_hash(new_pw, method='pbkdf2:sha256', salt_length=8)
        db.execute("UPDATE users SET hash = :hash_pw WHERE id = :user_id", hash_pw=hash_pw, user_id=session["user_id"])

        flash("Changed!")

        return redirect("/login")

    else:
        return render_template("change.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
