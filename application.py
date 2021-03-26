from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, common_time_slot

# Configure application
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meetings.db'
db = SQLAlchemy(app)

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
@login_required
def home():
    """Show meeting time"""

    # Get id of current user session
    user_id = session["user_id"]

    # Get current session user
    user = User.query.filter_by(id=user_id).first()

    time_slot = Meeting.query.filter_by(username=user.username).first()
    exists = bool(time_slot)
    if exists:
        return render_template("home.html", start_time=time_slot.start_time, end_time=time_slot.end_time, exists=exists)
    else:
        return render_template("home.html", exists=exists)


@app.route("/add_meeting", methods=["GET", "POST"])
@login_required
def add_meeting():
    """Add meeting time slot"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure start time was submitted
        if not request.form.get("starttime"):
            return apology("must provide start time", 403)

        # Ensure end time was submitted
        elif not request.form.get("endtime"):
            return apology("must provide end time", 403)

        # Store start and end times inputed
        start_time = request.form.get("starttime")
        end_time = request.form.get("endtime")

        # Check if end time is less than or equal to start time
        if int(start_time[:-3]) >= int(end_time[:-3]):
            if int(start_time[-2:]) >= int(end_time[-2:]):
                return apology("end time should be greater than start time", 403)

        # Get id of current user session
        user_id = session["user_id"]

        # Get current session user
        user = User.query.filter_by(id=user_id).first()

        # Check is user had previously set a time slot
        if not bool(Meeting.query.filter_by(username=user.username).first()):
            new_meeting = Meeting(username=user.username, start_time=start_time, end_time=end_time)

        else:
            new_meeting = Meeting.query.filter_by(username=user.username).first()
            new_meeting.start_time = start_time
            new_meeting.end_time = end_time

        db.session.add(new_meeting)
        db.session.commit()

        return redirect("/home")

    else:
        return render_template("meeting.html")


@app.route("/scheduler", methods=["GET", "POST"])
@login_required
def scheduler():
    """Get common time for meeting"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Get current session user name
        curr_username = User.query.filter_by(id=session["user_id"]).first()

        # Get user name inputed
        other_username = request.form.get("username")

        curr_meeting = Meeting.query.filter_by(username=curr_username.username).first()
        other_meeting = Meeting.query.filter_by(username=other_username).first()

        # Check if user exists
        if not bool(User.query.filter_by(username=other_username).first()):
            return apology("user does not exist", 403)

        # Check is current user has set a time slot
        if not bool(curr_meeting):
            return apology("must set time slot", 403)

        # Check if given user has set a time slot
        if not bool(other_meeting):
            return apology("other user must set time slot", 403)

        if common_time_slot(curr_meeting.start_time, curr_meeting.end_time, other_meeting.start_time,
                            other_meeting.end_time) is None:
            return render_template("scheduler.html", msg="No common time slot exists!")

        start, end = common_time_slot(curr_meeting.start_time, curr_meeting.end_time, other_meeting.start_time,
                                      other_meeting.end_time)

        return render_template("scheduler.html", post=True, start=start, end=end)
    else:
        return render_template("scheduler.html", post=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = User.query.filter_by(username=request.form.get("username")).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.password, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        db.session.add(user)
        db.session.commit()

        # Add user to current session
        session["user_id"] = user.id

        # Set logged in to true
        session['logged_in'] = True

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Set logged in to false
    session['logged_in'] = False

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Store the user inputs
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password", 403)

        # Ensure passwords match
        elif password != confirmation:
            return apology("passwords should match", 403)

        # Query database for username
        rows = User.query.filter_by(username=username).all()

        # If username already exists, return apology
        if len(rows) != 0:
            return apology("username already exists", 403)

        # Add user to database
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Add user to current session
        session["user_id"] = user.id

        # Set logged in to true
        session['logged_in'] = True

        # Redirect user to home page
        return redirect("/home")
    else:
        return render_template("register.html")


@app.errorhandler(404)
def page_not_found(e):
    """Apologize for 404 error"""
    return apology("not found", 404)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    start_time = db.Column(db.String(5))
    end_time = db.Column(db.String(5))

    def __int__(self, username, start_time, end_time):
        self.username = username
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<Meeting of %r>' % self.username
