import database, fingerprint, lcd
from student import Student
from time import sleep
fingerprint.sensor_intialization()
while True:
    print("\nWelcome  to my fingerprint attendance Program")
    print("\nMenu:")
    print("1. Enroll a new Student to the Database.")
    print("2. Remove Student.")
    print("3. Mark Attendance.")
    print("4. Send Report to the bot")
    print("5. see report")
    print("0. Exit ")
    choice=int(input("Enter your choice :"))
    match (choice):
        case 1:
            roll_no=int(input("Enter your Roll no :"))
            name=input("Enter your Name :")
            
            fingerprint_id=fingerprint.enroll_fingerprint()
            stu1=Student(fingerprint_id, roll_no, name)
            database.insert_student(stu1)
        case 2:
            removed_stu=database.get_stu_by_fingerid(fingerprint.get_fingerid())
            database.remove_student(removed_stu)
            print(f"{removed_stu[2]} is Removed.")
            lcd.display_message(removed_stu[2], "Removed")
            sleep(2)
        case 3:
            present_stu_id=fingerprint.mark_attendance_by_fingerprint()
            # pass the present student id to the attedance report program
        case 4:
            pass
            # build telegram bot to send report of the attendance sheet
        case 5:
            report=database.get_students()
            print(report)
        case 0:
            print("Exiting Program")
            lcd.display_message("Exiting","Program....")
        case _:
            print("Invalid Choice!!!")




 