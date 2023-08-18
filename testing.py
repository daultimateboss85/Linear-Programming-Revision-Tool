# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 23:24:57 2023

@author: judad
"""


from lines_for_lp import get_lineLP
# #Testing
# #1
# line = get_lineLP(num_lines = 1,  end_x = 100) #generate 1 line with domain ending at x = 100
# print(f"Test 1:{line}\n")

# #2
# lines,end_x = get_lineLP(num_lines = 5, end_x = 100)#generate 5 lines with domain ending at x=100
# print(f"Test 2:",end = " ")
# for line in lines:
#     print(line)
# print()

# #3
# print(f"Test 3:{l(x=2,y=2,rhs=100)}\n")

# #4
# print(f"Test 4:{l(x=-1,y=-1,rhs=100)}\n")

# #5
# print(f"Test 5:{l(x=0,y=1,rhs=100)}\n")

# #6 
# print(f"Test 6:{l(x=1,y=0,rhs=100)}\n")

# #7 
# print(f"Test 7:{l(x=100,y=100,rhs=1000)}\n")

# #8 
# print(f"Test 8:{l(x=2,y=2,rhs=100, status = '>=')}\n")

# #9 
# print(f"Test 9:{l(x=-1,y=-0,rhs=100, status = '>=')}\n")

# from lines import lines as l
# from func_plot1 import plot_linobj
 
# from linprog import max_obj 
# from graph_nodes import Graph
# l1 = l(1,3,500,"<=")
# l2 = l(3,1,500,"<=")
# l3 = l(5,4,1000,"<=")
# l4 = l(1,0,0,">=")
# l5 = l(0,1,0,">=")

# objective = l(1,1,0)

# lines = [l1,l2,l3,l4,l5]
 
# x =  np.arange(0,1001,10)

# plot_linobj(lines, x)


# nodes = max_obj(lines, minimax = "get_nodes",lenaxis = (100,100))
# print(nodes)

# graph = Graph(nodes)
# A = graph.get_node((0,0))
# cycles = graph.find_cycles(A, [A])

# from questions import lp_question
# equations = lp_question(lines, cycles)
# print(equations)

# optimalx,y,z = max_obj(lines, minimax = "low", lenaxis = (100,100) , objective= objective)

# random.seed(5)

# lines = [l(0,1,0),l(1,0,0),l(2,2,100),l(5,3,-23), l(3,1,60)]

# nodes = max_obj(lines,  minimax = "get_nodes", lenaxis =(100,100)) #nodes that will form graph

# graph = Graph(nodes)
# A = graph.get_node((0,0))#node to start traversal from

# cycles = graph.find_cycles(A, [A])

# from questions import lp_question

# inequalities, vertices = lp_question(lines = lines, cycles = cycles)


# fig, ax = empty_plot(x)
# plot_linobj(inequalities, x, ax= ax) #plot inequalities

# objective_function = get_objective_line(inequalities, x, axis = ax, len_axis = 100,minimax="high")
# print(objective_function)

# ax.legend()
#x = np.arange(0,101,10)
from graph_nodes import Graph
from objective_line import get_objective_line
import random
from linprog import max_obj

from func_plot1 import plot_linobj
from lines import lines as l
import numpy as np

#data wrangling 
l1 = l(1,3,500,"<=") #x + 3y <= 500
l2 = l(3,1,500,"<=")  # 3x + y <= 500
l3 = l(5,4,1000,"<=")

l4 = l(1,0,0,">=")
l5 = l(0,1,0,">=")

lines = [l1,l2,l3,l4,l5]

x = np.arange(0,511,10)

plot_linobj(lines, x) #plot the inequalities

























