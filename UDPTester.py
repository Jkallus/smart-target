import csv
import socket
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
from threading import Thread, Lock

localIP = "192.168.8.19"
localPort = 65238
bufferSize = 1024
 
datapoints_per_second = 0

def print_datapoints_per_second():
    global datapoints_per_second
    while True:
        time.sleep(1)  # Sleep for 1 second
        with lock:
            print(f"Datapoints per second: {datapoints_per_second}")
            datapoints_per_second = 0

print_thread = Thread(target=print_datapoints_per_second)
print_thread.start()

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

class Datapoint():
    def __init__(self, bl_ax: float, bl_ay: float, bl_az: float, tr_ax: float, tr_ay: float, tr_az: float, ms: int) -> None:
        self.bl_ax = bl_ax
        self.bl_ay = bl_ay
        self.bl_az = bl_az
        self.tr_ax = tr_ax
        self.tr_ay = tr_ay
        self.tr_az = tr_az
        #self.gx = gx
        #self.gy = gy
        #self.gz = gz
        self.ms = ms

def parse_data_string(data_str: str) -> Datapoint:
    labels = {}
    values = data_str.split(',')
    for value in values:
        key, val = value.split(':')
        if key == 'ms':
            labels[key] = int(val)
        else:
            labels[key] = float(val)    
    return Datapoint(labels['blax'], labels['blay'], labels['blaz'], labels['trax'], labels['tray'], labels['traz'], labels['ms'])

lock = Lock()
live_data: deque[Datapoint] = deque(maxlen=1000)

csv_file_path = 'datapoints.csv'
csvfile = open(csv_file_path, 'w', newline='')
fieldnames = ['blax', 'blay', 'blaz', 'trax', 'tray', 'traz', 'ms']
csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
csv_writer.writeheader()

def fetch_data(buffer: deque[Datapoint]):
    global datapoints_per_second
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        clientMsg = message.decode()
        with lock:
            datapoint = parse_data_string(clientMsg)
            #buffer.append(datapoint)
            datapoints_per_second += 1    
            # Write datapoint to CSV
            csv_writer.writerow({
                    'blax': datapoint.bl_ax,
                    'blay': datapoint.bl_ay,
                    'blaz': datapoint.bl_az,
                    'trax': datapoint.tr_ax,
                    'tray': datapoint.tr_ay,
                    'traz': datapoint.tr_az,
                    'ms': datapoint.ms
            })

thread = Thread(target=fetch_data, args=(live_data,))
thread.start()

# fig = plt.figure()
# axes = fig.add_subplot(1, 1, 1)

# def get_ms_component(data: deque[Datapoint]) -> list[int]:
#     return [datapoint.ms for datapoint in data]

# def get_ax_component(data: deque[Datapoint]) -> list[float]:
#    return [datapoint.ax for datapoint in data]
    
# def get_ay_component(data: deque[Datapoint]) -> list[float]:
#     return [datapoint.ay for datapoint in data]

# def get_az_component(data: deque[Datapoint]) -> list[float]:
#     return [datapoint.az for datapoint in data]

# def get_gx_component(data: deque[Datapoint]) -> list[float]:
#     return [datapoint.gx for datapoint in data]

# def get_gy_component(data: deque[Datapoint]) -> list[float]:
#     return [datapoint.gy for datapoint in data]

# def get_gz_component(data: deque[Datapoint]) -> list[float]:
#     return [datapoint.gz for datapoint in data]
    
# def animate(i, live_data: deque[Datapoint]):
#     axes.clear()
#     with lock:
#         t = get_ms_component(live_data)    
#         ax = get_ax_component(live_data)
#         ay = get_ay_component(live_data)
#         az = get_az_component(live_data)
#         gx = get_gx_component(live_data)
#         gy = get_gy_component(live_data)
#         gz = get_gz_component(live_data)
    
#     # Plotting ax
#     axes.plot(t, ax, label='ax')

#     # Plotting ay
#     axes.plot(t, ay, label='ay')

#     # Plotting az
#     axes.plot(t, az, label='az')

# #     # Plotting gx
# #     axes.plot(t, gx, label='gx')

# #     # Plotting gy
# #     axes.plot(t, gy, label='gy')

# #     # Plotting gz
# #     axes.plot(t, gz, label='gz')

#     axes.legend()

# ani = FuncAnimation(fig, animate, fargs = (live_data,), interval = 1000/60)
# plt.show()