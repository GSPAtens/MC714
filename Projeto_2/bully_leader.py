#Eleição

#Foi implementado o algoritmo Bully Leader para o problema da eleição, onde quando iniciada
# uma eleição, o processo com o maior ID entre os processos sem falha é selecionado como coordenador


import time

from mpi4py import MPI


class BullyLeader:
    def __init__(self, leader = 0):
        self.leader = leader

    def check_alive(self, comm, rank):
        msg = {'action': 'ALIVE_CHECK', 'from': rank}
        comm.send(msg, dest = self.leader)
        print(f'[{rank}] conferindo com a mensagem {msg}')
        resp = comm.irecv(source = self.leader)
        time.sleep(3)
        if resp.test()[0]:
            data = resp.wait()
            if data['action'] == 'OK':
                return True
        return False


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

eleicao = BullyLeader()
count = 0

while True:
    print(f"[{rank}] Loop")
    time.sleep(0.1)
    if rank != eleicao.leader:
        time.sleep(1)
        check = eleicao.check_alive(comm, rank)
        print(f"[{rank}] Check: {check}")
        # if not check:
        #     eleicao.request_election(comm, rank)
    else:
        req = comm.irecv()
        time.sleep(0.5)
        if req.test()[0]:
            print(f"[{rank}] Recebido")
            data = req.wait()
            print(data)
            source = data['from']
            print(f"[{rank}] from {source}")
            if data['action'] == 'ALIVE_CHECK':
                comm.send({'action': 'OK'}, dest = source)
        else:
            continue