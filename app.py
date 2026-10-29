from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rafic@2004",
    database="student_management"
)
print("MySQL connected successfully!")

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        if name == "" or email == "" or phone == "" or course == "":
            return render_template("add_student.html", error="Please fill the required information")
        if len(phone) != 10 or not phone.isdigit():
            return render_template("add_student.html", error="Please give a valid mobile number")
        
        cursor = db.cursor()
        sql = "INSERT INTO students (name, email, phone, course) VALUES (%s, %s, %s, %s)"

        values = (name, email, phone, course)

        cursor.execute(sql, values)

        db.commit()

        
        print(name)    
        print(email)
        print(phone)
        print(course)
    return render_template("add_student.html", success="Student added successfully!")
@app.route("/view-students")
def view_students():
    search = request.args.get("search")

    cursor = db.cursor()

    if search:
        sql = "SELECT * FROM students WHERE name LIKE %s"
        values = ("%" + search + "%",)
        cursor.execute(sql, values)
    else:
        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    return render_template("view_students.html", students=students)

@app.route("/edit-student/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    cursor = db.cursor()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        course = request.form["course"]
        if name == "" or email == "" or phone == "" or course == "":
            return render_template("edit_student.html", error="Please fill the required information")
        if len(phone) != 10 or not phone.isdigit():
            return render_template("edit_student.html", error="Please give a valid mobile number")

        sql = """
        UPDATE students
        SET name = %s, email = %s, phone = %s, course = %s
        WHERE student_id = %s
        """

        values = (name, email, phone, course, student_id)

        cursor.execute(sql, values)

        db.commit()

    cursor.execute(
        "SELECT * FROM students WHERE student_id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    return render_template("edit_student.html", student=student)
@app.route("/delete-student/<int:student_id>")
def delete_student(student_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id = %s",
        (student_id,)
    )

    db.commit()

    return "Student deleted successfully!"

if __name__ == "__main__":
    app.run(debug=True)