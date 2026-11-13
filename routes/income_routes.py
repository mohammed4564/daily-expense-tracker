
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db_connect import get_db_connection

income_bp = Blueprint("income", __name__, url_prefix="/api/income")


# CREATE INCOME
@income_bp.route("", methods=["POST"])
@jwt_required()
def add_income():
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        income_date = data.get("income_date")
        category = data.get("category")
        description = data.get("description")
        amount = data.get("amount")

        if not income_date or not category or amount is None:
            return jsonify({
                "success": False,
                "message": "Income date, category and amount are required"
            }), 400

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "message": "Amount must be greater than zero"
            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO public.income
            (user_id, income_date, category, description, amount)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING income_id, user_id, income_date,
                      category, description, amount, created_date
        """, (user_id, income_date, category, description, amount))

        row = cur.fetchone()
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Income added successfully",
            "data": {
                "income_id": row[0],
                "user_id": row[1],
                "income_date": str(row[2]),
                "category": row[3],
                "description": row[4],
                "amount": float(row[5]),
                "created_date": str(row[6])
            }
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# READ ALL INCOME
@income_bp.route("", methods=["GET"])
@jwt_required()
def get_all_income():
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT income_id, income_date, category,
                   description, amount, created_date
            FROM public.income
            WHERE user_id = %s
            ORDER BY income_date DESC
        """, (user_id,))

        rows = cur.fetchall()

        income_list = [{
            "income_id": row[0],
            "income_date": str(row[1]),
            "category": row[2],
            "description": row[3],
            "amount": float(row[4]),
            "created_date": str(row[5])
        } for row in rows]

        return jsonify({
            "success": True,
            "count": len(income_list),
            "data": income_list
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# READ INCOME BY ID
@income_bp.route("/<int:income_id>", methods=["GET"])
@jwt_required()
def get_income(income_id):
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT income_id, income_date, category,
                   description, amount, created_date
            FROM public.income
            WHERE income_id = %s AND user_id = %s
        """, (income_id, user_id))

        row = cur.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Income record not found"
            }), 404

        return jsonify({
            "success": True,
            "data": {
                "income_id": row[0],
                "income_date": str(row[1]),
                "category": row[2],
                "description": row[3],
                "amount": float(row[4]),
                "created_date": str(row[5])
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# UPDATE INCOME
@income_bp.route("/<int:income_id>", methods=["PUT"])
@jwt_required()
def update_income(income_id):
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        allowed_fields = [
            "income_date", "category", "description", "amount"
        ]

        updates = {
            field: data[field]
            for field in allowed_fields if field in data
        }

        if not updates:
            return jsonify({
                "success": False,
                "message": "No fields provided for update"
            }), 400

        if "category" in updates and (
            not isinstance(updates["category"], str)
            or not updates["category"].strip()
        ):
            return jsonify({
                "success": False,
                "message": "Category cannot be empty"
            }), 400

        if "amount" in updates:
            try:
                updates["amount"] = float(updates["amount"])
                if updates["amount"] <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "message": "Amount must be greater than zero"
                }), 400

        set_clause = ", ".join(
            f"{field} = %s" for field in updates
        )

        values = list(updates.values())
        values.extend([income_id, user_id])

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"""
            UPDATE public.income
            SET {set_clause}
            WHERE income_id = %s AND user_id = %s
            RETURNING income_id, income_date, category,
                      description, amount, created_date
        """, values)

        row = cur.fetchone()

        if not row:
            conn.rollback()
            return jsonify({
                "success": False,
                "message": "Income record not found"
            }), 404

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Income updated successfully",
            "data": {
                "income_id": row[0],
                "income_date": str(row[1]),
                "category": row[2],
                "description": row[3],
                "amount": float(row[4]),
                "created_date": str(row[5])
            }
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# DELETE INCOME
@income_bp.route("/<int:income_id>", methods=["DELETE"])
@jwt_required()
def delete_income(income_id):
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM public.income
            WHERE income_id = %s AND user_id = %s
            RETURNING income_id
        """, (income_id, user_id))

        row = cur.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Income record not found"
            }), 404

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Income deleted successfully"
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
