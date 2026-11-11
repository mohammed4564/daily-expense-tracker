
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db_connect import get_db_connection
from datetime import date
from decimal import Decimal, InvalidOperation

expense_bp = Blueprint(
    "expense",
    __name__,
    url_prefix="/api/expenses"
)


def validate_expense(data):

    expense_date = data.get("expense_date")
    category = data.get("category")
    description = data.get("description", "")

    try:
        amount = Decimal(str(data.get("amount")))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError("Valid amount is required")

    if not expense_date or not category:
        raise ValueError("Expense date and category are required")

    try:
        date.fromisoformat(expense_date)
    except (ValueError, TypeError):
        raise ValueError("Date must be in YYYY-MM-DD format")

    if not amount.is_finite() or amount <= 0:
        raise ValueError("Amount must be greater than zero")

    if amount.as_tuple().exponent < -2:
        raise ValueError("Amount cannot have more than 2 decimal places")

    if len(category) > 100 or len(description) > 250:
        raise ValueError("Category or description is too long")

    return expense_date, category, description, amount


def expense_to_dict(row):

    return {
        "expense_id": row[0],
        "expense_date": row[1].isoformat(),
        "category": row[2],
        "description": row[3],
        "amount": str(row[4])
    }


# 1. CREATE EXPENSE
@expense_bp.route("", methods=["POST"])
@jwt_required()
def create_expense():

    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}

    try:
        expense_date, category, description, amount = (
            validate_expense(data)
        )
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                INSERT INTO expenses
                (user_id, expense_date, category, description, amount)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING expense_id, expense_date,
                          category, description, amount;
            """, (
                user_id,
                expense_date,
                category,
                description,
                amount
            ))

            expense = expense_to_dict(cursor.fetchone())

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Expense created successfully",
            "expense": expense
        }), 201

    except Exception:
        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to create expense"
        }), 500

    finally:
        if conn:
            conn.close()


# 2. GET ALL EXPENSES
@expense_bp.route("", methods=["GET"])
@jwt_required()
def get_expenses():

    user_id = int(get_jwt_identity())

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT expense_id, expense_date,
                       category, description, amount
                FROM expenses
                WHERE user_id = %s
                ORDER BY expense_date DESC, expense_id DESC;
            """, (user_id,))

            rows = cursor.fetchall()

        expenses = [expense_to_dict(row) for row in rows]

        return jsonify({
            "success": True,
            "total_records": len(expenses),
            "expenses": expenses
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Unable to fetch expenses"
        }), 500

    finally:
        if conn:
            conn.close()


# 3. GET EXPENSE BY ID
@expense_bp.route("/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):

    user_id = int(get_jwt_identity())

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                SELECT expense_id, expense_date,
                       category, description, amount
                FROM expenses
                WHERE expense_id = %s
                  AND user_id = %s;
            """, (expense_id, user_id))

            row = cursor.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Expense not found"
            }), 404

        return jsonify({
            "success": True,
            "expense": expense_to_dict(row)
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "message": "Unable to fetch expense"
        }), 500

    finally:
        if conn:
            conn.close()


# 4. UPDATE EXPENSE
@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):

    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}

    try:
        expense_date, category, description, amount = (
            validate_expense(data)
        )
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                UPDATE expenses
                SET expense_date = %s,
                    category = %s,
                    description = %s,
                    amount = %s
                WHERE expense_id = %s
                  AND user_id = %s
                RETURNING expense_id, expense_date,
                          category, description, amount;
            """, (
                expense_date,
                category,
                description,
                amount,
                expense_id,
                user_id
            ))

            row = cursor.fetchone()

        if not row:
            conn.rollback()

            return jsonify({
                "success": False,
                "message": "Expense not found"
            }), 404

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Expense updated successfully",
            "expense": expense_to_dict(row)
        }), 200

    except Exception:
        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to update expense"
        }), 500

    finally:
        if conn:
            conn.close()


# 5. DELETE EXPENSE
@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):

    user_id = int(get_jwt_identity())

    conn = None

    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:

            cursor.execute("""
                DELETE FROM expenses
                WHERE expense_id = %s
                  AND user_id = %s
                RETURNING expense_id;
            """, (expense_id, user_id))

            deleted = cursor.fetchone()

        if not deleted:
            conn.rollback()

            return jsonify({
                "success": False,
                "message": "Expense not found"
            }), 404

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Expense deleted successfully"
        }), 200

    except Exception:
        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": "Unable to delete expense"
        }), 500

    finally:
        if conn:
            conn.close()
