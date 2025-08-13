
from utils.captureImages import processImagesAndSave
from utils.checkAreaAndAngle import isAreaAndAngleGood
from utils.checkObject import idObjectPresent
from utils.pickBadAndPlace import pickBadAndPlace
from utils.getBurnedState import check_burned_state

import serial
import time

def main():

    tryNO=20
    i=1

    serial_port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

    while i<=tryNO:

        print(f"\n--- Iteration {i} ---")
        startTime = time.time()

        processImagesAndSave()
        objectDetected = idObjectPresent()
        if not objectDetected:
            badFound = False
        if objectDetected:
            areaAngleGood = isAreaAndAngleGood()
            if not areaAngleGood:
                badFound = True
            else:
                goodBurnedState = check_burned_state()
                if not goodBurnedState:
                    badFound = True
                else:
                    badFound = False
                                
        badFound = pickBadAndPlace(badFound)
        print(f"Iteration {i} completed in {time.time() - startTime:.2f} seconds.")
        i+=1
        time.sleep(0.5)

    serial_port.close()
    print("Serial connection closed.")

if __name__ == "__main__":
    main()
