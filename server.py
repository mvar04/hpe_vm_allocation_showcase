from vm import VM

class Server:
    def __init__(self, memory: int, cores: int):
        self.memory = memory
        self.cores = cores
        self.allocated = []

    def __repr__(self):
        return f"Server(Memory: {self.memory}, Free: {self.free_space()}, Cores: {self.cores}, Available Cores: {self.free_cores()}, VMs: {self.allocated})"

    def used_memory(self):
        return sum(vm.memory for vm in self.allocated)

    def free_space(self):
        return self.memory - self.used_memory()
        
    def free_cores(self):
        return self.cores - sum(vm.cores for vm in self.allocated)
        
    def used_cores(self):
        return sum(vm.cores for vm in self.allocated)
        
    def can_allocate(self, vm: VM, limit_ratio: float = 1.0):
        return (vm.memory <= self.memory * limit_ratio - self.used_memory()) and vm.cores <= self.free_cores()

    def allocate_vm(self, vm: VM, limit_ratio: float = 1.0):
        if self.can_allocate(vm, limit_ratio):
            self.allocated.append(vm)
            return True
        return False

    def remove_vm(self, vm: VM):
        self.allocated.remove(vm)

    def clear(self):
        self.allocated.clear()