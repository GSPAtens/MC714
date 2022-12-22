#Exclusão Mútua

#Foi implementado o Token Ring para realizar a exclusão mútua, que consiste em um anel
# lógico entre os processos, onde o processo em posse do token detém o acesso exclusivo,
# retendo o token caso possua interesse ou passando diretamente para o próximo processo.

#Para teste, foram atribuídos, em diferentes momentos, interesse pelo uso do token por alguns processos

import time

from mpi4py import MPI


class TokenRing:
    def __init__(self, nodes, token = False, interested = False):
        self.nodes = nodes
        self.token = token
        self.interested = interested

    def check_token(self):
        return self.token

    def pass_token(self, comm, rank):
        print(f"[{rank}] passando o token")
        if self.check_token():
            self.token = False
            comm.send(True, dest = (rank + 1) % self.nodes)

    def recv_token(self, comm, rank):
        self.token = comm.recv(source = (rank - 1) % self.nodes)
        print(f"[{rank}] recebeu o token")
        if not self.interested:
            self.pass_token(comm, rank)

    def set_interested(self, interested):
        self.interested = interested


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

token_ring = TokenRing(size, rank == 0, rank == 0)

for i in range(10):
    if rank == 0:
        if i == 0:
            if token_ring.check_token():
                print(f"[{rank}] usando o token")
            token_ring.pass_token(comm, rank)
            token_ring.set_interested(False)

        if i == 2:
            token_ring.set_interested(True)

        token_ring.recv_token(comm, rank)

        if i == 2:
            print(f"[{rank}] usando o token")
            token_ring.set_interested(False)
            token_ring.pass_token(comm, rank)

    elif rank == 1:
        if i == 4:
            token_ring.set_interested(True)

        token_ring.recv_token(comm, rank)

        if i == 4:
            print(f"[{rank}] usando o token")
            token_ring.set_interested(False)
            token_ring.pass_token(comm, rank)

    elif rank == 2:
        if i == 6:
            token_ring.set_interested(True)

        token_ring.recv_token(comm, rank)

        if i == 6:
            print(f"[{rank}] usando o token")
            token_ring.set_interested(False)
            token_ring.pass_token(comm, rank)

    elif rank == 3:
        if i == 5:
            token_ring.set_interested(True)

        token_ring.recv_token(comm, rank)

        if i == 5:
            print(f"[{rank}] usando o token")
            token_ring.set_interested(False)
            token_ring.pass_token(comm, rank)

    time.sleep(0.1)