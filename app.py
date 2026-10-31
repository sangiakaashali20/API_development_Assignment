
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "Student API is working!"})


@app.route("/students", methods=["GET"])
def get_students():
    conn = connect_db()
    rows = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    department = data.get("department", "").strip()
    email = data.get("email", "").strip()

    if not all([name, department, email]):
        return jsonify({"error": "All fields are required"}), 400

    conn = connect_db()

    try:
        cursor = conn.execute(
            "INSERT INTO students (name, department, email) VALUES (?, ?, ?)",
            (name, department, email)
        )
        conn.commit()

        return jsonify({
            "message": "Student added successfully",
            "id": cursor.lastrowid
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    finally:
        conn.close()


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = connect_db()

    row = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(row))


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    department = data.get("department", "").strip()
    email = data.get("email", "").strip()

    if not all([name, department, email]):
        return jsonify({"error": "All fields are required"}), 400

    conn = connect_db()

    try:
        cursor = conn.execute(
            """UPDATE students
               SET name = ?, department = ?, email = ?
               WHERE id = ?""",
            (name, department, email, student_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Student not found"}), 404

        return jsonify({"message": "Student updated successfully"})

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 409

    finally:
        conn.close()


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = connect_db()

    cursor = conn.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
