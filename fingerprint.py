from pyfingerprint.pyfingerprint import PyFingerprint
from time import sleep
from database import get_stu_by_fingerid
import lcd
f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
def sensor_intialization():
    try:
        lcd.display_message("Fingerprint","Initializing...")
        sleep(2)
        if f.verifyPassword():
                print("Fingerprint Sensor Connected Successfully")
                lcd.display_message("Sensor Ready")
                sleep(2)
        else:
            raise ValueError("Wrong Sensor Password")
    except Exception as e:
        print("Error:", e)
        lcd.display_message("Sensor Error")
        sleep(3)
        exit()

def enroll_fingerprint():
    try:
        lcd.clear()
        lcd.display_message("Place Finger")
        print('Waiting for finger...')
        while ( f.readImage() == False ):
            sleep(1)

        print("Finger Detected")
        lcd.clear()
        lcd.display_message("Finger Detected")

        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        if positionNumber >= 0:
            print('Fingerprint already exists.')
            lcd.write_string("Fingerprint","Exists")
            exit(0)
        print('Remove finger...')
        while ( f.readImage() == True ):
            pass
        print('Waiting for same finger again...')
        while ( f.readImage() == False ):
            pass
        f.convertImage(0x02)
        if ( f.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')
        positionNumber = f.storeTemplate()
        print('Fingerprint enrolled successfully.')
        lcd.display_message("Fingerprint","Enrolled :)")
        return positionNumber

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def mark_attendance_by_fingerprint():
    try:
        lcd.write_string("Place Finger","Mark Attendance")
        print("Place finger to mark attendance.....")
        while ( f.readImage() == False ):
            sleep(.01)
        print("Finger Detected")
        lcd.clear()
        lcd.display_message("Finger Detected")

        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        if positionNumber >= 0:
            student=get_stu_by_fingerid(positionNumber)
            print(f"{student[2]} is Present.")
            lcd.write_string(student[2],"Present")
            return positionNumber
        else:
            print("First enroll to the database")
            lcd.write_string("Enroll to ","Database")
            exit(0)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
        
def get_fingerid():
    try:
        lcd.write_string("Scan Finger to",'Delete Student')
        print("Place finger to remove student from database.....")
        while ( f.readImage() == False ):
            sleep(.01)
        print("Finger Detected")
        lcd.clear()
        lcd.display_message("Finger Detected")

        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        if positionNumber >= 0:
            return positionNumber
        else:
            print("First enroll to the database")
            lcd.write_string("Enroll to Database")
            sleep(2)
            exit(0)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)
        




