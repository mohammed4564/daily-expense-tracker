
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.db_connect import get_db_connection

borrow_lend_bp = Blueprint(
    "borrow_lend",
    __name__,
    url_prefix="/api/borrow-lend"
)


def format_record(row):
    return {
        "transaction_id": row[0],
        "transaction_type": row[1],
        "person_name": row[2],
        "amount": float(row[3]),
        "transaction_date": str(row[4]),
        "due_date": str(row[5]) if row[5] else None,
        "description": row[6],
        "status": row[7],
        "created_date": str(row[8])
    }


# CREATE BORROW / LEND
@borrow_lend_bp.route("", methods=["POST"])
@jwt_required()
def add_borrow_lend():
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        transaction_type = data.get("transaction_type")
        person_name = data.get("person_name")
        amount = data.get("amount")
        transaction_date = data.get("transaction_date")
        due_date = data.get("due_date")
        description = data.get("description")

        if not all([
            transaction_type,
            person_name,
            amount is not None,
            transaction_date
        ]):
            return jsonify({
                "success": False,
                "message": "Transaction type, person name, amount and transaction date are required"
            }), 400

        transaction_type = transaction_type.upper()

        if transaction_type not in ["BORROWED", "LENT"]:
            return jsonify({
                "success": False,
                "message": "Transaction type must be BORROWED or LENT"
            }), 400

        if not isinstance(person_name, str) or not person_name.strip():
            return jsonify({
                "success": False,
                "message": "Person name cannot be empty"
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
            INSERT INTO public.borrow_lend
            (
                user_id,
                transaction_type,
                person_name,
                amount,
                transaction_date,
                due_date,
                description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING transaction_id, transaction_type,
                      person_name, amount, transaction_date,
                      due_date, description, status, created_date
        """, (
            user_id,
            transaction_type,
            person_name.strip(),
            amount,
            transaction_date,
            due_date,
            description
        ))

        row = cur.fetchone()
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Borrow/Lend record added successfully",
            "data": format_record(row)
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# READ ALL BORROW / LEND
@borrow_lend_bp.route("", methods=["GET"])
@jwt_required()
def get_all_borrow_lend():
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT transaction_id, transaction_type,
                   person_name, amount, transaction_date,
                   due_date, description, status, created_date
            FROM public.borrow_lend
            WHERE user_id = %s
            ORDER BY transaction_date DESC
        """, (user_id,))

        rows = cur.fetchall()

        records = [format_record(row) for row in rows]

        return jsonify({
            "success": True,
            "count": len(records),
            "data": records
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# READ BORROW / LEND BY ID
@borrow_lend_bp.route("/<int:transaction_id>", methods=["GET"])
@jwt_required()
def get_borrow_lend(transaction_id):
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT transaction_id, transaction_type,
                   person_name, amount, transaction_date,
                   due_date, description, status, created_date
            FROM public.borrow_lend
            WHERE transaction_id = %s AND user_id = %s
        """, (transaction_id, user_id))

        row = cur.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Borrow/Lend record not found"
            }), 404

        return jsonify({
            "success": True,
            "data": format_record(row)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# UPDATE BORROW / LEND
@borrow_lend_bp.route("/<int:transaction_id>", methods=["PUT"])
@jwt_required()
def update_borrow_lend(transaction_id):
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        allowed_fields = [
            "transaction_type",
            "person_name",
            "amount",
            "transaction_date",
            "due_date",
            "description",
            "status"
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

        if "transaction_type" in updates:
            updates["transaction_type"] = str(
                updates["transaction_type"]
            ).upper()

            if updates["transaction_type"] not in ["BORROWED", "LENT"]:
                return jsonify({
                    "success": False,
                    "message": "Invalid transaction type"
                }), 400

        if "status" in updates:
            updates["status"] = str(updates["status"]).upper()

            if updates["status"] not in [
                "ACTIVE", "COMPLETED", "CANCELLED"
            ]:
                return jsonify({
                    "success": False,
                    "message": "Invalid status"
                }), 400

        if "person_name" in updates:
            if (
                not isinstance(updates["person_name"], str)
                or not updates["person_name"].strip()
            ):
                return jsonify({
                    "success": False,
                    "message": "Person name cannot be empty"
                }), 400

            updates["person_name"] = updates["person_name"].strip()

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
        values.extend([transaction_id, user_id])

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"""
            UPDATE public.borrow_lend
            SET {set_clause}
            WHERE transaction_id = %s AND user_id = %s
            RETURNING transaction_id, transaction_type,
                      person_name, amount, transaction_date,
                      due_date, description, status, created_date
        """, values)

        row = cur.fetchone()

        if not row:
            conn.rollback()
            return jsonify({
                "success": False,
                "message": "Borrow/Lend record not found"
            }), 404

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Borrow/Lend record updated successfully",
            "data": format_record(row)
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# DELETE BORROW / LEND
@borrow_lend_bp.route("/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_borrow_lend(transaction_id):
    conn = None
    cur = None

    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM public.borrow_lend
            WHERE transaction_id = %s AND user_id = %s
            RETURNING transaction_id
        """, (transaction_id, user_id))

        row = cur.fetchone()

        if not row:
            return jsonify({
                "success": False,
                "message": "Borrow/Lend record not found"
            }), 404

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Borrow/Lend record deleted successfully"
        }), 200

    except Exception as e:
        if conn:
            conn.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
