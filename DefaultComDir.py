from Command import Command, Operator, CommandDir
import os
from re import search
import requests as req
import Util as util

def my_map(arr, f):
    return map(f, arr)

def my_filter(arr, f):
    return filter(f, arr)

def flatten(iterable):
    result = []
    for arr in iterable:
        result += arr
    return result

def zip(iter1, iter2, f):
    it1 = iter(iter1)
    it2 = iter(iter2)
    def result():
        while True:
            try:
                x = next(it1)
                y = next(it2)
                yield f(x, y)
            except StopIteration:
                break
    return result()

def foldl(iter, f, base):
    for x in iter:
        base = f(base, x)
    return base

def foldr(iter, f, base):
    for x in list(iter)[::-1]:
        base = f(x, base)
    return base

def any_match(iter, predicate):
    for e in iter:
        if predicate(e):
            return True
    return False

def all_match(iter, predicate):
    for e in iter:
        if not predicate(e):
            return False
    return True

def match_count(iter, predicate):
    res = 0
    for e in iter:
        if predicate(e):
            res += 1
    return res

def my_plus(x, y):
    return x + y

def my_diff(x, y):
    return x - y

def my_mult(x, y):
    return x * y

def my_devide(x, y):
    return x / y

def my_whole_devide(x, y):
    return x // y

def my_modulo(x, y):
    return x % y

def load(filename):
    with open(filename, 'rt') as f:
        arr = f.readlines()
    return map(lambda l: l if len(l) == 0 or l[-1] != '\n' else l[0:-1], arr)

def store(iterable, filename):
    with open(filename, 'wt') as file:
        file.writelines(map(lambda x: x + '\n', iterable))
    return None

def to_int(val):
    return int(val)

def to_float(val):
    return float(val)

def to_bool(val):
    return bool(val)

def to_string(val):
    return str(val)

def to_list(val):
    return list(val)

def my_strip(val):
    return val.strip()

def my_split(delim, string):
    return string.split(delim)

def split_whitespace(string):
    return string.split()

def csplit(delim, string):
    res = []
    start = 0
    end = 0
    bracket_count = 0
    delimlen = len(delim)
    while end < len(string) - delimlen + 1:
        if util.is_opening_bracket(string[end]):
            bracket_count += 1
        elif util.is_closing_bracket(string[end]):
            bracket_count -= 1
        elif bracket_count > 0:
            pass
        elif delim == string[end:end+delimlen]:
            res.append(string[start:end])
            start = end + delimlen
            end = start - 1
        end += 1
    
    res.append(string[start:])
    return res
        

def pick(index, str_arr):
    return str_arr[index]

def in_list(lst, elem):
    return elem in lst

def construct_list(head, tail: list):
    return [head] + tail

def to_string(val):
    return str(val)

def to_ssstring(val):
    if len(val) == 0:
        return ''
    res = ''
    for s in val[:-1]:
        res += s + ' '
    res += val[-1]
    return res

def to_csstring(val):
    if len(val) == 0:
        return ''
    res = ''
    for s in val[:-1]:
        res += s + ','
    res += val[-1]
    return res


def is_empty(val):
    return val.strip() == ''

def dot(f1, f2):
    return lambda x: f1(f2(x))

def cd(path):
    os.chdir(path)
    return None

def ls():
    dirs = []
    files = []
    for f in os.listdir('.'):
        if os.path.isfile(f):
            files.append(f)
        else:
            dirs.append(f)
    res = ''

    for d in dirs:
        res += 'd ' + d + '\n'
    res += '\n'
    for f in files:
        res += 'f ' + f + '\n'

    return res

def echo(string):
    return string

def matches(pattern, string):
    m = search(pattern, string)
    return m != None

def match(pattern, string):
    m = search(pattern, string)
    return m[0]

def subst(orig, sub, string):
    origlen = len(orig)
    strlen = len(string)
    res = ''
    i = 0
    while i < strlen - origlen + 1:
        if orig == string[i:i+origlen]:
            res += sub
            i += origlen
        else:
            res += string[i]
            i += 1
    res += string[i:]
    return res

def curl(url):
    result = []
    with req.get(url, allow_redirects=False) as r:
        result.append('HTTP ' + str(r.status_code) + ' ' + r.reason)
        for key in r.headers:
            result.append(key + ': ' + r.headers[key])
        result.append('')
        result += r.text.splitlines(False)
    return iter(result)

def hcurl(url):
    result = []
    with req.get(url, allow_redirects=False) as r:
        result.append('HTTP ' + str(r.status_code) + ' ' + r.reason)
        for key in r.headers:
            result.append(key + ': ' + r.headers[key])
    return iter(result)

def my_and(left_arg, right_arg):
    return left_arg and right_arg

def my_or(left_arg, right_arg):
    return left_arg or right_arg

def my_xor(left_arg, right_arg):
    return (left_arg and not right_arg) or (not left_arg and right_arg)

def my_not(arg):
    return not arg

def my_equals(left_arg, right_arg):
    return left_arg == right_arg

def my_n_equals(left_arg, right_arg):
    return left_arg != right_arg

def my_greater_than(left_arg, right_arg):
    return left_arg > right_arg

def my_greater_than_or_eq(left_arg, right_arg):
    return left_arg >= right_arg

def my_less_than(left_arg, right_arg):
    return left_arg < right_arg

def my_less_than_or_eq(left_arg, right_arg):
    return left_arg <= right_arg

def get_default_com_dir():
    result = CommandDir()
    result.add_command(Command('map', my_map, 2))
    result.add_command(Command('filter', my_filter, 2))
    result.add_command(Command('flatten', flatten, 1))
    result.add_command(Command('zip', zip, 3))
    result.add_command(Command('foldl', foldl, 3))
    result.add_command(Command('foldr', foldr, 3))
    result.add_command(Command('anymatch', any_match, 2))
    result.add_command(Command('allmatch', all_match, 2))
    result.add_command(Command('matchcount', match_count, 2))
    result.add_command(Command('+', my_plus, 2))
    result.add_command(Command('-', my_diff, 2))
    result.add_command(Command('*', my_mult, 2))
    result.add_command(Command('/', my_devide, 2))
    result.add_command(Command('//', my_whole_devide, 2))
    result.add_command(Command('%', my_modulo, 2))
    result.add_command(Command('load', load, 1))
    result.add_command(Command('store', store, 2))
    result.add_command(Command('int', to_int, 1))
    result.add_command(Command('float', to_float, 1))
    result.add_command(Command('bool', to_bool, 1))
    result.add_command(Command('string', to_string, 1))
    result.add_command(Command('ssstring', to_ssstring, 1))
    result.add_command(Command('csstring', to_csstring, 1))
    result.add_command(Command('list', to_list, 1))
    result.add_command(Command('strip', my_strip, 1))
    result.add_command(Command('split', my_split, 2))
    result.add_command(Command('splitwh', split_whitespace, 1))
    result.add_command(Command('csplit', csplit, 2))
    result.add_command(Command('pick', pick, 2))
    result.add_command(Command('in', in_list, 2))
    result.add_command(Command('construct_list', construct_list, 2))
    result.add_command(Command('isempty', is_empty, 1))
    result.add_command(Operator('.', dot, 0))
    result.add_command(Command('cd', cd, 1))
    result.add_command(Command('ls', ls, 0))
    result.add_command(Command('echo', echo, 1))
    result.add_command(Command('matches', matches, 2))
    result.add_command(Command('match', match, 2))
    result.add_command(Command('subst', subst, 3))
    result.add_command(Command('curl', curl, 1))
    result.add_command(Command('hcurl', hcurl, 1))
    result.add_command(Command('and', my_and, 2))
    result.add_command(Command('or', my_or, 2))
    result.add_command(Command('xor', my_xor, 2))
    result.add_command(Command('not', my_not, 1))
    result.add_command(Command('==', my_equals, 2))
    result.add_command(Command('!=', my_n_equals, 2))
    result.add_command(Command('>', my_greater_than, 2))
    result.add_command(Command('>=', my_greater_than_or_eq, 2))
    result.add_command(Command('<', my_less_than, 2))
    result.add_command(Command('<=', my_less_than_or_eq, 2))

    return result
    