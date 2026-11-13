
import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask import render_template
from routes.auth_routes import auth_bp
from routes.expense_routes import expense_bp
from routes.income_routes import income_bp
from routes.borrow_lend_routes import borrow_lend_bp

load_dotenv()



app = Flask(__name__)


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")


@app.route("/add-expense")
def add_expense_page():
    return render_template("add_expense.html")

@app.route("/edit-expense/<int:expense_id>")
def edit_expense_page(expense_id):
    return render_template(
        "edit_expense.html",
        expense_id=expense_id
    )

@app.route("/reports")
def reports_page():
    return render_template("reports.html")


@app.route("/income")
def income_page():
    return render_template("income.html")


@app.route("/borrow-lend")
def borrow_lend_page():
    return render_template("borrow_lend.html")

@app.route("/")
def home():
     return render_template("home.html")

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

if not app.config["JWT_SECRET_KEY"]:
    raise RuntimeError("JWT_SECRET_KEY is missing in .env")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

from datetime import timedelta


app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

# Register API blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(expense_bp)
app.register_blueprint(income_bp)
app.register_blueprint(borrow_lend_bp)

# =================================
# API HEALTH CHECK
# =================================

@app.route("/health")
def health_check():
    return jsonify({
        "success": True,
        "message": "Daily Expense Tracker API is running"
    })


@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "message": "API endpoint not found"
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(debug=True)
