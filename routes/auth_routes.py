
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from utils.db_connect import get_db_connection

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# USER REGISTRATION
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "Username, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 8 characters"
        }), 400

    password_hash = generate_password_hash(password)

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO users
                (username, email, password_hash, full_name)
                VALUES (%s, %s, %s, %s)
                RETURNING user_id, username, email, full_name;
            """, (username, email, password_hash, full_name))

            user = cursor.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful",
            "user": {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "full_name": user[3]
            }
        }), 201

    except Exception as e:

        if conn:
            conn.rollback()

        if getattr(e, "pgcode", None) == "23505":
            return jsonify({
                "success": False,
                "message": "Email already registered"
            }), 409

        return jsonify({
            "success": False,
            "message": "Registration failed"
        }), 500

    finally:
        if conn:
            conn.close()


# USER LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT user_id, username, email,
                       password_hash, full_name
                FROM users
                WHERE email = %s AND is_active = TRUE;
            """, (email,))

            user = cursor.fetchone()

        if not user or not check_password_hash(user[3], password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        access_token = create_access_token(
            identity=str(user[0])
        )

        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "full_name": user[4]
            }
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Login failed"
        }), 500

    finally:
        if conn:
            conn.close()
