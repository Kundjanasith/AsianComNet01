import os
import sys
import numpy as np 
import random

sys.path.append(os.path.dirname(os.getcwd()))
from utils.flow import Flow

output_path = 'flows/100_Packets.pkl'
num_flows = 100
num_switches = 14
list_switches = range(num_switches)

# [144p, 240p, 360p, 480p, 720p, 1080p]
pixels = np.array([36864, 102240, 230400, 409920, 921600, 2073600]) #pixels
data_size = (pixels*4)/pow(10,6) #MB (mega bytes)
print('DATA SIZE', data_size, 'MB')

packet_period = np.array([ 1.0/24, 1.0/30, 1.0/60]) #seconds
print('PERIOD', packet_period, 'SECONDS')
packet_deadline = np.array(range(1,11)) #milliseconds
packet_deadline = packet_deadline/pow(10,3) #seconds
print('DEADLINE', packet_deadline, 'SECONDS')

# 10 Gbits/s.
flows = []
for idx in range(num_flows):
    tmp_swtiches = list(list_switches).copy()
    src = random.choice(tmp_swtiches)
    tmp_swtiches.remove(src)
    dst = random.choice(tmp_swtiches)
    size = random.choice(data_size)
    period = random.choice(packet_period)
    deadline = random.choice(packet_deadline)
    flow = Flow(src=src, dst=dst, size=size, period=period, deadline=deadline)
    # print(idx, src, dst, size, period, deadline)
    flows.append(flow)

# import pickle 
# # save 
# with open(output_path, 'wb') as file:
#     pickle.dump(flows, file)

# # load
# with open(output_path, 'rb') as file:
#     flows = pickle.load(file)


