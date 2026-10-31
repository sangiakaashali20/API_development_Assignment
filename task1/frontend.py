
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Student Management System")
st.title("Student Management System")
st.write("Manage student records using our Flask API.")

def get_students():
    try:
        response = requests.get(f"{API_URL}/students")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        st.error("Cannot connect to API. Please run app.py first.")
        return []

# View students
st.header("All Students")

if st.button("Refresh Students"):
    st.rerun()

students = get_students()

if students:
    st.dataframe(pd.DataFrame(students), use_container_width=True)
else:
    st.info("No students found. Add a student below.")

# Add student
st.header("Add Student")

with st.form("add_student_form"):
    name = st.text_input("Student Name")
    department = st.text_input("Department")
    email = st.text_input("Email")
    add_button = st.form_submit_button("Add Student")

    if add_button:
        if name.strip() and department.strip() and email.strip():
            try:
                response = requests.post(
                    f"{API_URL}/students",
                    json={
                        "name": name,
                        "department": department,
                        "email": email
                    }
                )
                if response.status_code == 201:
                    st.success("Student added successfully!")
                    st.rerun()
                else:
                    st.error(response.json().get("error", "Could not add student"))
            except requests.RequestException:
                st.error("Could not connect to the API.")
        else:
            st.warning("Please fill in all fields.")

# Update student
st.header("Update Student")

with st.form("update_student_form"):
    update_id = st.number_input(
        "Student ID to Update", min_value=1, step=1
    )
    update_name = st.text_input("New Student Name")
    update_department = st.text_input("New Department")
    update_email = st.text_input("New Email")
    update_button = st.form_submit_button("Update Student")

    if update_button:
        if update_name.strip() and update_department.strip() and update_email.strip():
            try:
                response = requests.put(
                    f"{API_URL}/students/{int(update_id)}",
                    json={
                        "name": update_name,
                        "department": update_department,
                        "email": update_email
                    }
                )
                if response.status_code == 200:
                    st.success("Student updated successfully!")
                    st.rerun()
                else:
                    st.error(response.json().get("error", "Could not update student"))
            except requests.RequestException:
                st.error("Could not connect to the API.")
        else:
            st.warning("Please fill in all fields.")

# Delete student
st.header("Delete Student")

with st.form("delete_student_form"):
    delete_id = st.number_input(
        "Student ID to Delete", min_value=1, step=1, key="delete_id"
    )
    delete_button = st.form_submit_button("Delete Student")

    if delete_button:
        try:
            response = requests.delete(
                f"{API_URL}/students/{int(delete_id)}"
            )
            if response.status_code == 200:
                st.success("Student deleted successfully!")
                st.rerun()
            else:
                st.error(response.json().get("error", "Could not delete student"))
        except requests.RequestException:
            st.error("Could not connect to the API.")
