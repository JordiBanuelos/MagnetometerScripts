import smbus2
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# I2C setup
bus = smbus2.SMBus(1)
addr = 0x23

# RM3100 register addresses
READ_START = 0x24  # X-axis MSB
BYTES_TO_READ = 9  # 3 bytes per axis (X, Y, Z)

# Rolling window of data
time_window = 100  # number of data points to show
x_data, y_data, z_data = [], [], []
t_data = []

# Set up plot
plt.style.use('seaborn')
fig, ax = plt.subplots()
line_x, = ax.plot([], [], label='X (nT)', color='red')
line_y, = ax.plot([], [], label='Y (nT)', color='green')
line_z, = ax.plot([], [], label='Z (nT)', color='blue')
ax.set_ylim(-1000, 1000)  # Adjust this range to fit your expected data
ax.set_xlim(0, time_window)
ax.set_title('Real-Time Magnetic Field')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Mag Field (nT)')
ax.legend(loc='upper left')

# Function to convert 3 bytes to signed int
def bytes_to_int24(b):
    val = (b[0] << 16) | (b[1] << 8) | b[2]
    if val & (1 << 23):
        val -= (1 << 24)
    return val

# Animation update function
def update(frame):
    global x_data, y_data, z_data, t_data
    try:
        raw = bus.read_i2c_block_data(addr, READ_START, BYTES_TO_READ)
        x = bytes_to_int24(raw[0:3])
        y = bytes_to_int24(raw[3:6])
        z = bytes_to_int24(raw[6:9])

        t_data.append(time.time())
        x_data.append(x)
        y_data.append(y)
        z_data.append(z)

        if len(t_data) > time_window:
            t_data = t_data[-time_window:]
            x_data = x_data[-time_window:]
            y_data = y_data[-time_window:]
            z_data = z_data[-time_window:]

        t_relative = [t - t_data[0] for t in t_data]
        line_x.set_data(t_relative, x_data)
        line_y.set_data(t_relative, y_data)
        line_z.set_data(t_relative, z_data)

        ax.set_xlim(max(0, t_relative[0]), t_relative[-1] + 1)
    except Exception as e:
        print("Read error:", e)

    return line_x, line_y, line_z

ani = FuncAnimation(fig, update, interval=200)  # update every 200 ms
plt.tight_layout()
plt.show()

