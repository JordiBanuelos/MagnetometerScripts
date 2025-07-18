import smbus2
import time
import csv
import os
from datetime import datetime

# I2C setup
bus = smbus2.SMBus(1)
addr = 0x23

# RM3100 register addresses
READ_START = 0x24
BYTES_TO_READ = 9  # 3 bytes per axis (X, Y, Z)

# Get today's date for unique log file
date_str = datetime.now().strftime("%Y-%m-%d")
csv_filename = f"log_{date_str}.csv"
file_exists = os.path.isfile(csv_filename)

# Convert 3 bytes to signed 24-bit integer
def bytes_to_int24(b):
    val = (b[0] << 16) | (b[1] << 8) | b[2]
    if val & (1 << 23):
        val -= (1 << 24)
    return val

# Open CSV file and log data
with open(csv_filename, mode='a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if not file_exists:
        writer.writerow(['timestamp', 'x', 'y', 'z'])  # header

    print(f"📡 Logging RM3100 data to {csv_filename} (press Ctrl+C to stop)...\n")

    try:
        while True:
            raw = bus.read_i2c_block_data(addr, READ_START, BYTES_TO_READ)
            x = bytes_to_int24(raw[0:3])
            y = bytes_to_int24(raw[3:6])
            z = bytes_to_int24(raw[6:9])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Print to terminal
            print(f"[{timestamp}]  X: {x:<6}  Y: {y:<6}  Z: {z:<6}")

            # Log to CSV
            writer.writerow([timestamp, x, y, z])
            csvfile.flush()

            time.sleep(0.2)  # 5 Hz sampling rate
    except KeyboardInterrupt:
        print("\n🛑 Logging stopped. File saved:", csv_filename)
