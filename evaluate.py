
operators = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / (y+0.001), #deal with division by 0 later 
}


def evaluate(expr, x):
    if isinstance(expr, int):
        return expr
    
    if isinstance(expr, str):
        if expr == 'x':
            return x
        else:
            raise ValueError('Invalid expression must be an integer or x')
    
    if isinstance(expr, list):
        if not(len(expr) == 3):
            raise ValueError('Invalid expression must be length 3')

        op_func = operators[expr[0]]
        return op_func(evaluate(expr[1], x), evaluate(expr[2], x))



            
        
    
    