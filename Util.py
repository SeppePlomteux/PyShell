def is_number(numstr:str) -> bool:
    try:
        float(numstr)
        return True
    except ValueError:
        return False

__bracket_dict = {  '(':')',
                    ')':'(',
                    '[':']',
                    ']':'[',
                    '{':'}',
                    '}':'{'}

__opening_bracket_list = ['(', '[', '{']
__closing_bracket_list = [')', ']', '}']

def get_matching_bracket(bracket: str) -> str:
    global __bracket_dict
    return __bracket_dict[bracket]

def is_opening_bracket(char: str) -> bool:
    global __opening_bracket_list
    return char in __opening_bracket_list

def is_closing_bracket(char: str) -> bool:
    global __closing_bracket_list
    return char in __closing_bracket_list

def is_bracket(char: str) -> bool:
    global __opening_bracket_list
    global __closing_bracket_list
    return char in __opening_bracket_list or char in __closing_bracket_list