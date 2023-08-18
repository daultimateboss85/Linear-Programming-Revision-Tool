
from lines import Line2dcop
from  lines_for_lp import get_lineLP
from linprog import max_obj
from func_plot1 import plot_line
#class for objective line that can be moved to determine optimal solution

class DraggableLine(Line2dcop):
    def __init__(self,line2d,line, optimum_x_y,optimum_sol):

        self.optimum_sol = optimum_sol
       
        self.optimum_x_y  = optimum_x_y #coordinates of optimum solution
       
        Line2dcop.__init__(self,line2d,line) #self.Line2D = line2d, self.line = line
        self.press = None
                             
    def connect(self):
        """connect to all the events needed"""
        self.cidpress = self.line2d.figure.canvas.mpl_connect(
            "button_press_event", self.on_press)
        self.cidrelease = self.line2d.figure.canvas.mpl_connect(
            "button_release_event", self.on_release)
        self.cidmotion = self.line2d.figure.canvas.mpl_connect(
            "motion_notify_event", self.on_motion)
     
    def on_press(self,event):
        """Check whether the mouse is over line;if so store some data."""
        if event.inaxes != self.line2d.axes:
            return
        contains, attrd = self.line2d.contains(event) #checks to see if event happened in line
        if not contains:
            return 
        
        self.press =  (event.xdata, event.ydata) #where line was clicked
        
        
    def on_motion(self,event):
        
        """Move the line if the mouse is over line."""
        if self.press is None or event.inaxes != self.line2d.axes:
            return # if no event occurs in line or wrong axes return
        (xpress, ypress) = self.press
        dx = event.xdata - xpress #amount to shift line by in x direction
        dy = event.ydata - ypress #amount to shift line by in y direction

        #get line data and add or subtract from the line depending on dx and dy
        xdata = self.line2d.get_xdata()
       
        ydata = self.line2d.get_ydata()
       
        self.line2d.set_xdata(xdata + dx)
        self.line2d.set_ydata(ydata + dy)

        self.line2d.figure.canvas.draw()
        
        self.press = event.xdata, event.ydata #new press point to keep dx and dy constant

        # #we want to stop when we hit  optimum solution
        # #line is essentially changing while being shifted
        # #in short extrapolate new line made and see if the optimum solution will be on it if so disconnect
        # place_to_stop = self.optimum_x_y[1] - np.interp(self.optimum_x_y[0], self.line2d.get_xdata(),self.line2d.get_ydata())
        # if  -1< place_to_stop <1:#making solution more robust
        #     print("We are there")
        #     self.disconnect()
            

    def on_release(self, event):
        """Clear button press information"""
        self.press = None
        self.line2d.figure.canvas.draw()
        
    def disconnect(self):
        """Disconnect all callbacks"""
        self.line2d.figure.canvas.mpl_disconnect(self.cidpress)
        self.line2d.figure.canvas.mpl_disconnect(self.cidrelease)
        self.line2d.figure.canvas.mpl_disconnect(self.cidmotion)

       
def get_objective_line(question,x_range,axis,len_axis, chosen = None, minimax = None):
    """Function to return objecitve line"""
   
    if not chosen:
        line = get_lineLP(1,len_axis)
    else:
        line = chosen
    #maximizing objective function to constraints
    optimum_solution,optimum_intersection, optimum_x_y = max_obj(question,minimax,objective = line)

    optimum_x_y = list(optimum_x_y)
    #getting an objective line

    Line2Dcop = plot_line(line,x_range, axis,"objective line",objective = True)
  
    ob_line = DraggableLine(Line2Dcop,line, optimum_x_y,optimum_solution)
    ob_line.connect()

    return ob_line
