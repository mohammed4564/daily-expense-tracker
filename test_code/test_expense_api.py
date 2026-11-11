
import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:5000"

# Test user details
USER_DATA = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "Test@12345",
    "full_name": "Test User"
}

# Expense details
EXPENSE_DATA = {
    "expense_date": date.today().isoformat(),
    "category": "Food",
    "description": "Test breakfast",
    "amount": 150
}

TOKEN = None
EXPENSE_ID = None


def print_response(title, response):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("Status Code:", response.status_code)

    try:
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print(response.text)


def test_register():

    url = f"{BASE_URL}/api/auth/register"

    response = requests.post(
        url,
        json=USER_DATA,
        timeout=10
    )

    print_response("USER REGISTRATION", response)

    return response.status_code in (200, 201, 409)


def test_login():

    global TOKEN

    url = f"{BASE_URL}/api/auth/login"

    response = requests.post(
        url,
        json={
            "email": USER_DATA["email"],
            "password": USER_DATA["password"]
        },
        timeout=10
    )

    print_response("USER LOGIN", response)

    if response.status_code == 200:
        TOKEN = response.json().get("access_token")
        return bool(TOKEN)

    return False


def get_headers():

    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }


def test_create_expense():

    global EXPENSE_ID

    url = f"{BASE_URL}/api/expenses"

    response = requests.post(
        url,
        json=EXPENSE_DATA,
        headers=get_headers(),
        timeout=10
    )

    print_response("CREATE EXPENSE", response)

    if response.status_code == 201:
        EXPENSE_ID = response.json()["expense"]["expense_id"]
        return True

    return False


def test_get_expenses():

    url = f"{BASE_URL}/api/expenses"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=10
    )

    print_response("GET ALL EXPENSES", response)

    return response.status_code == 200


def test_get_expense_by_id():

    url = f"{BASE_URL}/api/expenses/{EXPENSE_ID}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=10
    )

    print_response("GET EXPENSE BY ID", response)

    return response.status_code == 200


def test_update_expense():

    url = f"{BASE_URL}/api/expenses/{EXPENSE_ID}"

    updated_data = {
        "expense_date": date.today().isoformat(),
        "category": "Food",
        "description": "Updated lunch expense",
        "amount": 250
    }

    response = requests.put(
        url,
        json=updated_data,
        headers=get_headers(),
        timeout=10
    )

    print_response("UPDATE EXPENSE", response)

    return response.status_code == 200


def test_delete_expense():

    url = f"{BASE_URL}/api/expenses/{EXPENSE_ID}"

    response = requests.delete(
        url,
        headers=get_headers(),
        timeout=10
    )

    print_response("DELETE EXPENSE", response)

    return response.status_code == 200


def run_all_tests():

    results = {}

    print("\nDAILY EXPENSE TRACKER API TESTING STARTED")

    try:
        results["Register"] = test_register()

        if not results["Register"]:
            print("\nRegistration failed. Stopping tests.")
            return

        results["Login"] = test_login()

        if not results["Login"]:
            print("\nLogin failed. Stopping tests.")
            return

        results["Create Expense"] = test_create_expense()

        if not results["Create Expense"]:
            print("\nExpense creation failed. Stopping tests.")
            return

        results["Get All Expenses"] = test_get_expenses()

        results["Get Expense By ID"] = test_get_expense_by_id()

        results["Update Expense"] = test_update_expense()

        results["Delete Expense"] = test_delete_expense()

    except requests.RequestException as e:
        print("\nAPI connection error:", e)

    finally:

        print("\n" + "=" * 60)
        print("API TEST SUMMARY")
        print("=" * 60)

        for test_name, status in results.items():

            result = "PASSED" if status else "FAILED"

            print(f"{test_name}: {result}")


if __name__ == "__main__":
    run_all_tests()
