class Command:
    def __init__(self, name, funct, arg_count) -> None:
        self.m_funct = funct
        self.m_name = name
        self.m_arg_count = arg_count
    
    def is_operator(self) -> bool:
        return False

    m_funct: callable
    m_arg_count: int
    m_name: str

class Operator(Command):
    def __init__(self, name, funct, prio):
        Command.__init__(self, name, funct, 2)
        self.m_priority = prio
    
    def is_operator(self) -> bool:
        return True
    
    m_priority: int


class CommandDir:
    def __init__(self):
        self.m_dict = {}
        self.m_operators = {}
        self.m_max_operator_prio = -1
    
    def add_command(self, comm: Command) -> None:
        self.m_dict[comm.m_name] = comm
        if comm.is_operator():
            self.m_operators[comm.m_name] = comm

    def get_command(self, name: str) -> Command:
        return self.m_dict[name]
    
    def get_operator(self, name: str) -> Command:
        return self.m_operators[name]
    
    def contains_command(self, name: str) -> bool:
        return name in self.m_dict
    
    def contains_operator(self, name: str) -> bool:
        return name in self.m_operators
    
    def merge_dirs(self, other) -> None:
        for key in other:
            self.m_dict[key] = other[key]

    m_dict: dict # map command name onto CommandInfo object
    m_operators: dict