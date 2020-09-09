#!/usr/bin/python3
from clock_timestamp_model import Model


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
        self.model = Model()
        self.running = True

    def run_rfid(self):
        # start RFID and beginning looking for card to scan
        while self.running:
            r_id = input('Scan card to clock in')
            if self.model.get_r_id(r_id):       # Check if card is attached to an employee
                state = self.user_state(r_id)   # Checks user's clock on/off status
                if not state:                   # Employee not clocked today.
                    self.clock_on(r_id)         # Clock employee in
                elif state == 'CLOCKED ON':     # Employee clocked on
                    self.clock_off(r_id)
                elif state == 'CLOCKED OFF':
                    print('Employee already clocked on and off today')
            else:
                print('Card does not exist')


    def user_state(self, r_id):
        emp_id = self.model.get_id_by_r_id(r_id)
        clocked_on = self.model.get_time('clock_on', emp_id, self.model.get_current_date())
        clocked_off = self.model.get_time('clock_off', emp_id, self.model.get_current_date())
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
        tag_id = input('scan card to store id')
        emp_id = input('Attach to which employee')
        self.model.set_r_id(emp_id, tag_id)
        print(f'Added {tag_id} to {emp_id}')

    # todo  preliminary done
    # todo now need to use the actual rfid stuff.


if __name__ == '__main__':
    import settings
    r = RfidController()
    # r.run_rfid()
    r.attach_rfid_card()

