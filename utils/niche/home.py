import wlkatapython
import serial
import time

# Configure the serial connection
# Replace "COM4" with your port (e.g., "/dev/ttyUSB0" on Linux)
# serial_port = serial.Serial("COM4", 115200, timeout=1)
serial_port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
# Create a Mirobot object
mirobot = wlkatapython.Mirobot_UART()

# Initialize the Mirobot with the serial connection
# Address -1 is used for direct connection; adjust if using a multi-function controller
mirobot.init(serial_port, -1)
# Home the robotic arm (move to initial zero position)
print("Homing the robotic arm...")
# mirobot.zero()
mirobot.homing()  # Robotic arm homing

# mirobot.pump(0)
time.sleep(5)  # Wait for homing to complete
serial_port.close()
print("Serial connection closed.")