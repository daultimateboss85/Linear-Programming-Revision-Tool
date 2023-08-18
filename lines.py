import numpy as np
from matplotlib.lines import Line2D

#pretty self explanatory
#x, y , right hand side and status attribute
class lines(Line2D):
    valid_statuses = ["=","<=",">="]
    def __init__(self,x=0,y=0,rhs=0,status = "=", test = None):
        self.x = x
        self.y = y
        self.rhs = rhs

        self.status = status
        self.test = test
# going to use these to work around matplotlib fill_between

#need the value of gradient...
        if self.rhs == "O": #also need the value of gradient of objective function to ensure it isnt parallel to other inequalities
            if self.y == 0:
                self.m = np.inf
                
            else:
                self.m = -self.x/self.y
               
        else:
            if self.y == 0:
                self.m = np.inf
                self.c = None
            else:
                self.m = -self.x/self.y
                self.c = self.rhs/self.y
                
            if self.x != 0:
                self.xc = float(f"{self.rhs/self.x:.3f}")
                
            else:
                self.xc = None
            

    def output(self,x):
        #will mainly be used to generate inequalities by comparing mean value of nodes with value of line at that point
        #but also see what a lines y will be for a given x
        if self.y != 0:
            y  = (self.rhs - self.x * x)/self.y
            return y
        
        else:
            return "NA"
    
#function to print line im working with
#takes into account coefficent of x and y so i dont have 1x +...  or x + -4y.used logic gates making it way easier to follow
#also takes away 0 so dont have 0x + or 0y...
    def __str__(self):
        y = str(self.y)
        x = str(self.x)
#taking care of 0
        if x == "0" and y == "0":
            
            return ("Invalid line")
###
        elif x == "0" and y != "0":
            ###
            
            if y.strip("-") != "1": 
                if "-" not in y:
                    return  f"{y}y {self.status} {self.rhs}" 
                
                elif "-" in y:
                     return f"-{y.strip('-')}y {self.status} {self.rhs}" 
                    ####
            elif y.strip("-") == "1":            
                if "-" not in y:
                    return f"{y.strip('1')}y {self.status} {self.rhs}"
                
                elif "-" in y:
                     return f"-{y.strip('-1')}y {self.status}{self.rhs}"
                    
                
            elif y.strip("-") != "1":           
                if "-" not in y:
                    return f"{y}y {self.status} {self.rhs}"
                
                elif "-" in y:
                     return f"-{y.strip('-')}y {self.status} {self.rhs}"
                    
            elif y.strip("-") == "1":             
                if "-" not in y:
                    return f"{y.strip('1')}y {self.status} {self.rhs}"
                
                elif "-" in y:
                     return f"-{y.strip('-1')}y {self.status} {self.rhs}"
                    
###
        elif x != "0" and y == "0":
            
            if x.strip("-") != "1" : 
        
                    return f"{x}x {self.status} {self.rhs}"
                
                    ####
            elif x.strip("-") != "1":             
                    return f"{x}x {self.status} {self.rhs}"
             
            elif x.strip("-") == "1":            
                    return f"{x.strip('1')}x {self.status} {self.rhs}"

                    
            elif x.strip("-") == "1" :             

                    return f"{x.strip('1')}x {self.status} {self.rhs}"

####
        elif x != "0" and y != "0":
###taking care of 1's and -
            if x.strip("-") != "1" and y.strip("-") != "1": #0,0
                if "-" not in y:
                    return f"{x}x + {y}y {self.status} {self.rhs}"
                
                elif "-" in y:
                    return f"{x}x - {y.strip('-')}y {self.status} {self.rhs}"
                    ####
            elif x.strip("-") != "1" and y.strip("-") == "1":             #0,1
                if "-" not in y:
                    return f"{x}x + {y.strip('1')}y {self.status} {self.rhs}"
                
                elif "-" in y:
                    return f"{x}x - {y.strip('-1')}y {self.status} {self.rhs}"
                    
                
            elif x.strip("-") == "1" and y.strip("-") != "1":             #1,0
                if "-" not in y:
                    return f"{x.strip('1')}x + {y}y {self.status} {self.rhs}"
                
                elif "-" in y:
                    return f"{x.strip('1')}x - {y.strip('-')}y {self.status } {self.rhs}"
                    
            elif x.strip("-") == "1" and y.strip("-") == "1":             #1,1
                if "-" not in y:
                    return f"{x.strip('1')}x + {y.strip('1')}y {self.status} {self.rhs}"
                
                elif "-" in y:

                    return f"{x.strip('1')}x - {y.strip('-1')}y {self.status} {self.rhs}"
                    

            
    def __repr__(self):
        return self.__str__()

#if both are 0 print invalid line
#major logic is if either the y or x attribute is 0, dont print the variable that is 0
#as for the variables that arent 0, check if the coefficient is 1 if it is 1, remove the 1 and print only the variable
#for y variables also check if it is negative and deal with it
#finally if neither 0,1,or negative just print it how it is

                    
class Line2dcop(lines,Line2D):
    """Class inheriting from both matplotlib lines and my own lines"""
    def __init__(self,Line2d,line):
        Line2D.__init__(self,Line2d.get_xdata(),Line2d.get_ydata())
        lines.__init__(self,line.x,line.y,line.rhs)
        
        self.line2d = Line2d
        self.line = line


    

