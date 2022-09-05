from __future__ import annotations
from dataclasses import dataclass
from functools import partial
from inspect import signature

@dataclass
class LiteralExpression:
    m_value: any

@dataclass
class AssignExpression:
    m_identifier: str
    m_value: Expression

@dataclass
class VariableExpression:
    m_identifier: str

@dataclass
class FuncAppExpression:
    m_funct: Expression
    m_args: list[Expression]

@dataclass
class LambdaExpression:
    m_parameters: list[str]
    m_expr: Expression

Expression = LiteralExpression | AssignExpression | VariableExpression | FuncAppExpression | LambdaExpression

class LambdaFunction:
    def __init__(self, funct, args, env):
        self.m_funct = funct
        self.m_args = args
        self.m_environment = env
    m_funct: Expression
    m_args: list[str]
    m_environment: dict

    def __call__(self, *args, **kwargs):
        if len(args) > len(self.m_args):
            raise TypeError('Too many arguments')
        f_env = {}
        for k in self.m_environment:
            f_env[k] = self.m_environment[k]
        for i in range(len(args)):
            f_env[self.m_args[i]] = args[i]
        if len(args) == len(self.m_args):
            extractor = []
            eval(self.m_funct, f_env, lambda v, _: extractor.append(v))
            return extractor[0]
        return LambdaFunction(self.m_funct, self.m_args[len(args):], f_env)


def eval(exp: Expression, environment, continuation):
    match exp:
        case LiteralExpression(value):
            return continuation(value, environment)
        case VariableExpression(identifier):
            if identifier not in environment:
                return raise_exception('Unknown identifier', 'The identifier ' + identifier + ' is not bound to any value')
            return continuation(environment[identifier], environment)
        case AssignExpression(identifier, value_exp):
            return eval_assign_expr(identifier, value_exp, environment, continuation)
        case FuncAppExpression(func, args):
            return eval_func_app_expr(func, args, environment, continuation)
        case LambdaExpression(params, expr):
            return eval_lambda_expr(expr, params, environment, continuation)

def eval_lambda_expr(lambda_expr: Expression, params: list[str], environment, continuation):
    if len(params) == 0:
        return eval(lambda_expr, environment, continuation)
    capture_dict = {}
    for k in environment:
        capture_dict[k] = environment[k]
    funct = LambdaFunction(lambda_expr, params, capture_dict)
    return continuation(funct, environment)

def eval_assign_expr(identifier: str, value_exp: Expression, environment, continuation):
    return eval(value_exp, environment, lambda val, env: eval_assign_expr_cont(identifier, environment, continuation, val))

def eval_assign_expr_cont(identifier: str, environment, continuation, value: any):
    environment[identifier] = value
    return continuation(value, environment)

def eval_func_app_expr(funct: Expression, arg_exprs: list[Expression], environment, continuation):
    eval(funct, environment, lambda f, env: eval_func_app_expr_cont(f, arg_exprs, env, continuation, []))

def eval_func_app_expr_cont(funct, arg_exprs: list[Expression], environment, continuation, eval_args, index = 0):
    if index == len(arg_exprs):
        if isinstance(funct, LambdaFunction):
            if len(eval_args) > len(funct.m_args):
                return raise_exception('Too many arguments', 'Too many arguments were provided')
            eval_env = {}
            for k in funct.m_environment:
                eval_env[k] = funct.m_environment[k]
            for i in range(len(eval_args)):
                eval_env[funct.m_args[i]] = eval_args[i]
            if len(eval_args) == len(funct.m_args):
                return eval(funct.m_funct, eval_env, lambda v, _: continuation(v, environment))
            else:
                new_funct = LambdaFunction(funct.m_funct, funct.m_args[len(eval_args):], eval_env)
                return continuation(new_funct, environment)
            pass
        funct_sign = signature(funct)
        if len(funct_sign.parameters) == len(eval_args):
            return continuation(funct(*eval_args), environment)
        elif len(funct_sign.parameters) > len(eval_args):
            return continuation(partial(funct, *eval_args), environment)
        else:
            return raise_exception('Too many arguments', 'Too many arguments were provided')
    eval(arg_exprs[index], environment, lambda x, env: eval_func_app_expr_cont(funct, arg_exprs, env, continuation, eval_args + [x], index + 1))

def raise_exception(title: str, info: str) -> None:
    print('=== EXCEPTION ===')
    print(title + ':')
    print(info)