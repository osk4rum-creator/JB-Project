class Machine:
    def __init__(self, name, os, cpu, ram):
        self.name = name
        self.os = os
        self.cpu = cpu
        self.ram = ram

    def to_dict(self):
        """Returns a dictionary representation for JSON storage."""
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram": self.ram
        }