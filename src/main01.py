import pickle, sys, os
import numpy as np 
sys.path.append(os.path.dirname(os.getcwd()))
from utils.flow import Flow
from utils.switch import Switch
from utils.connection import Connection
import time 
import tensorflow as tf


input_path = '../generatedFlow/flows/10_packets.pkl'
output_path = 'output'
SIMULATION_TIME = 1 #minutes
SIMULATION_TIME = SIMULATION_TIME * 60 * pow(10,6) #microseconds
# simulation step micro seconds

with open(input_path, 'rb') as file:
    packets = pickle.load(file)
print(len(packets))


class Network():
    def __init__(self):
        self.switches = {}
        self.connections = {}
        self.remainingStreams = []
        self.successTransfer = []
        self.edges = []
        self.nodes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
        # TODO apply NSF
        # 21 bidirectional fibers links
        self.edges.append(('1','2',1100))
        self.edges.append(('1','3',1600))
        self.edges.append(('1','8',2800))
        self.edges.append(('2','3',600))
        self.edges.append(('2','4',1000))
        self.edges.append(('3','6',2000))
        self.edges.append(('4','5',600))
        self.edges.append(('4','11',2400))
        self.edges.append(('5','7',800))
        self.edges.append(('5','6',1100))
        self.edges.append(('6','10',1200))
        self.edges.append(('6','13',2000))
        self.edges.append(('7','8',700))
        self.edges.append(('8','9',700))
        self.edges.append(('9','10',900))
        self.edges.append(('9','12',500))
        self.edges.append(('9','14',500))
        self.edges.append(('11','12',800))
        self.edges.append(('11','14',800))
        self.edges.append(('12','13',300))
        self.edges.append(('13','14',300))

        # INIT  SWITCHES
        for n in range(len(self.nodes)):
            self.switches[n] = Switch(n, output_path)
        # INIT CONNECTIONS
        for ed in self.edges:
            connection = Connection(self.switches[int(ed[0])-1],self.switches[int(ed[1])-1],ed[2])
            self.switches[int(ed[0])-1].addConnection(connection)
            self.connections['%d-%d'%(self.switches[int(ed[0])-1].name,self.switches[int(ed[1])-1].name)] = connection
            connection = Connection(self.switches[int(ed[1])-1],self.switches[int(ed[0])-1],ed[2])
            self.switches[int(ed[1])-1].addConnection(connection)
            self.connections['%d-%d'%(self.switches[int(ed[1])-1].name,self.switches[int(ed[0])-1].name)] = connection

    def inPacket(self, packet, t):
        if len(self.switches[packet.src].queue) < self.switches[packet.src].MAXIMUM_QUEUE-1:
            self.switches[packet.src].enQueue(packet,t)
        else:
            self.remainingStreams.append(packet)

    def calculate_bezier_curve_points(self, start, control, end, t):
        x = (1 - t)**2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0]
        y = (1 - t)**2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]
        return x, y

    def readableNanoSeconds(self, t):
        m = int(t / (60 * pow(10,6)))
        s = t - (m * (60 * pow(10,6)))
        return '%d M %02.6f S'%(m,s/pow(10,6))

    def run(self, t, episode):
        # print('===============',self.readableNanoSeconds(t))
        for s in self.switches.keys():
            if len(self.switches[s].queue) == 0: continue
            # print('--------><')
            # print('%dBEFORE'%s)
            # for p in self.switches[s].queue:
            #     print('S',p)
            # print('TAKE ACTION..........')
            for p in self.switches[s].queue:
                self.switches[s].randomForward(p,t)
            # print('AFTER')
            # for p in self.switches[s].queue:
            #     print('S',p)

        # FREE CONNECTION
        for c in self.connections.keys():
            if self.connections[c].packet == None: continue
            if t/pow(10,6) >= self.connections[c].availableTime and t != 0 and self.connections[c].packet != None:
                if len(self.switches[self.connections[c].dst.name].queue) < self.switches[self.connections[c].dst.name].MAXIMUM_QUEUE:
                    self.connections[c].packet.current_location = self.connections[c].dst.name
                    self.connections[c].packet.timestamp['IN-%d'%self.connections[c].dst.name] = t/pow(10,6) 
                    if self.connections[c].packet.current_location == self.connections[c].packet.dst:
                        self.successTransfer.append(self.connections[c].packet)
                        with open('results/%s/tmp_pk/%d/P%d.pkl'%(output_path,episode,self.connections[c].packet.id), 'wb') as file:
                            pickle.dump(self.connections[c].packet, file)
                        # for ss in self.switches.keys():
                        #     with open('tmp_pk/S%d.pkl'%ss, 'wb') as file:
                        #         pickle.dump(self.switches[ss], file)
                        # for cc in self.connections.keys():
                        #     with open('tmp_pk/C%s.pkl'%cc, 'wb') as file:
                        #         pickle.dump(self.connections[cc], file)
                    else:
                        self.switches[self.connections[c].dst.name].enQueue(self.connections[c].packet,t/pow(10,6))
                    self.connections[c].packet = None
                # else:


        # ENQUEUE
        for p in self.remainingStreams:
            if len(self.switches[p.src].queue) < self.switches[p.src].MAXIMUM_QUEUE - 1:
                # print('y')
                self.switches[p.src].enQueue(p,t) #sim time
                self.remainingStreams.remove(p)
                
# print('Total packets: ',len(packets))
# network = Network()
# for p in packets:
#     network.inPacket(p,0)


# packets_in_each_sw = np.zeros(14)
# for s in network.switches.keys():
#     packets_in_each_sw[s] = len(network.switches[s].queue)
# # print('In queue packets',packets_in_each_sw,sum(packets_in_each_sw))
# # print('Remaining packets',len(network.remainingStreams))
# # print('Success packets',len(network.successTransfer))
# packets_in_each_conn = 0
# for c in network.connections.keys():
#     if network.connections[c].packet != None:
#         packets_in_each_conn = packets_in_each_conn + 1
# # print('Connection packets',packets_in_each_conn,'/',len(network.connections.keys()))

# SIMULATION_TIME = 10 #minutes
# SIMULATION_TIME = SIMULATION_TIME * 60 * pow(10,6) #microseconds
# from tqdm import tqdm
# # progress_bar = total=len(packets), desc="Success packets")
# for sim_time in range(SIMULATION_TIME):
#     network.run(sim_time)
#     # print('===========',network.readableNanoSeconds(sim_time))
#     packets_in_each_sw = np.zeros(14)
#     for s in network.switches.keys():
#         packets_in_each_sw[s] = len(network.switches[s].queue)
#     print('In queue packets',packets_in_each_sw,sum(packets_in_each_sw))
#     print('Remaining packets',len(network.remainingStreams))
#     print('Success packets',len(network.successTransfer))
#     # progress_bar.update(n=1)
#     packets_in_each_conn = 0
#     for c in network.connections.keys():
#         if network.connections[c].packet != None:
#             packets_in_each_conn = packets_in_each_conn + 1
#     print('Connection packets',packets_in_each_conn,'/',len(network.connections.keys()))
#     if sum(packets_in_each_sw) + len(network.remainingStreams) + len(network.successTransfer) + packets_in_each_conn != len(packets):
#         arr = []
#         a = []
#         for i in packets:
#             arr.append(i)
#         for i in network.successTransfer:
#             a.append(i)
#         for c in network.connections.keys():
#             if network.connections[c].packet != None:
#                 a.append(network.connections[c].packet)
#         for s in network.switches.keys():
#             for p in network.switches[s].queue:
#                 a.append(p)
#         for i in arr:
#             if i not in a:
#                 print(i)
#         for p in network.switches[4].queue:
#             print(p)
#         break
#     if len(network.successTransfer) == len(packets): break

def simulation(episode):
    with open(input_path, 'rb') as file:
        packets = pickle.load(file)
    # packets = packets[:10]
    packets_src = np.zeros(14)
    packets_dst = np.zeros(14)
    for p in packets:
        packets_src[p.src] = packets_src[p.src] + 1
        packets_dst[p.dst] = packets_dst[p.dst] + 1
    print('Total packets: ',len(packets))
    network = Network()
    for p in packets:
        network.inPacket(p,0)
    
    # INIT MODEL
    for s in network.switches.keys():
        network.switches[s].init_model(episode)

    # packets_in_each_sw = np.zeros(9)
    # for s in network.switches.keys():
    #     packets_in_each_sw[s] = len(network.switches[s].queue)
    # print('In queue packets',packets_in_each_sw,sum(packets_in_each_sw))
    # print('Remaining packets',len(network.remainingStreams))
    # print('Success packets',len(network.successTransfer))
    # packets_in_each_conn = 0
    # for c in network.connections.keys():
    #     if network.connections[c].packet != None:
    #         packets_in_each_conn = packets_in_each_conn + 1
    # print('Connection packets',packets_in_each_conn,'/',len(network.connections.keys()))
    SIMULATION_TIME = 10 #minutes
    SIMULATION_TIME = SIMULATION_TIME * 60 * pow(10,6) #microseconds
    os.system('mkdir results/%s/tmp_pk/%d'%(output_path,episode))
    for sim_time in range(SIMULATION_TIME):
        s_tem = time.time()
        network.run(sim_time,episode)
        e_tem = time.time()
        print('===========',network.readableNanoSeconds(sim_time),e_tem-s_tem)
        packets_in_each_sw = np.zeros(14)
        for s in network.switches.keys():
            packets_in_each_sw[s] = len(network.switches[s].queue)
        print('In queue packets',packets_in_each_sw,sum(packets_in_each_sw))
        print('Remaining packets',len(network.remainingStreams))
        print('Success packets',len(network.successTransfer))
        packets_in_each_conn = 0
        for c in network.connections.keys():
            if network.connections[c].packet != None:
                packets_in_each_conn = packets_in_each_conn + 1
        print('Connection packets',packets_in_each_conn,'/',len(network.connections.keys()))
        if sum(packets_in_each_sw) + len(network.remainingStreams) + len(network.successTransfer) + packets_in_each_conn != len(packets):
            print('ERRROR')
            break
        if len(network.successTransfer) == len(packets): 
            print('SUCCESS')
            break
    # AFTER SIMULATION
    print('----------------------------------')
    for s in network.switches.keys():
        # print(s)
        # print(len(network.switches[s].rewards),len(network.switches[s].states))
        # print(np.array(network.switches[s].rewards).shape,np.array(network.switches[s].states).shape)
        os.system('mkdir results/%s/rewards_pk/%d'%(output_path,episode))
        with open('results/%s/rewards_pk/%d/S%d.pkl'%(output_path,episode,s), 'wb') as file:
            pickle.dump(network.switches[s].rewards, file)
        if len(network.switches[s].states) == 0:
            os.system('mkdir results/%s/loss_pk/%d'%(output_path,episode))
            with open('results/%s/loss_pk/%d/S%d.pkl'%(output_path,episode,s), 'wb') as file:
                pickle.dump(-99, file)
            # grads = tape.gradient(loss, network.switches[s].model.trainable_variables)
            # network.switches[s].optimizer.apply_gradients(zip(grads, network.switches[s].model.trainable_variables))
            network.switches[s].model.save_weights('results/%s/models/S%d_EP%d.weights.h5'%(output_path,network.switches[s].name,episode))
        else:
            returns = np.cumsum(network.switches[s].rewards[::-1])[::-1]
            advantages = returns - np.mean(returns)
            with tf.GradientTape() as tape:
                print(np.array(network.switches[s].states).shape)
                print(network.switches[s].model.input_shape)
                print(network.switches[s].model.output_shape)
                input_states = np.array(network.switches[s].states)
                input_states = input_states.reshape(input_states.shape[0],input_states.shape[2])
                logits = network.switches[s].model(input_states)
                action_masks = tf.one_hot(network.switches[s].actions, len(network.switches[s].outConnections.keys()))
                print(action_masks.shape,logits.shape)
                log_probs = tf.reduce_sum(action_masks * tf.math.log(logits), axis=1)
                loss = tf.reduce_mean(log_probs * network.switches[s].delay)
            os.system('mkdir results/%s/loss_pk/%d'%(output_path,episode))
            with open('results/%s/loss_pk/%d/S%d.pkl'%(output_path,episode,s), 'wb') as file:
                pickle.dump(loss, file)
            grads = tape.gradient(loss, network.switches[s].model.trainable_variables)
            network.switches[s].optimizer.apply_gradients(zip(grads, network.switches[s].model.trainable_variables))
            network.switches[s].model.save_weights('results/%s/models/S%d_EP%d.weights.h5'%(output_path,network.switches[s].name,episode))


for i in range(0,100):
    simulation(i)