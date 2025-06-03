from server import Server
from vm import VM
from config import LIMIT_RATIO, POOL
from allocator import first_fit_allocate

servers = [(4, 4), (8, 4), (10, 4), (6, 4)]
vms = [(6, 1), (2, 1), (4, 1), (6, 1), (2, 1)]

servers = [Server(i[0], i[1]) for i in servers]
vms = [VM(i[0], i[1]) for i in vms]


for vm in vms:
	first_fit_allocate(servers, vm)
	
print(servers)