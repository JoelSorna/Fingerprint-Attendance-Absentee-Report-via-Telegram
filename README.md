# Fingerprint Attendance & Absentee Report via Telegram

A Raspberry Pi-based **Fingerprint Attendance System** that uses a fingerprint sensor to identify students, mark their attendance, store student information in an SQLite database, and send attendance/absentee reports through Telegram.

## 📌 Project Overview

This project automates the process of taking student attendance using a fingerprint sensor.

Instead of manually calling names or maintaining a paper attendance sheet, students can place their finger on the fingerprint sensor. The system identifies the registered fingerprint and marks the corresponding student as **Present**.

The project is designed using a modular Python structure so that different functionalities such as fingerprint processing, database operations, LCD display, attendance management, and Telegram reporting can be maintained separately.

## ✨ Features

* 🔐 Fingerprint-based student identification
* 👨‍🎓 Register new students
* 🗑️ Remove registered students
* ✅ Mark attendance using fingerprints
* 🗄️ Store student data using SQLite
* 📺 Display system messages on a 16×2 LCD
* 📱 Send attendance/absentee reports through Telegram
* 🧩 Modular Python code structure
* 🍓 Designed to run on Raspberry Pi

## 🛠️ Technologies Used

* **Python**
* **Raspberry Pi**
* **PyFingerprint**
* **SQLite**
* **RPLCD**
* **RPi.GPIO**
* **Telegram Bot API** *(reporting module)*

## 🔧 Hardware Requirements

* Raspberry Pi
* Optical Fingerprint Sensor
* 16×2 LCD Display
* USB connection for fingerprint sensor
* Jumper wires
* Breadboard
* Power supply for Raspberry Pi

## 💻 Software Requirements

Install Python libraries required by the project:

```bash
pip install pyfingerprint
pip install RPLCD
```

The project also uses Raspberry Pi GPIO libraries.

> Note: Some Raspberry Pi GPIO packages may already be installed depending on the Raspberry Pi OS version.

## 📁 Project Structure

```text
Fingerprint_Attendance/
│
├── main.py
├── database.py
├── fingerprint.py
├── student.py
├── lcd.py
├── attendance.py
├── telegram_bot.py
├── .gitignore
└── students.db
```

### File Description

| File              | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| `main.py`         | Main program and menu                                  |
| `student.py`      | Contains the `Student` class                           |
| `database.py`     | SQLite database operations                             |
| `fingerprint.py`  | Fingerprint sensor operations                          |
| `lcd.py`          | LCD initialization and display functions               |
| `attendance.py`   | Attendance recording and report generation             |
| `telegram_bot.py` | Sends attendance reports through Telegram              |
| `.gitignore`      | Prevents unnecessary/private files from being uploaded |
| `students.db`     | Local SQLite database                                  |

## 🔄 How the System Works

```text
                ┌──────────────────┐
                │      main.py     │
                │  Main Controller │
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │fingerprint │  │  database  │  │    lcd     │
   │    .py     │  │    .py     │  │    .py     │
   └─────┬──────┘  └─────┬──────┘  └────────────┘
         │               │
         ▼               ▼
   Fingerprint        SQLite
     Sensor          Database
         │
         ▼
   Student Identified
         │
         ▼
   Attendance Recorded
         │
         ▼
   ┌─────────────────┐
   │ telegram_bot.py │
   └────────┬────────┘
            │
            ▼
       Telegram Report
```

## 📝 Student Registration

When registering a new student:

1. Enter the student's roll number.
2. Enter the student's name.
3. Place the student's finger on the fingerprint sensor.
4. The fingerprint is converted into a template.
5. The system checks whether the fingerprint already exists.
6. If it is new, the fingerprint is stored in the sensor.
7. The fingerprint ID, roll number, and name are stored in SQLite.

Example:

```text
Roll No: 25
Name: John

Fingerprint ID: 3
```

The database stores the relationship between the fingerprint ID and the student.

## ✅ Attendance Process

When a student wants to mark attendance:

1. The student places their finger on the sensor.
2. The sensor searches for a matching fingerprint.
3. The system obtains the fingerprint ID.
4. The fingerprint ID is matched with the SQLite database.
5. The student's name is retrieved.
6. Attendance is recorded.
7. The LCD displays the student's attendance status.

Example:

```text
Fingerprint
Detected

John
Present
```

## 📱 Telegram Reporting

The Telegram module will be used to send attendance reports.

The system can generate a report containing information such as:

```text
Attendance Report

Present:
25 - John
31 - David
42 - Sarah

Absent:
12 - Alex
18 - Michael
```

The report can then be sent automatically to a configured Telegram bot.

## 🗄️ Database

The project uses **SQLite** because it is lightweight and does not require a separate database server.

A student record contains information such as:

```text
Fingerprint ID
Roll Number
Name
```

Attendance records can later contain:

```text
Fingerprint ID
Date
Time
Attendance Status
```

## 🔒 Security

Sensitive information such as the Telegram Bot Token should **not** be directly written into the source code or uploaded to GitHub.

Use environment variables or a `.env` file instead.

Example `.env`:

```text
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

The `.env` file should be included in `.gitignore`.

## ▶️ Running the Project

Clone the repository:

```bash
git clone https://github.com/JoelSorna/Fingerprint-Attendance-Absentee-Report-via-Telegram.git
```

Move into the project directory:

```bash
cd Fingerprint-Attendance-Absentee-Report-via-Telegram
```

Run the main program:

```bash
python3 main.py
```

The system will display the main menu:

```text
Welcome to my Fingerprint Attendance Program

Menu:
1. Enroll a new Student to the Database
2. Remove Student
3. Mark Attendance
4. Send Report to the Bot
0. Exit
```

## 🚧 Project Status

The project is being developed incrementally.

### Completed

* [x] Fingerprint sensor initialization
* [x] Fingerprint enrollment
* [x] Fingerprint matching
* [x] Student database
* [x] Student registration
* [x] Student removal
* [x] LCD display
* [x] Modular Python structure

### In Progress

* [ ] Attendance database
* [ ] Daily attendance report
* [ ] Absentee identification
* [ ] Telegram bot integration
* [ ] Automated Telegram report

## 🎯 Future Improvements

Possible future improvements include:

* Automatic daily attendance reports
* Automatic absentee reports
* Telegram commands for checking attendance
* Admin authentication
* Attendance history
* Monthly attendance reports
* Web-based attendance dashboard
* Export attendance to CSV/Excel
* Multiple class/section support

## 👨‍💻 Author

**Joel Sorna**

BSc Information Technology

## 📄 License

This project is developed for educational and academic purposes.

