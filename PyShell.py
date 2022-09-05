from Expression import eval
from Command import Command, CommandDir
from Parser import * #parse_string, ParsingError
from DefaultComDir import get_default_com_dir
from os import getcwd
from collections.abc import Iterator


class PyShell:
    def __init__(self, com_dir: CommandDir = None):
        com_dir = com_dir if com_dir else {}
        self.m_command_dir = get_default_com_dir()
        self.m_command_dir.merge_dirs(com_dir)
        self.m_environment = {}
    
    def print_result(self, res, env):
        if isinstance(res, Iterator):
            for e in res:
                print(e)
        else:
            print(res)
        self.m_environment = env

    def run(self):
        while True:
            prompt = '\033[31m' + getcwd() + '>>\033[m'
            in_line = input(prompt).strip()
            if in_line.casefold() == 'exit':
                break
            if in_line == '':
                continue
            try:
                expr = parse_string(in_line, self.m_command_dir)
                eval(expr, self.m_environment, self.print_result)
            except ParsingError as pe:
                print ('Parsing Error:')
                print(pe)
            except RuntimeError as e:
                print('Unhandled exception encountered:')
                print(e)

    m_command_dir = None
    m_environment = None