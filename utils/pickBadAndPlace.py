import wlkatapython
import serial
import time

# from part_1_integration import savepath_GetArea

# Configure the serial connection
# Replace "COM4" with your port (e.g., "/dev/ttyUSB0" on Linux)
# serial_port = serial.Serial("COM4", 115200, timeout=1)
serial_port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
# Create a Mirobot object
mirobot = wlkatapython.Mirobot_UART()
# Create a conveyor control object (assuming a similar structure to Mirobot)
conveyor = wlkatapython.Mirobot_UART()  # May need adjustment based on exact class
# Initialize the Mirobot with the serial connection
# Address -1 is used for direct connection; adjust if using a multi-function controller
mirobot.init(serial_port, -1)
conveyor.init(serial_port, -1)  # Address 1; adjust if needed
# Home the robotic arm (move to initial zero position)
print("Homing the robotic arm...")
#mirobot.homing() # Robotic arm homing

# i = 0

# bad_found = False
# tryNO=10
# while i<tryNO:
def pickBadAndPlace(bad_found: bool) -> bool:
    """
    Picks up a bad item and places it in the designated area.
    Args:
        bad_found (bool): Indicates if a bad item was detected.
    Returns:
        bool: True if a bad item was found and processed, False otherwise.
    """
    
    if not bad_found:
        conveyor.sendMsg("G91 G01 D15 F500")
        time.sleep(2)  # Wait for homing to complete

    else:
        conveyor.sendMsg("G91 G01 D15 F500")
        time.sleep(2)
        # Define joint angles (in degrees) for each axis (J1 to J6)
        #joint_angles = [0, 20, -15, 0, 10, 0]  # Example: J1=0°, J2=30°, J3=-15°, J4=0°, J5=45°, J6=0°
        # Set joint angles
        #print(f"Moving to joint angles: {joint_angles}")
        mirobot.speed(1)
        mirobot.writeangle(0,23.4,49.2,-24.1,-0.0,-26.8,-18.5)
        time.sleep(2)
        mirobot.writeangle(0,23.7,52.6,-24.2,-0.0,-30,-19)
        time.sleep(2)
        mirobot.pump(1)
        time.sleep(3)
        mirobot.zero()
        time.sleep(3)
        mirobot.writeangle(0,-56.1,16.1,15.4,0,-31.6,56.1)
        time.sleep(2)
        mirobot.writeangle(0,-56.1,18.5,16.3,0,-34.9,56.1)
        time.sleep(2)
        mirobot.pump(0)
        time.sleep(2)
        mirobot.zero()
        # time.sleep(2)
        # conveyor.sendMsg("G90 G01 D0 F500")
        # time.sleep(3)
        # Close the serial connection
        # serial_port.close()
        # print("Serial connection closed.")
        bad_found = True
    bad_found = False

    # serial_port.close()
    # print("Serial connection closed.")   
    return bad_found

 