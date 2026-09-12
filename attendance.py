import sqlite3
import requests
from datetime import datetime, date
from telegram_config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DEBUG_MODE

def create_attendance_table():
    """Create attendance table if it doesn't exist"""
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        c.execute("""CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fingerprint_id INTEGER NOT NULL,
                    roll_no INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'present',
                    UNIQUE(fingerprint_id, date)
                )""")
        
        conn.commit()
        conn.close()
        print("✓ Attendance table created/verified")
        return True
    except Exception as e:
        print(f"✗ Error creating attendance table: {e}")
        return False


def mark_student_present(fingerprint_id, roll_no, name):
    """Mark a student as present in attendance"""
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        today = str(date.today())
        current_time = datetime.now().strftime("%H:%M:%S")
        
        c.execute("SELECT * FROM attendance WHERE fingerprint_id=? AND date=?",
                  (fingerprint_id, today))
        
        if c.fetchone():
            print(f"✓ {name} already marked present today")
            conn.close()
            return False
        c.execute("""INSERT INTO attendance 
                    (fingerprint_id, roll_no, name, date, time, status)
                    VALUES (?, ?, ?, ?, ?, 'present')""",
                  (fingerprint_id, roll_no, name, today, current_time))
        
        conn.commit()
        conn.close()
        print(f"✓ {name} marked present at {current_time}")
        return True
        
    except Exception as e:
        print(f"✗ Error marking attendance: {e}")
        return False


def get_todays_attendance():
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        today = str(date.today())
        c.execute("SELECT * FROM attendance WHERE date=? ORDER BY time",
                  (today,))
        
        records = c.fetchall()
        conn.close()
        return records
    except Exception as e:
        print(f"✗ Error fetching attendance: {e}")
        return []


def get_all_students():
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM students ORDER BY roll_no")
        students = c.fetchall()
        conn.close()
        return students
    except Exception as e:
        print(f"✗ Error fetching students: {e}")
        return []


def get_attendance_summary(date_str=None):
    if date_str is None:
        date_str = str(date.today())
    
    try:
        all_students = get_all_students()
        if not all_students:
            return {"total": 0, "present": 0, "absent": 0, "present_students": [], "absent_students": []}
        
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        c.execute("SELECT fingerprint_id FROM attendance WHERE date=?", (date_str,))
        present_ids = [row[0] for row in c.fetchall()]
        conn.close()
        
        total = len(all_students)
        present = len(present_ids)
        absent = total - present
        
        present_students = []
        absent_students = []
        
        for student in all_students:
            fingerprint_id, roll_no, name = student[0], student[1], student[2]
            if fingerprint_id in present_ids:
                present_students.append((roll_no, name))
            else:
                absent_students.append((roll_no, name))
        
        return {
            "total": total,
            "present": present,
            "absent": absent,
            "present_students": sorted(present_students),
            "absent_students": sorted(absent_students),
            "date": date_str
        }
    except Exception as e:
        print(f"✗ Error generating summary: {e}")
        return {"total": 0, "present": 0, "absent": 0, "present_students": [], "absent_students": []}



def send_telegram_message(message_text):
    if not TELEGRAM_BOT_TOKEN:
        print("✗ Telegram bot token not configured!")
        print("  → Edit telegram_config.py and add your bot token")
        return False
    
    if not TELEGRAM_CHAT_ID:
        print("✗ Telegram chat ID not configured!")
        print("  → Edit telegram_config.py and add your chat ID")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            if DEBUG_MODE:
                print("✓ Message sent to Telegram successfully")
            return True
        else:
            print(f"✗ Telegram API Error: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("✗ Telegram request timeout - check internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Connection error - can't reach Telegram servers")
        return False
    except Exception as e:
        print(f"✗ Error sending Telegram message: {e}")
        return False


def send_telegram_photo_with_caption(image_path, caption_text):
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("✗ Telegram bot token not configured!")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        
        with open(image_path, 'rb') as f:
            files = {'photo': f}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption_text,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            if DEBUG_MODE:
                print("✓ Photo sent to Telegram successfully")
            return True
        else:
            print(f"✗ Telegram API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error sending photo: {e}")
        return False

def generate_attendance_report(date_str=None):
    summary = get_attendance_summary(date_str)
    
    if date_str is None:
        date_str = str(date.today())
    
    report = f"📋 <b>ATTENDANCE REPORT</b>\n"
    report += f"📅 Date: <b>{date_str}</b>\n"
    report += f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    report += f"👥 <b>Total Students:</b> {summary['total']}\n"
    report += f"✅ <b>Present:</b> <b>{summary['present']}</b>\n"
    report += f"❌ <b>Absent:</b> <b>{summary['absent']}</b>\n"
    
    if summary['total'] > 0:
        percentage = (summary['present'] / summary['total']) * 100
        report += f"📊 <b>Attendance %:</b> {percentage:.1f}%\n"
    
    report += f"\n━━━━━━━━━━━━━━━━━━━━━━━━\n"
  
    if summary['present_students']:
        report += f"\n✅ <b>PRESENT STUDENTS ({len(summary['present_students'])}):</b>\n"
        report += "─────────────────────────\n"
        for roll_no, name in summary['present_students']:
            report += f"  • <b>{roll_no}.</b> {name}\n"
    
    if summary['absent_students']:
        report += f"\n❌ <b>ABSENT STUDENTS ({len(summary['absent_students'])}):</b>\n"
        report += "─────────────────────────\n"
        for roll_no, name in summary['absent_students']:
            report += f"  • <b>{roll_no}.</b> {name}\n"
    
    return report


def generate_summary_report(date_str=None):
    """
    Generate a short summary report (best for quick updates)
    Args:
        date_str: Date in format YYYY-MM-DD (default: today)
    Returns:
        Formatted summary string
    """
    summary = get_attendance_summary(date_str)
    
    if date_str is None:
        date_str = str(date.today())
    
    report = f"📊 <b>ATTENDANCE SUMMARY</b>\n"
    report += f"📅 {date_str}\n"
    report += f"━━━━━━━━━━━━━━━━━━━\n"
    report += f"👥 Total: <b>{summary['total']}</b>\n"
    report += f"✅ Present: <b>{summary['present']}</b>\n"
    report += f"❌ Absent: <b>{summary['absent']}</b>\n"
    
    if summary['total'] > 0:
        percentage = (summary['present'] / summary['total']) * 100
        report += f"📈 Rate: <b>{percentage:.1f}%</b>"
    
    return report


def send_attendance_report(detailed=True):
    """
    Send attendance report to Telegram
    Args:
        detailed: If True, send full report; if False, send summary
    Returns:
        True if successful
    """
    print("📤 Sending attendance report to Telegram...")
    
    if detailed:
        report = generate_attendance_report()
    else:
        report = generate_summary_report()
    
    success = send_telegram_message(report)
    
    if success:
        print("✓ Report sent successfully!")
    else:
        print("✗ Failed to send report")
        print("\nGenerated Report:")
        print(report)
    
    return success


def send_daily_reminder():
    """Send daily reminder message"""
    message = "🔔 <b>Daily Attendance Reminder</b>\n"
    message += "━━━━━━━━━━━━━━━━━━━━\n"
    message += "📌 Time to mark attendance!\n"
    message += "Please ensure all students mark their fingerprint.\n\n"
    message += "📅 Date: " + str(date.today())
    
    return send_telegram_message(message)


def send_late_arrival_alert(name, roll_no, time_str):
    """Send alert for late arrival"""
    message = f"⏰ <b>LATE ARRIVAL ALERT</b>\n"
    message += f"━━━━━━━━━━━━━━━━━━━\n"
    message += f"👤 Student: <b>{name}</b>\n"
    message += f"🔢 Roll No: <b>{roll_no}</b>\n"
    message += f"⏱️ Time: <b>{time_str}</b>\n"
    
    return send_telegram_message(message)



def clear_todays_attendance():
    """Clear today's attendance records (for reset)"""
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        today = str(date.today())
        
        c.execute("DELETE FROM attendance WHERE date=?", (today,))
        conn.commit()
        conn.close()
        
        print(f"✓ Cleared attendance for {today}")
        return True
    except Exception as e:
        print(f"✗ Error clearing attendance: {e}")
        return False


def export_attendance_csv(date_str=None, filename=None):
    """
    Export attendance to CSV file
    Args:
        date_str: Date in format YYYY-MM-DD (default: today)
        filename: Output filename (default: attendance_YYYY-MM-DD.csv)
    Returns:
        Filename if successful, None otherwise
    """
    if date_str is None:
        date_str = str(date.today())
    
    if filename is None:
        filename = f"attendance_{date_str}.csv"
    
    try:
        summary = get_attendance_summary(date_str)
        
        with open(filename, 'w') as f:
            f.write("Roll No,Name,Status\n")
            
            for roll_no, name in summary['present_students']:
                f.write(f"{roll_no},{name},Present\n")
            
            for roll_no, name in summary['absent_students']:
                f.write(f"{roll_no},{name},Absent\n")
        
        print(f"✓ Attendance exported to {filename}")
        return filename
    except Exception as e:
        print(f"✗ Error exporting CSV: {e}")
        return None


def get_monthly_attendance(month, year):
    """
    Get attendance statistics for a month
    Args:
        month: Month number (1-12)
        year: Year
    Returns:
        Dictionary with monthly stats
    """
    try:
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        
        # Get all students
        all_students = get_all_students()
        
        monthly_stats = {}
        
        for student in all_students:
            fingerprint_id, roll_no, name = student[0], student[1], student[2]
            
            c.execute("""SELECT COUNT(*) FROM attendance 
                        WHERE fingerprint_id=? 
                        AND strftime('%m', date)=? 
                        AND strftime('%Y', date)=?""",
                      (fingerprint_id, f"{month:02d}", str(year)))
            
            days_present = c.fetchone()[0]
            monthly_stats[name] = {
                'roll_no': roll_no,
                'present_days': days_present
            }
        
        conn.close()
        return monthly_stats
    except Exception as e:
        print(f"✗ Error getting monthly attendance: {e}")
        return {}



def initialize_attendance_system():
    """Initialize the attendance system"""
    print("🔧 Initializing Attendance System...")
    create_attendance_table()
    print("✓ Attendance system initialized")
