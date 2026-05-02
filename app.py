from flask import Flask, render_template, request, redirect, url_for, session
from database.db import get_db, init_db, seed_db, create_user, validate_user, get_user_by_id
from database.queries import get_user_by_id as get_user_details, get_summary_stats, get_recent_transactions, get_category_breakdown

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'


# Initialize database on startup
with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    user = None
    if session.get('user_id'):
        user = get_user_by_id(session['user_id'])
    return render_template("landing.html", user=user)


@app.route("/register")
def register():
    # Redirect already logged-in users away from register page
    if session.get('user_id'):
        return redirect(url_for('landing'))
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_post():
    """
    Handles registration form submission
    Validates email, password, and confirm password, creates user, sets session, redirects to landing
    """
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    name = request.form.get('name', '').strip()
    
    # Validate confirm password matches
    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match")
    
    try:
        user_id = create_user(email, password, name)
        session['user_id'] = user_id
        return redirect(url_for('landing'))
    except ValueError as e:
        return render_template("register.html", error=str(e))


@app.route("/login")
def login():
    # Redirect already logged-in users away from login page
    if session.get('user_id'):
        return redirect(url_for('landing'))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """
    Handles login form submission
    Validates email and password, sets session, redirects to landing
    """
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    user_id = validate_user(email, password)
    
    if user_id:
        session['user_id'] = user_id
        return redirect(url_for('landing'))
    else:
        return render_template("login.html", error="Invalid email or password")


@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")

# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout", methods=["POST"])
def logout():
    """
    Handles logout — clears session and redirects to landing page
    """
    session.clear()
    return redirect(url_for('landing'))


@app.route("/profile")
def profile():
    """
    Displays user profile page with dynamic data from database.
    Only accessible to authenticated users.
    """
    # Authentication guard
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    # Get date filters from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Fetch dynamic data from database
    user = get_user_details(user_id)
    if not user:
        return redirect(url_for('login'))
    
    # Add initials
    user['initials'] = ''.join(word[0].upper() for word in user['name'].split())
    
    # Fetch stats with optional filters
    stats = get_summary_stats(user_id, start_date=start_date, end_date=end_date)
    # Format total_spent with ₹ symbol
    if stats['total_spent'] > 0:
        stats['total_spent'] = f"₹{stats['total_spent']:.2f}"
    else:
        stats['total_spent'] = "₹0.00"
    
    # Fetch transactions and format amounts with optional filters
    transactions = get_recent_transactions(user_id, limit=10, start_date=start_date, end_date=end_date)
    for txn in transactions:
        txn['amount'] = f"₹{txn['amount']:.2f}"
    
    # Fetch category breakdown with optional filters
    categories = get_category_breakdown(user_id, start_date=start_date, end_date=end_date)
    
    context = {
        'user': user,
        'stats': stats,
        'transactions': transactions,
        'categories': categories,
        'start_date': start_date,
        'end_date': end_date
    }
    
    return render_template('profile.html', **context)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
