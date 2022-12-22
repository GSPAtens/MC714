# **MC714 - Projeto 2**

|Nome|RA|
|---|---|
|Gabriel de Sousa Pereira|216194|

Este projeto consiste na implementação de algoritmos distribuídos direcionados para execução na nuvem, sendo eles: 
* Exclusão mútua (token ring)
* Eleição (bully leader)
* Relógio lógico de Lamport

## Uso

Para utilizar os algoritmos, é necessário o uso de Python3 e dos seguintes pacotes:
```
  sudo apt install libopenmpi-dev -y
  sudo apt install python3-pip -y
  pip3 install mpi4py
```

Para executar os algoritmos, onde numProc é o número de processos participando da dinâmica:
```
mpirun -mca btl ^openib -np numProc python3 token_ring.py
mpirun -mca btl ^openib -np numProc python3 bully_leader.py
mpirun -mca btl ^openib -np numProc python3 lamport_clock.py
```
