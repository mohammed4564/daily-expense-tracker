from flask import Blueprint, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from utils.db_connect import get_db_connection


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# Current Terms & Conditions version
TERMS_VERSION = "1.0"


# ==========================================
# USER REGISTRATION
# ==========================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")
    terms_accepted = data.get("terms_accepted", False)

    # Validate Terms & Conditions
    if terms_accepted is not True:
        return jsonify({
            "success": False,
            "message": "You must accept the Terms & Conditions."
        }), 400

    # Validate required fields
    if not isinstance(username, str) or not username.strip():
        return jsonify({
            "success": False,
            "message": "Username is required"
        }), 400

    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "success": False,
            "message": "Email is required"
        }), 400

    if not isinstance(password, str) or not password:
        return jsonify({
            "success": False,
            "message": "Password is required"
        }), 400

    username = username.strip()
    email = email.strip()

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
                INSERT INTO public.users
                (
                    username,
                    email,
                    password_hash,
                    full_name,
                    terms_accepted,
                    terms_accepted_at,
                    terms_version
                )
                VALUES (
                    %s, %s, %s, %s,
                    TRUE,
                    CURRENT_TIMESTAMP,
                    %s
                )
                RETURNING
                    user_id,
                    username,
                    email,
                    full_name,
                    terms_accepted,
                    terms_accepted_at,
                    terms_version;
            """, (
                username,
                email,
                password_hash,
                full_name,
                TERMS_VERSION
            ))

            user = cursor.fetchone()

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful",
            "user": {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "full_name": user[3],
                "terms_accepted": user[4],
                "terms_accepted_at": user[5].isoformat(),
                "terms_version": user[6]
            }
        }), 201

    except Exception as e:

        if conn:
            conn.rollback()

        if getattr(e, "pgcode", None) == "23505":
            return jsonify({
                "success": False,
                "message": "Username or email already registered"
            }), 409

        print("Registration Error:", str(e))

        return jsonify({
            "success": False,
            "message": "Registration failed"
        }), 500

    finally:

        if conn:
            conn.close()


# ==========================================
# USER LOGIN
# ==========================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    if not email.strip() or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    conn = None

    try:

        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT
                    user_id,
                    username,
                    email,
                    password_hash,
                    full_name
                FROM public.users
                WHERE email = %s
                AND is_active = TRUE;
            """, (email.strip(),))

            user = cursor.fetchone()

        if not user or not check_password_hash(user[3], password):
            return jsonify({
                "success": False,
                "message": "Invalid email or password"
            }), 401

        # Generate Access Token
        access_token = create_access_token(
            identity=str(user[0])
        )

        # Generate Refresh Token
        refresh_token = create_refresh_token(
            identity=str(user[0])
        )

        return jsonify({
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "user_id": user[0],
                "username": user[1],
                "email": user[2],
                "full_name": user[4]
            }
        }), 200

    except Exception as e:

        print("Login Error:", str(e))

        return jsonify({
            "success": False,
            "message": "Login failed"
        }), 500

    finally:

        if conn:
            conn.close()


# ==========================================
# CHANGE PASSWORD
# ==========================================

@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():

    data = request.get_json(silent=True) or {}

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    # Validate input
    if not isinstance(current_password, str) or not isinstance(new_password, str):
        return jsonify({
            "success": False,
            "message": "Current password and new password are required"
        }), 400

    if not current_password or not new_password:
        return jsonify({
            "success": False,
            "message": "Current password and new password are required"
        }), 400

    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "New password must contain at least 8 characters"
        }), 400

    if current_password == new_password:
        return jsonify({
            "success": False,
            "message": "New password must be different from current password"
        }), 400

    user_id = get_jwt_identity()

    conn = None

    try:

        conn = get_db_connection()

        with conn.cursor() as cursor:

            # Get existing password hash
            cursor.execute("""
                SELECT password_hash
                FROM public.users
                WHERE user_id = %s
                AND is_active = TRUE;
            """, (user_id,))

            user = cursor.fetchone()

            if not user:
                return jsonify({
                    "success": False,
                    "message": "User account not found or inactive"
                }), 404

            # Verify current password
            if not check_password_hash(user[0], current_password):
                return jsonify({
                    "success": False,
                    "message": "Current password is incorrect"
                }), 400

            # Generate new password hash
            new_password_hash = generate_password_hash(new_password)

            # Update password
            cursor.execute("""
                UPDATE public.users
                SET password_hash = %s
                WHERE user_id = %s;
            """, (new_password_hash, user_id))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Password changed successfully. Please log in again."
        }), 200

    except Exception as e:

        if conn:
            conn.rollback()

        print("Change Password Error:", str(e))

        return jsonify({
            "success": False,
            "message": "Unable to change password"
        }), 500

    finally:

        if conn:
            conn.close()


# ==========================================
# REFRESH ACCESS TOKEN
# ==========================================

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    conn = None

    try:

        conn = get_db_connection()

        with conn.cursor() as cursor:

            # Verify account status
            cursor.execute("""
                SELECT user_id
                FROM public.users
                WHERE user_id = %s
                AND is_active = TRUE;
            """, (user_id,))

            user = cursor.fetchone()

        if not user:
            return jsonify({
                "success": False,
                "message": "User account not found or inactive"
            }), 401

        # Generate new access token
        new_access_token = create_access_token(
            identity=str(user_id)
        )

        return jsonify({
            "success": True,
            "message": "Access token refreshed successfully",
            "access_token": new_access_token
        }), 200

    except Exception as e:

        print("Refresh Token Error:", str(e))

        return jsonify({
            "success": False,
            "message": "Unable to refresh access token"
        }), 500

    finally:

        if conn:
            conn.close()
