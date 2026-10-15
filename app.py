from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection

app = Flask(__name__)


# ==================== DASHBOARD ====================

@app.route("/")
def home():

    connection = get_db_connection()
    cursor = connection.cursor()

    tables = {
        "Students": "Student",
        "Courses": "Course",
        "Faculty": "Faculty",
        "Batches": "Batch",
        "Enrollments": "Enrollment",
        "Laboratories": "Laboratory",
        "Lab Allocations": "Lab_Allocation",
        "Examinations": "Examination",
        "Results": "Result",
        "Certificates": "Certificate"
    }

    counts = {}

    for name, table in tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[name] = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template("index.html", counts=counts)


# ==================== STUDENTS ====================

@app.route("/students")
def students():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT Student_ID, Student_Name, Email, Phone, DOB
        FROM Student
        ORDER BY Student_ID
    """)

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", students=students)


@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form["student_name"]
    email = request.form["email"]
    phone = request.form["phone"]
    dob = request.form["dob"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Student_ID), 0) + 1 FROM Student"
    )

    student_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Student
        (Student_ID, Student_Name, Email, Phone, DOB)
        VALUES (%s, %s, %s, %s, %s)
    """, (student_id, name, email, phone, dob))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("students"))


# ==================== COURSES ====================

@app.route("/courses")
def courses():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT Course_ID, Course_Name, Duration, Fees
        FROM Course
        ORDER BY Course_ID
    """)

    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("courses.html", courses=courses)


@app.route("/add_course", methods=["POST"])
def add_course():

    course_name = request.form["course_name"]
    duration = request.form["duration"]
    fees = request.form["fees"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Course_ID), 100) + 1 FROM Course"
    )

    course_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Course
        (Course_ID, Course_Name, Duration, Fees)
        VALUES (%s, %s, %s, %s)
    """, (course_id, course_name, duration, fees))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("courses"))


# ==================== FACULTY ====================

@app.route("/faculty")
def faculty():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT Faculty_ID, Faculty_Name, Email, Specialization
        FROM Faculty
        ORDER BY Faculty_ID
    """)

    faculty = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("faculty.html", faculty=faculty)


@app.route("/add_faculty", methods=["POST"])
def add_faculty():

    name = request.form["faculty_name"]
    email = request.form["email"]
    specialization = request.form["specialization"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Faculty_ID), 200) + 1 FROM Faculty"
    )

    faculty_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Faculty
        (Faculty_ID, Faculty_Name, Email, Specialization)
        VALUES (%s, %s, %s, %s)
    """, (faculty_id, name, email, specialization))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("faculty"))


# ==================== BATCHES ====================

@app.route("/batches")
def batches():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get batches with course and faculty names
    cursor.execute("""
        SELECT
            b.Batch_ID,
            c.Course_Name,
            f.Faculty_Name,
            b.Start_Date,
            b.End_Date,
            b.Timing
        FROM Batch b
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        JOIN Faculty f
            ON b.Faculty_ID = f.Faculty_ID
        ORDER BY b.Batch_ID
    """)

    batches = cursor.fetchall()

    # Get courses for dropdown
    cursor.execute("""
        SELECT Course_ID, Course_Name
        FROM Course
        ORDER BY Course_Name
    """)

    courses = cursor.fetchall()

    # Get faculty for dropdown
    cursor.execute("""
        SELECT Faculty_ID, Faculty_Name
        FROM Faculty
        ORDER BY Faculty_Name
    """)

    faculty = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "batches.html",
        batches=batches,
        courses=courses,
        faculty=faculty
    )


@app.route("/add_batch", methods=["POST"])
def add_batch():

    course_id = request.form["course_id"]
    faculty_id = request.form["faculty_id"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    timing = request.form["timing"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Batch_ID), 300) + 1 FROM Batch"
    )

    batch_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Batch
        (Batch_ID, Course_ID, Faculty_ID, Start_Date, End_Date, Timing)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        batch_id,
        course_id,
        faculty_id,
        start_date,
        end_date,
        timing
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("batches"))

# ==================== ENROLLMENTS ====================

@app.route("/enrollments")
def enrollments():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Get existing enrollments
    cursor.execute("""
        SELECT
            e.Enrollment_ID,
            s.Student_Name,
            c.Course_Name,
            b.Batch_ID,
            e.Enrollment_Date
        FROM Enrollment e
        JOIN Student s
            ON e.Student_ID = s.Student_ID
        JOIN Batch b
            ON e.Batch_ID = b.Batch_ID
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        ORDER BY e.Enrollment_ID
    """)

    enrollments = cursor.fetchall()

    # Students for dropdown
    cursor.execute("""
        SELECT Student_ID, Student_Name
        FROM Student
        ORDER BY Student_Name
    """)

    students = cursor.fetchall()

    # Batches for dropdown
    cursor.execute("""
        SELECT
            b.Batch_ID,
            c.Course_Name,
            f.Faculty_Name
        FROM Batch b
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        JOIN Faculty f
            ON b.Faculty_ID = f.Faculty_ID
        ORDER BY b.Batch_ID
    """)

    batches = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "enrollments.html",
        enrollments=enrollments,
        students=students,
        batches=batches
    )


@app.route("/add_enrollment", methods=["POST"])
def add_enrollment():

    student_id = request.form["student_id"]
    batch_id = request.form["batch_id"]
    enrollment_date = request.form["enrollment_date"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Enrollment_ID), 0) + 1 FROM Enrollment"
    )

    enrollment_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Enrollment
        (
            Enrollment_ID,
            Student_ID,
            Batch_ID,
            Enrollment_Date
        )
        VALUES (%s, %s, %s, %s)
    """, (
        enrollment_id,
        student_id,
        batch_id,
        enrollment_date
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("enrollments"))

# ==================== LABORATORIES ====================

@app.route("/laboratories")
def laboratories():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT Lab_ID, Lab_Name, Capacity, Location
        FROM Laboratory
        ORDER BY Lab_ID
    """)

    laboratories = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "laboratories.html",
        laboratories=laboratories
    )


@app.route("/add_laboratory", methods=["POST"])
def add_laboratory():

    lab_name = request.form["lab_name"]
    capacity = request.form["capacity"]
    location = request.form["location"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Lab_ID), 500) + 1 FROM Laboratory"
    )

    lab_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Laboratory
        (Lab_ID, Lab_Name, Capacity, Location)
        VALUES (%s, %s, %s, %s)
    """, (
        lab_id,
        lab_name,
        capacity,
        location
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("laboratories"))

# ==================== LAB ALLOCATION ====================

@app.route("/lab_allocations")
def lab_allocations():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Existing allocations
    cursor.execute("""
        SELECT
            la.Allocation_ID,
            la.Batch_ID,
            c.Course_Name,
            l.Lab_Name,
            la.Allocation_Date,
            la.Start_Time,
            la.End_Time
        FROM Lab_Allocation la
        JOIN Batch b
            ON la.Batch_ID = b.Batch_ID
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        JOIN Laboratory l
            ON la.Lab_ID = l.Lab_ID
        ORDER BY la.Allocation_ID
    """)

    allocations = cursor.fetchall()

    # Batches for dropdown
    cursor.execute("""
        SELECT
            b.Batch_ID,
            c.Course_Name
        FROM Batch b
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        ORDER BY b.Batch_ID
    """)

    batches = cursor.fetchall()

    # Laboratories for dropdown
    cursor.execute("""
        SELECT Lab_ID, Lab_Name
        FROM Laboratory
        ORDER BY Lab_ID
    """)

    laboratories = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "lab_allocations.html",
        allocations=allocations,
        batches=batches,
        laboratories=laboratories
    )


@app.route("/add_lab_allocation", methods=["POST"])
def add_lab_allocation():

    batch_id = request.form["batch_id"]
    lab_id = request.form["lab_id"]
    allocation_date = request.form["allocation_date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Allocation_ID), 0) + 1 FROM Lab_Allocation"
    )

    allocation_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Lab_Allocation
        (
            Allocation_ID,
            Batch_ID,
            Lab_ID,
            Allocation_Date,
            Start_Time,
            End_Time
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        allocation_id,
        batch_id,
        lab_id,
        allocation_date,
        start_time,
        end_time
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("lab_allocations"))

# ==================== EXAMINATIONS ====================

@app.route("/examinations")
def examinations():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Existing examinations
    cursor.execute("""
        SELECT
            e.Exam_ID,
            e.Batch_ID,
            c.Course_Name,
            e.Exam_Date,
            e.Exam_Type,
            e.Total_Marks
        FROM Examination e
        JOIN Batch b
            ON e.Batch_ID = b.Batch_ID
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        ORDER BY e.Exam_ID
    """)

    examinations = cursor.fetchall()

    # Batches for dropdown
    cursor.execute("""
        SELECT
            b.Batch_ID,
            c.Course_Name
        FROM Batch b
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        ORDER BY b.Batch_ID
    """)

    batches = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "examinations.html",
        examinations=examinations,
        batches=batches
    )


@app.route("/add_examination", methods=["POST"])
def add_examination():

    batch_id = request.form["batch_id"]
    exam_date = request.form["exam_date"]
    exam_type = request.form["exam_type"]
    total_marks = request.form["total_marks"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COALESCE(MAX(Exam_ID), 0) + 1 FROM Examination"
    )

    exam_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Examination
        (
            Exam_ID,
            Batch_ID,
            Exam_Date,
            Exam_Type,
            Total_Marks
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        exam_id,
        batch_id,
        exam_date,
        exam_type,
        total_marks
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("examinations"))

# ==================== RESULTS ====================

@app.route("/results")
def results():

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Existing results
    cursor.execute("""
        SELECT
            r.Result_ID,
            s.Student_Name,
            e.Exam_ID,
            c.Course_Name,
            r.Marks,
            r.Status
        FROM Result r
        JOIN Student s
            ON r.Student_ID = s.Student_ID
        JOIN Examination e
            ON r.Exam_ID = e.Exam_ID
        JOIN Batch b
            ON e.Batch_ID = b.Batch_ID
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        ORDER BY r.Result_ID
    """)

    results = cursor.fetchall()

    # Students for dropdown
    cursor.execute("""
        SELECT Student_ID, Student_Name
        FROM Student
        ORDER BY Student_Name
    """)

    students = cursor.fetchall()

    # Examinations for dropdown
    cursor.execute("""
        SELECT
            e.Exam_ID,
            c.Course_Name,
            e.Exam_Type
        FROM Examination e
        JOIN Batch b
            ON e.Batch_ID = b.Batch_ID
        JOIN Course c
            ON b.Course_ID = c.Course_ID
        ORDER BY e.Exam_ID
    """)

    examinations = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "results.html",
        results=results,
        students=students,
        examinations=examinations
    )


@app.route("/add_result", methods=["POST"])
def add_result():

    student_id = request.form["student_id"]
    exam_id = request.form["exam_id"]
    marks = float(request.form["marks"])

    # Pass mark = 40%
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Total_Marks
        FROM Examination
        WHERE Exam_ID = %s
    """, (exam_id,))

    total_marks = cursor.fetchone()[0]

    pass_mark = total_marks * 0.40

    if marks >= pass_mark:
        status = "Pass"
    else:
        status = "Fail"

    cursor.execute(
        "SELECT COALESCE(MAX(Result_ID), 0) + 1 FROM Result"
    )

    result_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Result
        (
            Result_ID,
            Exam_ID,
            Student_ID,
            Marks,
            Status
        )
        VALUES (%s, %s, %s, %s, %s)
    """, (
        result_id,
        exam_id,
        student_id,
        marks,
        status
    ))

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("results"))


# ==================== CERTIFICATES ====================

@app.route("/certificates")
def certificates():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            cert.Certificate_ID,
            cert.Certificate_No,
            s.Student_Name,
            c.Course_Name,
            cert.Issue_Date
        FROM Certificate cert
        JOIN Student s ON cert.Student_ID = s.Student_ID
        JOIN Course c ON cert.Course_ID = c.Course_ID
        ORDER BY cert.Certificate_ID
    """)
    certificates = cursor.fetchall()

    cursor.execute("SELECT Student_ID, Student_Name FROM Student ORDER BY Student_Name")
    students = cursor.fetchall()

    cursor.execute("SELECT Course_ID, Course_Name FROM Course ORDER BY Course_Name")
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "certificates.html",
        certificates=certificates,
        students=students,
        courses=courses
    )


@app.route("/add_certificate", methods=["POST"])
def add_certificate():
    student_id = request.form["student_id"]
    course_id = request.form["course_id"]
    issue_date = request.form["issue_date"]
    certificate_no = request.form["certificate_no"].strip()

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COALESCE(MAX(Certificate_ID), 0) + 1 FROM Certificate")
    certificate_id = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Certificate
            (Certificate_ID, Student_ID, Course_ID, Issue_Date, Certificate_No)
        VALUES (%s, %s, %s, %s, %s)
    """, (certificate_id, student_id, course_id, issue_date, certificate_no))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for("certificates"))



# ==================== RUN ====================

if __name__ == "__main__":
    app.run(debug=True)