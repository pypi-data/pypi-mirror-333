import sympy as sp

def solve_equation(equation, variable):
    x = sp.symbols(variable)
    solution = sp.solve(equation, x)
    return solution

def step_by_step_solution(equation, variable):
    x = sp.symbols(variable)
    steps = sp.solve(equation, x, dict=True)
    return steps