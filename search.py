import copy 
import random
from evaluate import evaluate

grammar = [
    -2, 
    -1, 
    0,
    1, 
    2, 
    ['+', "tbf", "tbf"],
    ['-', "tbf", "tbf"],
    ['*', "tbf", "tbf"],
    ['/', "tbf", "tbf"],
    "x"
]

def get_grammar(grammar, i):
    elem = grammar[i]
    if isinstance(elem, list):
        elem = elem.copy()
    return elem

def get_random_grammar(grammar):
    elem = random.choice(grammar)
    if isinstance(elem, list):
        elem = elem.copy()
    return elem

def rec_len(expr):
    if not(isinstance(expr, list)):
        return 1
    else:
        return sum([rec_len(i) for i in expr])


def prob_search(inputs, targets, grammar, progs= [["tbf", 100]]): #idk what num to put there
    """
    inputs is a list of x inputs
    targets is a list of target values
    
    searches via at any time step, expanding the node with the highest rating
    
    ratings are determined by closeness to target value of 100 random program fill ins 
    
    this recursive program expands one "tbf" in the most likely partial program and possibly ends if finds program
    """
    
    #remove the highest scoring program from prog
    j = 0
    while(j < 50):
        j += 1
        # print(progs, "progs")
        best_program = min(progs, key=lambda x: x[1] * rec_len(x[0])) #weighing by length of program
        print(best_program, "best_program")
        progs.remove(best_program)
        
        #if best program has no tbf, move on 
        if not(recursive_search(best_program[0], "tbf")):
            continue
        
        for i in range(len(grammar)):
            new_prog = copy.deepcopy(best_program[0])
            new_elem = get_grammar(grammar, i)
            new_prog = deep_replace(new_prog, "tbf", new_elem)
            # print(new_prog, "new_prog")
            
            new_prog_fills = try_random_fills(new_prog, grammar)
            # print(new_prog_fills, "new_prog_fills")
            
            closenesses = []
            for fill in new_prog_fills:
                # print(new_prog_fills, "new_prog_fills")
                results = [evaluate(fill, x) for x in inputs]
                c = closeness(results, targets)
                # print(c, "closeness")
                closenesses.append(c)
                
            
            # print(closenesses, "closenesses")
            
            rating = sum(closenesses) / len(closenesses)
            if rating == 0:
                return new_prog
            
            progs.append([new_prog, rating])
            
        
    
    
    
def recursive_search(expr, target):
    # print("recursive_search", expr, target)
    
    if not(isinstance(expr, list)):
        if expr == target:
            return True
        else:
            return False
    
    for i in expr:
        if i == target:
            return True
        elif isinstance(i, list):
            if recursive_search(i, target):
                return True
    return False

#just replaces first instance #TODO make smth better 
def deep_replace(expr, old, replacement):
    #note in place!!
    # print("deep replacing", expr, old, replacement)
    if not(isinstance(expr, list)):
        if expr == old:
            return replacement
        else:
            return expr
    
    for i, item in enumerate(expr):
        if item == old:
            expr[i] = replacement
            return expr
        elif isinstance(item, list):
            if recursive_search(item, old):
                deep_replace(item, old, replacement)
                return expr 
    return expr
    
    
def try_random_fills(prog, grammar, num_fills = 10, max_depth = 10):
    fills = []
    
    
    for i in range(num_fills):
        # print(fills)
        fill = copy.deepcopy(prog)
        
        depth = 0
        while recursive_search(fill, "tbf"):
            if depth < max_depth:
                new_elem = get_random_grammar(grammar)
                #shouldn't need this but 
                if isinstance(new_elem, list):
                    new_elem = new_elem.copy()
                # print(new_elem, "new_elem")
                fill = deep_replace(fill, "tbf", new_elem)
            else: #do x to make it stop
                fill = deep_replace(fill, "tbf", "x")
            depth += 1	
        
        fills.append(fill)
        
    return fills 
        
    

    
    
def closeness(results, targets):
    #metric is average difference 
    return sum([abs(results[i] - targets[i]) for i in range(len(results))]) / len(results)
    
    
    
if __name__ == "__main__":
    test_prog = ["*", "5", ["+", "tbf", "tbf"]]
    test_prog2 = ["+", "tbf", "tbf"]
    # print(deep_replace(test_prog, "tbf", "x"))
    
    inputs = [1, 2, 3, 4, 5]
    targets = [2, 4, 6, 8, 10]
    
    
    
    # print(try_random_fills(test_prog2, [1, 2, 3, 4, 5]))
    
    print(prob_search(inputs, targets, grammar))