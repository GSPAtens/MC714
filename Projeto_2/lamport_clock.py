#Relógio de Lamport

import time

from mpi4py import MPI


class LamportClock:
    def __init__(self, time=0):
        self.time = time

    def update(self, time):
        if time > self.time:
            self.time = time

    def tick(self):
        self.time += 1

    def get_time(self):
        return self.time


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

lamport_clock = LamportClock()

if rank == 0:
    lamport_clock.tick()
    data = {'msg': 'teste 0 para 1', 'time': lamport_clock.get_time()}
    print(f"[{rank}] Enviando mensagem: {data['msg']}")
    comm.send(data, dest = 1)

    lamport_clock.tick()
    data = {'msg': 'teste 0 para 2', 'time': lamport_clock.get_time()}
    print(f"[{rank}] Enviando mensagem: {data['msg']}")
    comm.send(data, dest = 2)

    lamport_clock.tick()
    data = {'msg': 'teste 0 para 3', 'time': lamport_clock.get_time()}
    print(f"[{rank}] Enviando mensagem: {data['msg']}")
    comm.send(data, dest = 3)

elif rank == 1:
    data = comm.recv()
    print(f"[{rank}] Mensagem recebida: {data['msg']}")
    lamport_clock.update(data['time'])

    lamport_clock.tick()
    data = {'msg': 'test 1 to 3', 'time': lamport_clock.get_time()}
    print(f"[{rank}] Enviando mensagem: {data['msg']}")
    comm.send(data, dest=3)

elif rank == 2:
    data_r = comm.irecv()

    lamport_clock.tick()
    data = {'msg': 'test 2 to 3', 'time': lamport_clock.get_time()}
    print(f"[{rank}] Enviando mensagem: {data['msg']}")
    comm.send(data, dest=3)

    data = data_r.wait()
    print(f"[{rank}] Mensagem recebida: {data['msg']}")
    lamport_clock.update(data['time'])

elif rank == 3:
    data = comm.recv()
    print(f"[{rank}] Mensagem recebida: {data['msg']}")
    lamport_clock.update(data['time'])

    data = comm.recv()
    print(f"[{rank}] Mensagem recebida: {data['msg']}")
    lamport_clock.update(data['time'])

time.sleep(0.5)

print(f"[{rank}] Tempo final: {lamport_clock.get_time()}")