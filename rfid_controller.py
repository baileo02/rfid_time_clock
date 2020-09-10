#!/usr/bin/python3
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from time import sleep
from clock_timestamp_model import Model
from datetime import datetime

class RfidController:
    """
    Purpose of this class is to deal with everything RFID related.
    This includes starting up the rfid to continually search for a rfid tag, clocking in/out employees,
    displaying on the lcd user clocked in and time and a function allowing rfid tags to be attached to a user.

    run_rfid(): Should be run when the application starts. It continually looks for a RFID card to scan.
                The card scanned will then search and match an employee, clocking them on/off
    user_state(): Determines the user's clock in status for today's system date.
    clock_on(): Creates a new time record for an employee
    clock_off(): Updates the clock off time record using today's date and employee ID
    attach_rfid_card(): Used to assign rfid tags to employees' r_id field.
    """
    def __init__(self):
        # Start LCD function
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        # Create PCF8574 GPIO adapter.
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)        

        self.model = Model()
        self.running = True
        self.display_lcd_default()
    
    def alert(self):
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(16, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(16,GPIO.LOW)        
        GPIO.cleanup()  
        
    def run_rfid(self):
        
        MIFAREReader = MFRC522.MFRC522()
        
        while self.running:
            r_id = None
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL) # scan for card
            if status == MIFAREReader.MI_OK:    # if card is found
                print('card detected')
                #self.alert()#todo buzzer gpio is messing with the RFID GPIO
            (status, r_id) = MIFAREReader.MFRC522_Anticoll()  # get uid
            r_id = ''.join([str(a) for a in r_id])
            if status == MIFAREReader.MI_OK:    # if we have the uid
                if self.model.get_r_id(r_id):       # Check if card is attached to an employee
                    state = self.user_state(r_id)   # Checks user's clock on/off status
                    if not state:   # Employee not clocked today.
                        self.clock_on(r_id)         # Clock employee in
                        message = 'Hi '
                    elif state == 'CLOCKED ON':     # Employee clocked on
                        self.clock_off(r_id)
                        message = 'See you '
                    elif state == 'CLOCKED OFF':
                        message = 'Already clocked off '
                    else:
                        message = 'Error'
                    self.display_lcd(self.model.get_name_by_r_id(r_id), message)
                    self.model.db.mydb.commit()
                else:
                    self.display_lcd('Error!', 'Card does not exist')
            


    def user_state(self, r_id):
        emp_id = self.model.get_id_by_r_id(r_id)
        clocked_on = self.model.get_time('clock_on', emp_id, datetime.now().strftime('%Y-%m-%d'))
        clocked_off = self.model.get_time('clock_off', emp_id, datetime.now().strftime('%Y-%m-%d'))
        print(clocked_on)
        print(clocked_off)
        
        if clocked_on and clocked_off:
            return 'CLOCKED OFF'
        elif not clocked_on and not clocked_off:
            return None
        elif clocked_on and not clocked_off:
            return 'CLOCKED ON'

    def clock_on(self, r_id):
        emp_id = self.model.get_id_by_r_id(r_id)
        self.model.create_time_record('clock_on', emp_id, self.model.get_current_date(), self.model.get_current_time())

    def clock_off(self, r_id):
        emp_id = self.model.get_id_by_r_id(r_id)
        self.model.set_time_record('clock_off', emp_id, self.model.get_current_date(), self.model.get_current_time())

    def attach_rfid_card(self):
        emp_name = input('Attach to which employee')
        signal.signal(signal.SIGINT, self.end_read)
        MIFAREReader = MFRC522.MFRC522()
        while self.running:
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL) # scan for card
            if status == MIFAREReader.MI_OK:    # if card is found
                print('card detected')
            (status, r_id) = MIFAREReader.MFRC522_Anticoll()  # get rfid tag id
            r_id = ''.join([str(a) for a in r_id])      # store the list of integers as one string.
            if status == MIFAREReader.MI_OK:
                emp_id = self.model.get_id_by_name(emp_name)
                self.model.set_r_id(emp_id, r_id)
                print(f'Added {r_id} to {emp_name}')
                self.running = False
                
    def display_lcd_default(self):
        self.mcp.output(3,1)
        self.lcd.begin(16,2)
        self.lcd.clear()
        self.lcd.setCursor(2,0)
        self.lcd.message('READY TO SCAN')
        
    
    def display_lcd(self, name, message):
        try:
            self.mcp.output(3,1)     # turn on LCD backlight
            self.lcd.begin(16,2)     # set number of LCD lines and columns
            self.lcd.clear()
            self.lcd.setCursor(0,0)  # set cursor position
            self.lcd.message(message + name.capitalize() + '\n')
            self.lcd.message('Time now: ' + datetime.now().strftime('%H:%M'))
            sleep(5)
            self.lcd.clear()
        finally:
            GPIO.cleanup()
            self.display_lcd_default()

if __name__ == '__main__':
    import settings
    r = RfidController()
    r.run_rfid()
    # r.attach_rfid_card()
    #todo if user forgets to sign off, and date changes user cannot clock back in again 
    #todo unless app is restarted. need to refresh the db.


