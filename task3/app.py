from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Demo users
users = {
    "employee": {
        "password": "emp123",
        "role": "Employee"
    },
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    }
}

# Demo tokens
tokens = {}

# Employee records
employees = [
    {"id": 1, "name": "Ali", "department": "IT"},
    {"id": 2, "name": "Sara", "department": "HR"}
]

# LOGIN API
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:

        token = username + "_token"

        tokens[token] = users[username]["role"]

        return jsonify({
            "message": "Login successful",
            "token": token,
            "role": users[username]["role"]
        }), 200

    return jsonify({"message": "Invalid username or password"}), 401


# AUTHENTICATION
def authentication(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token or token not in tokens:
            return jsonify({"message": "Authentication required"}), 401

        return f(*args, **kwargs)

    return decorated


# AUTHORIZATION
def admin_only(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if tokens.get(token) != "Administrator":
            return jsonify({"message": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated


# VIEW EMPLOYEES (Employee + Admin)
@app.route('/employees', methods=['GET'])
@authentication
def view_employees():

    return jsonify(employees), 200


# ADD EMPLOYEE (Admin only)
@app.route('/employees', methods=['POST'])
@authentication
@admin_only
def add_employee():

    data = request.get_json()

    new_employee = {
        "id": max([e["id"] for e in employees], default=0) + 1,
        "name": data["name"],
        "department": data["department"]
    }

    employees.append(new_employee)

    return jsonify({
        "message": "Employee added successfully",
        "employee": new_employee
    }), 201


# UPDATE EMPLOYEE (Admin only)
@app.route('/employees/<int:id>', methods=['PUT'])
@authentication
@admin_only
def update_employee(id):

    data = request.get_json()

    for employee in employees:

        if employee["id"] == id:

            employee["name"] = data["name"]
            employee["department"] = data["department"]

            return jsonify({
                "message": "Employee updated successfully",
                "employee": employee
            }), 200

    return jsonify({"message": "Employee not found"}), 404


# DELETE EMPLOYEE (Admin only)
@app.route('/employees/<int:id>', methods=['DELETE'])
@authentication
@admin_only
def delete_employee(id):

    for employee in employees:

        if employee["id"] == id:

            employees.remove(employee)

            return jsonify({
                "message": "Employee deleted successfully"
            }), 200

    return jsonify({"message": "Employee not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
