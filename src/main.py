import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configure the serial port
port = 'COM4'
baudrate = 115200
ser = serial.Serial(port, baudrate, timeout=0.1)  # Non-blocking read with a small timeout

# Initialize the plot
fig, ax = plt.subplots()
heatmap = ax.imshow(np.zeros((8, 8)), vmin=0, vmax=1600, cmap='nipy_spectral')  # Changed to 'nipy_spectral'
ax.set_title("Sensor Data Heatmap")

# Buffer to store incoming data
data_buffer = ""

def update(frame):
    global data_buffer

    # Read all available data from the serial port
    raw_data = ser.read(ser.in_waiting).decode('latin-1', errors='ignore')
    data_buffer += raw_data

    # Check for the presence of start and stop identifiers
    start_index = data_buffer.find("[")
    stop_index = data_buffer.find("]")

    # Only process the most recent complete set of data
    if start_index != -1 and stop_index != -1 and stop_index > start_index:
        # Extract the latest data set and discard everything before it
        data_string = data_buffer[start_index + 1:stop_index]
        data_buffer = data_buffer[stop_index + 1:]  # Keep only unprocessed data

        # Split the data into values and convert to integers
        try:
            values = [int(v) for v in data_string.split(",")]
            if len(values) == 64:
                # Convert the list to a 2D numpy array and update the heatmap
                values_array = np.array(values).reshape((8, 8))
                heatmap.set_data(values_array)
        except ValueError:
            # Handle any conversion errors
            pass

    return [heatmap]

# Create an animation to update the heatmap in real-time
ani = animation.FuncAnimation(fig, update, interval=50)  # Reduced interval for more frequent updates

plt.colorbar(heatmap)
plt.show()
