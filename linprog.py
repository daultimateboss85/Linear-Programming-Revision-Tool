import numpy as np
from graph_nodes import Node

#function to solve two simultaneous equations
def simultaneous(line1,line2):
    a = np.array([line1.x,line1.y])
    b = np.array([line2.x,line2.y])
    
    lhs = np.array([a,b])
    rhs = np.array([line1.rhs, line2.rhs])

    try:
        solution = np.linalg.solve(lhs,rhs)
    
    #for lines that cant be solved simultaneously eg x = 10 and x = 80
    except np.linalg.LinAlgError:
        return None
    
    else:
        return solution
    
# recursive algorithm to bring total number of possible combinations from a list
def combinations(iterable):
    """recursive algorithm to bring total number of combinations from an iterable"""
    if len(iterable) == 0:        
        return[[]]

    combos = []
    for combo in combinations(iterable[1:]):
        combos += [combo, combo + [iterable[0]]]

    return combos

#receives an objective function and solutions from lines and returns solutions put in function
def max_obj(lines, minimax, lenaxis = None, objective= None):
    """Function that either get nodes for graph or maximises or minimises an objective function
    lines - lines to use
    minimax - mode ("high", "low", "get_nodes")
    lenaxis - length of axis (x,y)
    objective - function to be maximised
    """
    rows = combinations(lines)
    #filtering for those with only two lines
    rows = list(filter(lambda a: len(a) == 2,rows))   
    solutions = []
    new_rows = []
    #removing combinations of lines that dont give solutions 
    for row in rows:
        ans = simultaneous(row[0], row[1])
        #adding solutions of lines to solutions
        if type(ans) == np.ndarray: 
            new_rows.append(row)
            solutions.append(ans)
      
    rows = new_rows
   #putting corresponding values of objective using solutions into a list
    tests = []
    #defualt objective is none as for now im more often using this function to get the nodes
    if objective:
        for obj in solutions:
            sol = obj[0] * objective.x + obj[1] * objective.y
            tests.append(sol)         
    #going to use this function to also get the nodes from a graph
    #removing solutions not in axis from list dont want the user to be shifting the graph to find regions
    if minimax == "get_nodes":
        filtered_rows = [] #lines of intersections i need
        filtered_list = [] #solutions ill use for nodes
        gotten_nodes = [] #stores the nodes
        
        for i,solution in enumerate(solutions):
            if (solution[0] <= lenaxis[0]) and  (solution[1] <= lenaxis[1]) and solution[0] >= 0 and solution[1] >= 0:
              filtered_list.append(solution) #getting only nodes in range
              filtered_rows.append(rows[i]) #getting lines that make nodes
        
        for node, row  in zip(filtered_list,filtered_rows):
            gotten_nodes.append(Node(node,row)) #creating nodes based on solution and lines that make node

        return gotten_nodes     
        
    #trying to go for each sol:
    #for each line: if it doesnt satisfy it remove solution from solutions(removing answers that are not in the feasible region)
    elif minimax == "high":
        for i in range(len(tests)):
            for line in lines:
                
                    if line.status == "<=":
                        if round(solutions[i][0] * line.x + solutions[i][1] * line.y,10) > line.rhs:
                            
                            tests[i] = -np.inf
                            
                    elif line.status == ">=":
                        if round(solutions[i][0] * line.x + solutions[i][1] * line.y,10) < line.rhs:
                            tests[i] = -np.inf
                            
    #optimum things
        optimum_index = tests.index(max(tests))
        optimum_intersection = rows[optimum_index]
        optimum_solution = tests[optimum_index]
        optimum_x_and_y  = solutions[optimum_index]
       
        
    ## round bcuz of an error python gave me
    ## instead of evaluating 25 it did 24.99999999999999996 and that evaluated to false
    ## looked everywhere for the drop in accuracy but couldnt find it python or maybe my laptop just isnt smart enough
    elif minimax == "low":
        
        for i in range(len(tests)):
                
            for line in lines:
                if line.status == "<=":
                    if round(solutions[i][0] * line.x + solutions[i][1] * line.y,10) > line.rhs:
                        tests[i] = np.inf
                        
                        
                elif line.status == ">=":
                    if round(solutions[i][0] * line.x + solutions[i][1] * line.y,10) < line.rhs:
                        tests[i] = np.inf
                        
       
    #optimum things
        optimum_index = tests.index(min(tests))
        optimum_intersection = rows[optimum_index]
        optimum_solution = tests[optimum_index]
        optimum_x_and_y  = solutions[optimum_index]

    return optimum_solution,optimum_intersection,optimum_x_and_y




























