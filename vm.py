class VM:
    def __init__(self, memory: int, cores: int):
        self.memory = memory
        self.cores = cores

    def __repr__(self):
        return f"VM(Memory: {self.memory}MB, Cores: {self.cores})"
