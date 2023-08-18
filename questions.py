import random
from graph_nodes import Graph
from lines import lines as l
import numpy as np

class Graphing_question():
    def __init__(self, access_mode, nec_info):
        #access_modes - y-intercept,x-intercept,area to shade, click
        #nec_info is majorly a line 
        """
        Parameters
        ----------
        access_mode : STRING
            SUB AREA OF GRAPHING LINEAR PROGRAMMING PROBLEMS
        nec_info : ANY
            INFO NEEDED TO MAKE QUESTION
        
        part:int
            Phase of question- 1 x or y intercept ,2 - drawing and shading
        Returns
        -------
        None.

        """
        
        self.access_mode = access_mode
        self.nec_info = nec_info
        
        if self.access_mode =="area to shade":
            self.part = 2
        
        elif self.access_mode == "y-intercept" :
            self.part =1 
        
        elif self.access_mode == "x-intercept":
            self.part = 1
            
        if self.part:
            self.style = random.randint(0,1)
            
            
            self.question_stems = {"c":[f"What is the {access_mode} of the line {nec_info}?",
                          f"is the {access_mode} of the line {nec_info}"]}
            
            self.question_stem = self.question_stems["c"][self.style]
            
        
    def get_question(self, question_type, axes = None, lenaxis = None):
        self.question_type = question_type
       
        if question_type == "fill_blank":
            if self.access_mode == "y-intercept" :
                self.answer = self.nec_info.c
            elif self.access_mode == "x-intercept":
                self.answer = self.nec_info.xc
                
            elif self.access_mode == "area to shade":
                places, letters, correct = put_letters(self.nec_info, lenaxis, axes)
                
                self.answer = letters[places.index(correct)]
                
                #print(self.answer)
            return self,self.question_stem
        
        elif question_type == "MCQ":
            if self.part ==1:
                a = f"({self.nec_info.xc},0)"
                b = f"({self.nec_info.c},0)"
                c = f"(0,{self.nec_info.xc})"
                d = f"(0,{self.nec_info.c})"
                e = f"(0,0)"
                
                self.options = [a,b,c,d,e]
                if self.access_mode == "y-intercept":
                    self.answer = d
                elif self.access_mode == "x-intercept":
                    self.answer = a
                    
                return self,self.question_stem,self.options
            
            elif self.part == 2:
                places, letters, correct = put_letters(self.nec_info, lenaxis, axes)
                a,b = letters
                self.options = [a,b]
                self.answer = self.options[places.index(correct)]
                
                return self, self.question_stem,self.options
        
        elif question_type == "touch":
            self.question_stem = "Click on the part of graph that should be shaded out"
            return self, self.question_stem

def validate(equation,event):
    """function to validate where user clicks"""
    
    if equation.status == ">=":
        if (event.xdata * equation.x + event.ydata * equation.y) > equation.rhs:
            return "Wrong"
        else:
            return "CorrecT"
    
    elif equation.status == "<=":
        if event.xdata * equation.x + event.ydata * equation.y < equation.rhs:
            return "Wrong"
        else:
            return "CorrecT"  
                
def validates(equations,event):
    """Validates user click in feasible region"""
    for equation in equations:
        lhs = equation.x *event.xdata + equation.y * event.ydata 
        if equation.status == "<=":
            if lhs < equation.rhs:
                continue
            else:
                return False
        elif equation.status == ">=":
            if lhs > equation.rhs:
                continue
            else:
                return False
    return True

def suit_y(ob_func,entry, lenaxis):
    """Testing for a suitable yintercept for objective function"""
    #creating a new line and testing to see if c will be suitable
    
    equation = l(x = ob_func.x,y = ob_func.y,rhs =ob_func.test)
    if equation.m >0 :
        new_eq = l(equation.x,equation.y,entry)
        if lenaxis>new_eq.c > 0 or 0<new_eq.xc < lenaxis:
           hold = True 
        else:
           hold = False
        
    elif equation.m < 0:
        
        new_eq = l(equation.x,equation.y, entry)
        if new_eq.c > 0 and new_eq.output(lenaxis) < lenaxis:
            hold = True 
        else:
            hold = False
        
    elif equation.m == 0:
       
        if entry > 0 and entry < lenaxis:
            hold = True 
        else:
            hold = False
    
    elif equation.m == np.inf:
        if entry == "NA":
            hold = True 
        else:
            hold = False
    new_eq = l(equation.x,equation.y,entry)
    return hold, new_eq

from lines_for_lp import get_lineLP
from linprog import max_obj
import statistics as stats

def filter_cycles(cycles):
    """filters the cycles returning cycle with greatest number of nodes"""
    lengths = [len(cycle) for cycle in cycles]
    for cycle in cycles:
        if len(cycle) == max(lengths):
            return cycle

def lp_question(lines, cycles):
    """
    Parameters
    ----------
    lines : List
        has lines that form LP problem
    nodes : List
        has nodes that form cycle on graph
        
    Returns
    -------
    lines : list
        lines have been given inequality symbols
    cop_nodes : list containing vertices of feasible region
    """
    nodes = filter_cycles(cycles)
   
    xs = [node.x for node in nodes] #xcoordinate of all nodes
    ys = [node.y for node in nodes] #ycoordinate of all nodes
    
    xbar = stats.mean(xs) #mean xcoordinate
    ybar = stats.mean(ys) #mean ycoordinate
    
    ytests = [line.output(xbar) for line in lines] #y value of lines at xbar
    
    for ytest ,line in zip(ytests,lines):
        if ytest == "NA": #for lines such as x = blah
   
             if xbar < line.rhs:
                 line.status = "<="
                 
             elif xbar > line.rhs:
                 line.status = ">="
        #set inequality of line based on comaprison with ybar
        elif ybar < ytest:
            line.status = "<="
        elif ybar > ytest:
            line.status = ">="
    
    #also want to get the nodes that form feasible region need to filter nodes that form cycle to those in feasible region
    cop_nodes = nodes[:]
    
    for node in nodes:
        for line in lines:
            if line.status == "<=":
                #another computer issue gave -59.6200000000000000005 when i wanted -59.62
                if round(node.x * line.x + node.y * line.y,10) > line.rhs:
                    cop_nodes.remove(node)
                    
            elif line.status == ">=":
                if round(node.x * line.x + node.y* line.y,10) < line.rhs:
                    cop_nodes.remove(node)
   
    return lines, cop_nodes

class LPquestion():
    """Linear programming Ineqaulties"""
    def __init__(self,num_of_lines,lenaxis):
#getting the lines
        cycles = None
#getting the nodes
#finding the cycles
        while not cycles:
            lines, x = get_lineLP(num_of_lines ,lenaxis)
            nodes = max_obj(lines, "get_nodes",(lenaxis,lenaxis))
            graph = Graph(nodes)
            A = graph.get_node((0,0))
            cycles = graph.find_cycles(A,[A])
            
        #equations that make the linear programming question
        self.equations, self.nodes = lp_question(lines, cycles)
        self.minimax = random.choice(("high","low"))
        
def put_letters(line, lenaxis, axes):
    """function to return points at which i can put letters i want """
    line = line
    lenaxis_tup = (lenaxis,lenaxis)
    if line.rhs == lenaxis:
        return None
    else:
        lines_add = [l(1,0,100),l(0,1,100), l(1,0,0),l(0,1,0)] 
        #putting in the boundaries
        lines_add.append(line)
        #getting nodes for graph
        nodes = max_obj(lines_add, "get_nodes", lenaxis = lenaxis_tup)
        
        graph = Graph(nodes)
        
        b = graph.get_node((0,100))
        
        new_cycles = []
        
        cycles = graph.find_cycles(b,[b]) # found cycles
        ###if the cycle contains node whose borders are the boundaries of the square remove it 
        
        for cycle in cycles:
            if  len(cycle) != len(nodes):
                new_cycles.append(cycle)
        #print(new_cycles)
    
        places = [] #places to put letters with correspoding letters
        #we've gotten new cycles
        if len(new_cycles) == 2:
           
        #want to recieve an axis and put letters at the centre of the cycles
            for cycle in new_cycles:#
                xs = [node.x for node in cycle] #xcoordinate of all nodes
                ys = [node.y for node in cycle] #ycoordinate of all nodes
                
                xbar = stats.mean(xs) #mean xcoordinate
                ybar = stats.mean(ys) #mean ycoordinate
                
                places.append((xbar,ybar))#places    
                
        correct = None
        for place in places:
            
            if line.status == ">=":
                if place[0] * line.x + place[1] * line.y < line.rhs:
                    correct = place
                   
            elif line.status == "<=":
                if place[0] * line.x + place[1] * line.y > line.rhs:
                    correct = place
            
        letters = ["A","B","C","D","E"]
        letters = letters[:len(places)]
        
        for letter, place in zip(letters, places):
            axes.text(place[0],place[1],letter)
            
        return places,letters, correct
        

