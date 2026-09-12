import database
import fingerprint
import lcd
from student import Student
from attendance import (
    initialize_attendance_system, 
    mark_student_present,
    get_todays_attendance,
    send_attendance_report,
    send_daily_reminder,
    clear_todays_attendance,
    export_attendance_csv,
    generate_attendance_report,
    generate_summary_report
)
from time import sleep

# Initialize the fingerprint sensor
fingerprint.sensor_initialization()

# Initialize attendance system
initialize_attendance_system()

def display_menu():
    """Display main menu"""
    print("\n" + "="*60)
    print("Welcome to Fingerprint Attendance System")
    print("="*60)
    print("\nMenu:")
    print("1.  Enroll a new Student to the Database")
    print("2.  Remove Student")
    print("3.  Mark Attendance")
    print("4.  Send Attendance Report to Telegram")
    print("5.  View Today's Attendance")
    print("6.  View All Students")
    print("7.  Clear Today's Attendance (Reset)")
    print("8.  Export Attendance to CSV")
    print("9.  Send Daily Reminder to Telegram")
    print("10. View Live Attendance List")
    print("0.  Exit")
    print("="*60)


def enroll_student():
    """Enroll a new student"""
    print("\n--- Enroll New Student ---")
    try:
        roll_no = int(input("Enter Roll Number: "))
        name = input("Enter Name: ")
        
        fingerprint_id = fingerprint.enroll_fingerprint()
        stu1 = Student(fingerprint_id, roll_no, name)
        database.insert_student(stu1)
        print(f"✓ Student {name} enrolled successfully!")
        lcd.display_message(name, "Enrolled!")
        sleep(2)
    except ValueError:
        print("✗ Invalid input!")
        lcd.display_message("Invalid", "Input")
        sleep(2)


def remove_student():
    """Remove a student"""
    print("\n--- Remove Student ---")
    try:
        removed_stu_data = fingerprint.get_fingerid()
        removed_stu = database.get_stu_by_fingerid(removed_stu_data)
        if removed_stu:
            database.remove_student(removed_stu)
            print(f"✓ {removed_stu[2]} has been removed.")
            lcd.display_message(removed_stu[2], "Removed")
            sleep(2)
        else:
            print("✗ Student not found!")
    except Exception as e:
        print(f"✗ Error: {e}")


def mark_attendance():
    """Mark attendance by fingerprint"""
    print("\n--- Mark Attendance ---")
    try:
        present_stu_id = fingerprint.mark_attendance_by_fingerprint()
        student = database.get_stu_by_fingerid(present_stu_id)
        
        if student:
            fingerprint_id, roll_no, name = student[0], student[1], student[2]
            
            # Mark in attendance database
            if mark_student_present(fingerprint_id, roll_no, name):
                print(f"✓ {name} marked present!")
                lcd.display_message(name, "Present ✓")
            else:
                print(f"⚠ {name} already marked today")
                lcd.display_message(name, "Already Done")
            sleep(2)
    except Exception as e:
        print(f"✗ Error: {e}")


def view_todays_attendance():
    """View today's attendance"""
    print("\n--- Today's Attendance ---")
    records = get_todays_attendance()
    
    if records:
        print("\nAttendance Records:")
        print("-" * 70)
        print(f"{'Roll No':<10} {'Name':<20} {'Time':<15} {'Status':<15}")
        print("-" * 70)
        for record in records:
            fingerprint_id, roll_no, name, date, time, status = record[1:]
            print(f"{roll_no:<10} {name:<20} {time:<15} {status:<15}")
        print("-" * 70)
        print(f"Total Present: {len(records)}")
    else:
        print("No attendance records for today yet!")


def view_all_students():
    """View all enrolled students"""
    print("\n--- All Enrolled Students ---")
    report = database.get_students()
    
    if report:
        print("\nStudent List:")
        print("-" * 60)
        print(f"{'Fingerprint ID':<15} {'Roll No':<10} {'Name':<35}")
        print("-" * 60)
        for student in report:
            fingerprint_id, roll_no, name = student[0], student[1], student[2]
            print(f"{fingerprint_id:<15} {roll_no:<10} {name:<35}")
        print("-" * 60)
        print(f"Total Students: {len(report)}")
    else:
        print("No students enrolled yet!")


def send_report():
    """Send attendance report to Telegram"""
    print("\n--- Send Attendance Report ---")
    print("1. Detailed Report (with all names)")
    print("2. Summary Report (statistics only)")
    
    try:
        choice = int(input("Choose report type (1-2): "))
        
        if choice == 1:
            print("Sending detailed report...")
            send_attendance_report(detailed=True)
        elif choice == 2:
            print("Sending summary report...")
            send_attendance_report(detailed=False)
        else:
            print("✗ Invalid choice!")
            
    except ValueError:
        print("✗ Invalid input!")


def reset_attendance():
    """Clear today's attendance"""
    print("\n--- Clear Today's Attendance ---")
    print("⚠ WARNING: This will delete all attendance records for today!")
    
    confirm = input("Are you sure? (yes/no): ").lower()
    
    if confirm == "yes":
        if clear_todays_attendance():
            print("✓ Today's attendance cleared!")
            lcd.display_message("Attendance", "Cleared")
            sleep(2)
    else:
        print("✗ Operation cancelled")


def export_csv():
    """Export attendance to CSV"""
    print("\n--- Export Attendance to CSV ---")
    
    filename = export_attendance_csv()
    
    if filename:
        print(f"✓ Exported to {filename}")
        lcd.display_message("Exported", "to CSV")
        sleep(2)
    else:
        print("✗ Export failed")


def send_reminder():
    """Send daily reminder"""
    print("\n--- Send Daily Reminder ---")
    print("Sending reminder to Telegram...")
    
    if send_daily_reminder():
        print("✓ Reminder sent!")
        lcd.display_message("Reminder", "Sent")
    else:
        print("✗ Failed to send reminder")
    
    sleep(2)


def view_live_list():
    """View live attendance list"""
    print("\n--- Live Attendance List ---")
    summary = generate_attendance_report()
    print(summary.replace("<b>", "").replace("</b>", "").replace("<br>", "\n"))


# ==================== MAIN LOOP ====================

def main():
    """Main program loop"""
    while True:
        try:
            display_menu()
            
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                enroll_student()
                
            elif choice == 2:
                remove_student()
                
            elif choice == 3:
                mark_attendance()
                
            elif choice == 4:
                send_report()
                
            elif choice == 5:
                view_todays_attendance()
                
            elif choice == 6:
                view_all_students()
                
            elif choice == 7:
                reset_attendance()
                
            elif choice == 8:
                export_csv()
                
            elif choice == 9:
                send_reminder()
                
            elif choice == 10:
                view_live_list()
                
            elif choice == 0:
                print("\nExiting Program...")
                lcd.display_message("Exiting", "Program")
                sleep(2)
                database.close_connection()
                lcd.clear()
                break
                
            else:
                print("✗ Invalid Choice! Please try again.")
                lcd.display_message("Invalid", "Choice")
                sleep(2)
                
        except ValueError:
            print("✗ Invalid input! Please enter a number.")
            lcd.display_message("Invalid", "Input")
            sleep(2)
        except KeyboardInterrupt:
            print("\n\nProgram interrupted!")
            database.close_connection()
            lcd.clear()
            break
        except Exception as e:
            print(f"✗ An error occurred: {e}")
            lcd.display_message("Error", "Occurred")
            sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated!")
        database.close_connection()
        lcd.clear()
