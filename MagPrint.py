import smbus2
import time

# I2C setup
bus = smbus2.SMBus(1)
addr = 0x23

# RM3100 register addresses
READ_START = 0x24  # X-axis MSB
BYTES_TO_READ = 9  # 3 bytes per axis (X, Y, Z)

# Function to convert 3 bytes to signed int
def bytes_to_int24(b):
    val = (b[0] << 16) | (b[1] << 8) | b[2]
    if val & (1 << 23):  # check sign bit
        val -= (1 << 24)
    return val

print("Reading RM3100 values... Press Ctrl+C to stop.")
try:
    while True:
        # Read 9 bytes from sensor
        raw = bus.read_i2c_block_data(addr, READ_START, BYTES_TO_READ)
        x = bytes_to_int24(raw[0:3])
        y = bytes_to_int24(raw[3:6])
        z = bytes_to_int24(raw[6:9])

        # Print to terminal
        print(f"X: {x}, Y: {y}, Z: {z}")
        time.sleep(0.2)  # ~5 Hz
except KeyboardInterrupt:
    print("Stopped.")
