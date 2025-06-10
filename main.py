'''
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
'''

from server import Server
from vm import VM
from allocator import (
    greedy_allocate, 
    first_fit_allocate, 
    best_fit_allocate, 
    next_fit_allocate,
    weight_balanced_allocate,
    best_fit_epsilon_greedy_allocate,
    delayed_bin_packing_allocate
)
from config import DEFAULT_SERVER_CAPACITY, POOL

def print_servers(servers):
    print("\n=== Server States ===")
    for i, server in enumerate(servers):
        print(f"SERVER{i + 1}:")
        print(f"    Memory: {server.used_memory()}MB / {server.memory}MB ({server.used_memory() * 100 / server.memory}% used)")
        print(f"    CPUs: {server.used_cores()} / {server.cores} ({server.used_cores() * 100 / server.cores}% used)")
        print(f"    Active VMs: {len(server.allocated)}")
        print(f"    System CPU: {server.used_cores() * 100 / server.cores}%")
        print(f"    System Memory: {server.used_memory()}MB / {server.memory}MB ({server.used_memory() * 100 / server.memory}%)")
        print(f"    Disk Usage: 0%")
        print(f"    Load Average: 0.00")

def main():
    # Unpacking (memory, cores) from config
    servers = [Server(DEFAULT_SERVER_CAPACITY[0], DEFAULT_SERVER_CAPACITY[1]) for _ in range(POOL)]
    last_used_index = 0

    print("Select allocation algorithm:")
    print("1. Original Greedy (with reassignment)")
    print("2. First Fit")
    print("3. Best Fit")
    print("4. Next Fit")
    print("5. Weight Balanced")
    print("6. Epsilon Greedy Best Fit")
    print("7. Delayed Bin Packing")
    print(f"\nServer Pool Size: {POOL}, Each Server Capacity: {DEFAULT_SERVER_CAPACITY}")

    try:
        algorithm = int(input("Select algorithm (1-7): "))
        if algorithm not in range(1, 8):
            print("Invalid selection. Defaulting to Best Fit (3).")
            algorithm = 3
    except ValueError:
        print("Invalid input. Defaulting to Best Fit (3).")
        algorithm = 3

    print("\nUsing allocation strategy:", {
        1: "Original Greedy",
        2: "First Fit",
        3: "Best Fit",
        4: "Next Fit",
        5: "Weight Balanced",
        6: "Best Fit Epsilon Greedy",
        7: "Delayed Bin Packing"
    }[algorithm])

    print("Enter VM requirements as: <memory> <cpu> (type 'exit' to stop)")

    while True:
        entry = input("New VM > ")
        if entry.lower() == 'exit':
            break

        try:
            mem, cpu = map(int, entry.strip().split())
            vm = VM(mem, cpu)
            success = False

            if algorithm == 1:
                success = greedy_allocate(servers, vm)
            elif algorithm == 2:
                success = first_fit_allocate(servers, vm)
            elif algorithm == 3:
                success = best_fit_allocate(servers, vm)
            elif algorithm == 4:
                last_used_index, success = next_fit_allocate(servers, vm, last_used_index)
            elif algorithm == 5:
                success = weight_balanced_allocate(servers, vm)
            elif algorithm == 6:
                success = best_fit_epsilon_greedy_allocate(servers, vm)
            elif algorithm == 7:
                success = delayed_bin_packing_allocate(servers, vm)

            if success:
                print(f"VM(mem={mem}, cpu={cpu}) allocated successfully.")
            else:
                print(f"Could NOT allocate VM(mem={mem}, cpu={cpu}) – insufficient resources.")

            print_servers(servers)

        except ValueError:
            print("Invalid input. Enter two integers: <memory> <cpu>")

if __name__ == "__main__":
    main()

