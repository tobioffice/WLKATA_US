import wlkatapython
import serial
import time

# from part_1_integration import savepath_GetArea

# Configure the serial connection
# Replace "COM4" with your port (e.g., "/dev/ttyUSB0" on Linux)
# serial_port = serial.Serial("COM4", 115200, timeout=1)
serial_port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
# Create a Mirobot object
# mirobot = wlkatapython.Mirobot_UART()
# Create a conveyor control object (assuming a similar structure to Mirobot)
conveyor = wlkatapython.Mirobot_UART()  # May need adjustment based on exact class
# Initialize the Mirobot with the serial connection
# Address -1 is used for direct connection; adjust if using a multi-function controller
# mirobot.init(serial_port, -1)
conveyor.init(serial_port, -1)  # Address 1; adjust if needed
# Home the robotic arm (move to initial zero position)
print("Homing the robotic arm...")

conveyor.sendMsg("G90 G01 D0 F500") 

serial_port.close()
print("Serial connection closed.")