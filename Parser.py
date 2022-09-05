from __future__ import annotations
from dataclasses import dataclass
from Expression import *
from Util import *
from Command import *
from math import inf

class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        m_message = message
    
    def __repr__(self):
        return 'Parsing failure: ' + self.m_message

    m_message: str

def concat_list(str_arr: list[str]) -> str:
    acc = ''
    [acc := acc + i + ' ' for i in str_arr]
    return '' if acc == '' else acc[0:-1]

def parse_token(token:str, com_dir: CommandDir) -> Expression:
    if token.casefold() == 'true'.casefold():
        return LiteralExpression(True)
    elif token.casefold() == 'false'.casefold():
        return LiteralExpression(False)
    elif token.casefold() == 'nil'.casefold():
        return LiteralExpression([])
    elif token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
        return LiteralExpression(int(token))
    elif token[0] == '"' or token[0] == '\'':
        return LiteralExpression(token[1:-1])
    elif is_number(token):
        return LiteralExpression(float(token))
    elif com_dir.contains_command(token):
        command = com_dir.get_command(token)
        if command.m_arg_count == 0:
            return FuncAppExpression(LiteralExpression(command.m_funct), [])
        return LiteralExpression(command.m_funct)
    else:
        return VariableExpression(token)


def match_brackets(str_arr: list[str]) -> tuple[dict, bool]:
    bracket_stack = []
    retval = {}
    for i in range(len(str_arr)):
        if is_opening_bracket(str_arr[i]):
            bracket_stack.append((str_arr[i], i))
        elif is_closing_bracket(str_arr[i]):
            if len(bracket_stack) == 0:
                return (None, False)
            (matching_bracket_char, matching_bracket_pos) = bracket_stack.pop()
            if get_matching_bracket(matching_bracket_char) != str_arr[i]:
                return (None, False)
            retval[matching_bracket_pos] = i
            retval[i] = matching_bracket_pos
    if len(bracket_stack) != 0:
        return (None, False)
    return (retval, True)

def get_block(str_arr: list[str], bracket_dict: dict, start: int) -> tuple[int, int]:
    if is_opening_bracket(str_arr[start]):
        matching_bracket = bracket_dict[start]
        return (start, matching_bracket + 1)
    else:
        return (start, start + 1)

def parse_splitted_string(str_arr: list[str], bracket_dict: dict, start: int, end: int, com_dir: CommandDir, err_trace = '') -> Expression:
    if end - start <= 0:
        raise ParsingError('Expected token or identifier\n' + err_trace)
    if end - start == 1:
        return parse_token(str_arr[start], com_dir)
    if str_arr[start] == '(' and bracket_dict[start] == end - 1:
        return parse_splitted_string(str_arr, bracket_dict, start + 1, end - 1, com_dir, err_trace + 'In subexpression ' + concat_list(str_arr[start+1:end-1]) + '\n')
    
    i = start
    leftmost_assignment = None
    leftmost_lambda = None
    while i < end:
        if is_opening_bracket(str_arr[i]):
            i = bracket_dict[i] + 1
        elif str_arr[i] == '=':
            leftmost_assignment = i
            break
        elif str_arr[i] == '->':
            leftmost_lambda = i
            break
        else:
            i += 1
    
    if leftmost_lambda != None:
        params = str_arr[start:leftmost_lambda]
        expr = parse_splitted_string(str_arr, bracket_dict, leftmost_lambda+1, end, com_dir, err_trace + 'In lambda ' + concat_list(str_arr[start:end]) + '\n')
        return LambdaExpression(params, expr)
    if leftmost_assignment != None:
        if leftmost_assignment - start != 1:
            raise ParsingError('Invalid variable identifier: ' + str_arr[start:leftmost_assignment] + '\n' + err_trace)
        ass_value = parse_splitted_string(str_arr, bracket_dict, leftmost_assignment+1, end, com_dir, err_trace + 'In assigment operant ' + concat_list(str_arr[leftmost_assignment+1:end]) + '\n')
        return AssignExpression(str_arr[start], ass_value)

    i = start
    priority = inf
    rightmost_op = None
    while i < end:
        if is_opening_bracket(str_arr[i]):
            i = bracket_dict[i] + 1
        elif com_dir.contains_operator(str_arr[i]) and com_dir.get_operator(str_arr[i]).m_priority <= priority:
            rightmost_op = i
            priority = com_dir.get_operator(str_arr[i]).m_priority
            i += 1
        else:
            i += 1
    
    if rightmost_op != None:
        function = parse_splitted_string(str_arr, bracket_dict, rightmost_op, rightmost_op+1, com_dir, err_trace + 'In operator expression ' + concat_list(str_arr[rightmost_op:rightmost_op+1]) + '\n')
        first_arg = parse_splitted_string(str_arr, bracket_dict, start, rightmost_op, com_dir, err_trace + 'In left operant operant ' + concat_list(str_arr[start:rightmost_op]) + '\n')
        second_arg = parse_splitted_string(str_arr, bracket_dict, rightmost_op+1, end, com_dir, err_trace + 'In right operant operant ' + concat_list(str_arr[rightmost_op+1:end]) + '\n')
        return FuncAppExpression(function, [first_arg, second_arg])
    
    arg_exp_list = []
    (fn_start, fn_end) = get_block(str_arr, bracket_dict, start)
    function_exp = parse_splitted_string(str_arr, bracket_dict, fn_start, fn_end, com_dir, err_trace + 'In function expression ' + concat_list(str_arr[fn_start:fn_end]) + '\n')

    i = fn_end
    while i < end:
        (arg_start, arg_end) = get_block(str_arr, bracket_dict, i)
        arg_exp_list.append(parse_splitted_string(str_arr, bracket_dict, arg_start, arg_end, com_dir, err_trace + 'In argument expression ' + concat_list(str_arr[arg_start:arg_end]) + '\n'))
        i = arg_end
    
    if i > end:
        raise ParsingError('Syntax Error' + err_trace)

    return FuncAppExpression(function_exp, arg_exp_list)

def reorder_pipes(str_arr: list[str]) -> list[str]:
    (bracket_dict, _) = match_brackets(str_arr)
    i = len(str_arr) - 1
    rightmost_pipe = None
    while i >= 0:
        if is_closing_bracket(str_arr[i]):
            i = bracket_dict[i]
        elif str_arr[i] == '|':
            rightmost_pipe = i
            (f_start, f_end) = get_block(str_arr, bracket_dict, i + 1)
            beginning = str_arr[f_start:f_end]
            middle = reorder_pipes(str_arr[0:i])
            end = str_arr[f_end:]
            break
        else:
            i -= 1
    
    def reorder_subexpressions(arr: list[str], bracket_dict: dict) -> list[str]:
        i = len(arr) - 1
        while i >= 0:
            if is_closing_bracket(str_arr[i]):
                j = bracket_dict[i]
                arr = arr[0:j+1] + reorder_pipes(arr[j+1:i]) + arr[i:]
                i = j-1
            else:
                i -= 1
        return arr


    if rightmost_pipe == None:
        return reorder_subexpressions(str_arr, bracket_dict)
    
    (bracket_dict, _) = match_brackets(beginning)
    beginning = reorder_subexpressions(beginning, bracket_dict)
    (bracket_dict, _) = match_brackets(end)
    end = reorder_subexpressions(end, bracket_dict)
    
    return beginning + ['('] + middle + [')'] + end

def handle_array(str_arr: list[str]) -> list[str]:
    (bracket_dict, _) = match_brackets(str_arr)
    if len(str_arr) == 0:
        return ['nil']
    
    i = 0
    leftmost_comma = None
    while i < len(str_arr):
        if is_opening_bracket(str_arr[i]):
            i = bracket_dict[i]
        elif str_arr[i] == ',':
            leftmost_comma = i
            break
        else:
            i += 1
    
    if leftmost_comma == None:
        head = expand_arrays(str_arr)
        tail = ['nil']
    else:
        head = expand_arrays(str_arr[0:leftmost_comma])
        tail = handle_array(str_arr[leftmost_comma+1:])
    
    return ['(', 'construct_list', '('] + head + [')'] + tail + [')']
    

def expand_arrays(str_arr: list[str]) -> list[str]:
    (bracket_dict, _) = match_brackets(str_arr)
    i = len(str_arr) - 1
    while i >= 0:
        if str_arr[i] == ']':
            arr_start = bracket_dict[i]
            arr_end = i
            str_arr = str_arr[0:arr_start] + handle_array(str_arr[arr_start+1:arr_end]) + str_arr[arr_end+1:]
            i = arr_start - 1
        else:
            i -= 1
    return str_arr

def split_string(to_split: str) -> list[str]:
    special_tokens = ['(', ')', '|', '[', ']', ',']
    string_delims = ['\'', '"']
    result = []
    i = 0
    while i < len(to_split):
        if to_split[i] in special_tokens:
            result.append(to_split[i])
            i += 1
        elif to_split[i] in string_delims:
            j = i + 1
            while to_split[j] != to_split[i]:
                j += 1
            result.append(to_split[i:j+1])
            i = j + 1
        elif not to_split[i].isspace():
            j = i + 1
            while j < len(to_split) and not to_split[j].isspace() and not to_split[j] in special_tokens:
                j += 1
            result.append(to_split[i:j])
            i = j
        else:
            i += 1
    return result


def parse_string(to_parse: str, com_dir: CommandDir) -> SyntaxTree:
    splitted = split_string(to_parse)
    (bracket_dict, success) = match_brackets(splitted)
    if not success:
        raise ParsingError('Invalid syntax: unmatched brackets')
    arrs_expanded = expand_arrays(splitted)
    (bracket_dict, success) = match_brackets(arrs_expanded)
    pipes_reordered = reorder_pipes(arrs_expanded)
    (bracket_dict, success) = match_brackets(pipes_reordered)
    if not success:
        raise RuntimeError('Encountered failure while parsing')
    return parse_splitted_string(pipes_reordered, bracket_dict, 0, len(pipes_reordered), com_dir, 'In Expression ' + to_parse + '\n')
