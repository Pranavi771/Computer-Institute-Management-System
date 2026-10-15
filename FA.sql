CREATE DATABASE ComputerInstituteDB;
USE ComputerInstituteDB;

CREATE TABLE Student (
    Student_ID INT PRIMARY KEY,
    Student_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Phone VARCHAR(15),
    DOB DATE
);

CREATE TABLE Course (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(100) NOT NULL,
    Duration VARCHAR(50),
    Fees DECIMAL(10,2)
);

CREATE TABLE Faculty (
    Faculty_ID INT PRIMARY KEY,
    Faculty_Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    Specialization VARCHAR(100)
);

CREATE TABLE Batch (
    Batch_ID INT PRIMARY KEY,
    Course_ID INT,
    Faculty_ID INT,
    Start_Date DATE,
    End_Date DATE,
    Timing VARCHAR(50),

    FOREIGN KEY (Course_ID)
        REFERENCES Course(Course_ID),

    FOREIGN KEY (Faculty_ID)
        REFERENCES Faculty(Faculty_ID)
);

CREATE TABLE Enrollment (
    Enrollment_ID INT PRIMARY KEY,
    Student_ID INT,
    Batch_ID INT,
    Enrollment_Date DATE,

    FOREIGN KEY (Student_ID)
        REFERENCES Student(Student_ID),

    FOREIGN KEY (Batch_ID)
        REFERENCES Batch(Batch_ID)
);

CREATE TABLE Laboratory (
    Lab_ID INT PRIMARY KEY,
    Lab_Name VARCHAR(100) NOT NULL,
    Capacity INT,
    Location VARCHAR(100)
);

CREATE TABLE Lab_Allocation (
    Allocation_ID INT PRIMARY KEY,
    Batch_ID INT,
    Lab_ID INT,
    Allocation_Date DATE,
    Start_Time TIME,
    End_Time TIME,

    FOREIGN KEY (Batch_ID)
        REFERENCES Batch(Batch_ID),

    FOREIGN KEY (Lab_ID)
        REFERENCES Laboratory(Lab_ID)
);

CREATE TABLE Examination (
    Exam_ID INT PRIMARY KEY,
    Batch_ID INT,
    Exam_Date DATE,
    Exam_Type VARCHAR(50),
    Total_Marks INT,

    FOREIGN KEY (Batch_ID)
        REFERENCES Batch(Batch_ID)
);


CREATE TABLE Result (
    Result_ID INT PRIMARY KEY,
    Exam_ID INT,
    Student_ID INT,
    Marks INT,
    Status VARCHAR(20),

    FOREIGN KEY (Exam_ID)
        REFERENCES Examination(Exam_ID),

    FOREIGN KEY (Student_ID)
        REFERENCES Student(Student_ID)
);


CREATE TABLE Certificate (
    Certificate_ID INT PRIMARY KEY,
    Student_ID INT,
    Course_ID INT,
    Issue_Date DATE,
    Certificate_No VARCHAR(50) UNIQUE,

    FOREIGN KEY (Student_ID)
        REFERENCES Student(Student_ID),

    FOREIGN KEY (Course_ID)
        REFERENCES Course(Course_ID)
);

INSERT INTO Student VALUES
(1, 'Aarav Sharma', 'aarav@gmail.com', '9876543210', '2005-04-12'),
(2, 'Pranavi Joshi', 'pranavi@gmail.com', '9876543211', '2005-08-20'),
(3, 'Riya Patil', 'riya@gmail.com', '9876543212', '2004-12-15'),
(4, 'Aditya Kulkarni', 'aditya@gmail.com', '9876543213', '2005-02-10'),
(5, 'Sneha Deshmukh', 'sneha@gmail.com', '9876543214', '2005-06-25'),
(6, 'Rahul Mehta', 'rahul@gmail.com', '9876543215', '2004-11-08'),
(7, 'Ananya Shah', 'ananya@gmail.com', '9876543216', '2005-09-14'),
(8, 'Om Jadhav', 'om@gmail.com', '9876543217', '2005-01-18');

INSERT INTO Course VALUES
(101, 'Python Programming', '3 Months', 15000),
(102, 'Computer Networking', '4 Months', 18000),
(103, 'Cybersecurity', '4 Months', 22000),
(104, 'Database Management', '3 Months', 16000);

INSERT INTO Faculty VALUES
(201, 'Rahul Sharma', 'rahul.faculty@gmail.com', 'Python'),
(202, 'Priya Patil', 'priya.faculty@gmail.com', 'Networking'),
(203, 'Amit Desai', 'amit.faculty@gmail.com', 'Cybersecurity'),
(204, 'Neha Kulkarni', 'neha.faculty@gmail.com', 'Database Systems');

INSERT INTO Batch VALUES
(301, 101, 201, '2026-07-01', '2026-09-30', '10:00 AM - 12:00 PM'),
(302, 102, 202, '2026-07-15', '2026-11-15', '01:00 PM - 03:00 PM'),
(303, 103, 203, '2026-08-01', '2026-11-30', '10:00 AM - 12:00 PM'),
(304, 104, 204, '2026-08-15', '2026-11-15', '03:00 PM - 05:00 PM');

INSERT INTO Enrollment VALUES
(401, 1, 301, '2026-06-25'),
(402, 2, 301, '2026-06-26'),
(403, 3, 302, '2026-07-05'),
(404, 4, 303, '2026-07-20'),
(405, 5, 304, '2026-08-05'),
(406, 6, 303, '2026-07-25'),
(407, 7, 304, '2026-08-06'),
(408, 8, 302, '2026-07-08');

INSERT INTO Laboratory VALUES
(501, 'Programming Lab', 30, 'Block A - 101'),
(502, 'Networking Lab', 25, 'Block A - 102'),
(503, 'Cybersecurity Lab', 25, 'Block B - 201'),
(504, 'Database Lab', 30, 'Block B - 202');

INSERT INTO Lab_Allocation VALUES
(601, 301, 501, '2026-07-10', '10:00:00', '12:00:00'),
(602, 302, 502, '2026-07-20', '01:00:00', '03:00:00'),
(603, 303, 503, '2026-08-10', '10:00:00', '12:00:00'),
(604, 304, 504, '2026-08-20', '03:00:00', '05:00:00');

INSERT INTO Examination VALUES
(701, 301, '2026-09-25', 'Final', 100),
(702, 302, '2026-11-10', 'Final', 100),
(703, 303, '2026-11-20', 'Final', 100),
(704, 304, '2026-11-10', 'Final', 100);

INSERT INTO Result VALUES
(801, 701, 1, 85, 'Pass'),
(802, 701, 2, 91, 'Pass'),
(803, 702, 3, 78, 'Pass'),
(804, 703, 4, 88, 'Pass'),
(805, 704, 5, 72, 'Pass'),
(806, 703, 6, 65, 'Pass'),
(807, 704, 7, 54, 'Pass'),
(808, 702, 8, 39, 'Fail');

INSERT INTO Certificate VALUES
(901, 1, 101, '2026-10-01', 'CERT-PY-001'),
(902, 2, 101, '2026-10-01', 'CERT-PY-002'),
(903, 3, 102, '2026-11-15', 'CERT-NW-001'),
(904, 4, 103, '2026-11-30', 'CERT-CS-001'),
(905, 5, 104, '2026-11-15', 'CERT-DB-001');



