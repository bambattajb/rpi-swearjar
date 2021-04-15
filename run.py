import RPi.GPIO as GPIO
import time

from NFC import *
from db import *
from screen import *

if __name__ == '__main__':
    nfc = NFC()
    nfc.setup()
    db = SwearsDb()

    try:
        while True:

            # Wait for NFC detection
            uidStr = nfc.listen()
            if(uidStr):

                # We have what we need so free up GPIO
                del nfc

                # Instantiate screen on GPIO
                screen = Screen()

                # Throw a default message to the screen
                screen.draw("Processing")

                # Get user
                user = db.get_user(uidStr)
                if not user:
                    screen.draw("ID not recognised")
                else:
                    screen.draw("Hello %s %s" % (user[2], user[1]))
                    time.sleep(2)
                    swearcount = db.insert_swear(user[0])
                    screen.draw("%s swears logged\n\nToday: %s\nThis week: %s\nThis month: %s" % (swearcount['Total'], swearcount['Today'], swearcount['Week'], swearcount['Month']))

                time.sleep(3)
                # Instantiate NFC
                nfc = NFC()
                # RE-setup NFC
                nfc.setup()
                screen.clear()
                # Free GPIO for NFC
                del screen

    except Exception as e:
        print("Error in main loop")
        print(e)
    finally:
        GPIO.cleanup()
