###module to generate lines for linear programming
from lines import lines as l
import numpy as np
import random

#first generate points
def generate_pointsline(x,number):
    """generate points for lines based on x axis
    A pair of points per number"""
    points = []
    for _ in range(number):
        point_oney = random.randrange(0,np.amax(x))
        point_onex = random.randrange(0,np.amax(x))

        point_twoy = random.randrange(0,np.amax(x))
        point_twox = random.randrange(0,np.amax(x))

        coordinates = [(point_onex,point_oney),(point_twox,point_twoy)]
        points.append(coordinates)
    
    return points

#using two points to draw a line
def drawtwopoints(point_one, point_two):
    """uses two points to draw a line"""
    l_onex, l_oney = point_one
    l_twox, l_twoy = point_two

    #y = mx + c
    try:
        m = (l_twoy-l_oney)/(l_twox-l_onex) 
        c =  l_twoy - m*l_twox
        line = l(round(-m,2),1,round(c,2))

        return line
        
    except ZeroDivisionError:#gradient of line is infinity line of form x = k
        m = 1 #coefficient of x is 1
        c =  l_twox #rhs is going to be x value 
        line = l(round(m,2),0,round(c,2))
        
    return line


#main function generating and returning lines for linear programming
def get_lineLP(num_lines,end_x,objective = None):
    """returns the lines to be plotted"""
    x = np.arange(0,end_x+1,10)
    if num_lines > 1: #then i need linear programming lines include y and x = 0
        
        points = generate_pointsline(x,num_lines)

        lines = [] #array of lines
    
        for point in points:
            line = drawtwopoints(point[0],point[1])
            lines.append(line)

        lines.extend([l(1,0,0),l(0,1,0)]) #adding x and y = 0 to lines
    
        return lines ,x

    elif num_lines ==1:
        #one objective line
        
        point = generate_pointsline(x,num_lines)[0]

        line = drawtwopoints(point[0],point[1])
        
        intercept_test = line.rhs
        
        if not objective:
            return line
        
        if objective:
            
            #objective function must not be x = blah or y = blah
            while line.m == np.inf or line.m == 0:
                line = drawtwopoints(point[0], point[1])
                intercept_test = line.rhs
                
            line = l(line.x,line.y,"O",test = intercept_test)
            return line
