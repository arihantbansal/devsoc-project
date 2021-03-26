from functools import wraps
from flask import redirect, render_template, session


def common_time_slot(first_start, first_end, second_start, second_end):
    first_start = int(first_start.split(":")[0]) * 100 + int(first_start.split(":")[1])
    first_end = int(first_end.split(":")[0]) * 100 + int(first_end.split(":")[1])
    second_start = int(second_start.split(":")[0]) * 100 + int(second_start.split(":")[1])
    second_end = int(second_end.split(":")[0]) * 100 + int(second_end.split(":")[1])

    if first_end < second_start or second_end < first_start:
        return None

    start = max(first_start, second_start)
    end = min(first_end, second_end)
    common_start = str(start)[:-2] + ":" + str(start)[-2:]
    common_end = str(end)[:-2] + ":" + str(end)[-2:]

    return common_start, common_end


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

