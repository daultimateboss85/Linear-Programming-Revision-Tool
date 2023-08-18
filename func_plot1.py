
import matplotlib.pyplot as plt
import numpy as np
#making a line in terms of x
# if zerodivision error => gradient is infinity, return value of x as an array(solution done to workaround matplotlib limitations)


def in_terms_y(equation,x):
    try:
        y = -equation.x/equation.y*x + equation.rhs/equation.y
        return y
    except ZeroDivisionError:

        new_arr = np.array([])
        for i in range(len(x)):
            new_arr = np.append(new_arr,equation.rhs)
        return new_arr
    

#plots a set of lines on
#also shades regions


def plot_linobj(equations,x, ax = None):
    """Main function for plotting inequalities"""
    ready_plots = []
    if not ax:
        fig,ax = plt.subplots()#figsize = (5,5),#facecolor = "#EFEFE0")
       # ax.set_facecolor("#EFEFE0")
        
        for line in equations:
            
            y = in_terms_y(line,x) # create an array in terms of x (ie what we will plot)
            ready_plots.append(y) # append array to list
            
            
           
    # determining region to shade based on lines gradient attribute
    #if gradient is not infinity use fill_between
    #figured its because of intercept that determines side of line 0,0 lies
    #using that to determine where to shade
    
            if line.m != np.inf and line.m != 0:
                ax.plot(x,y,label = line.__str__(),picker = True) #plot line on graph, label will be string representation i defined in lines module
                
    
                test = line.y * 0 + line.x * 0 # new proposed. testing a value of in region then shading based on that
                
                
                if line.status == ">=":
                    if line.c > 0:
                        if test > line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
    
                        elif test < line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
    #nb we wont want lines that are >= with c < 0 
                    elif line.c < 0:
                        if test > line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
                        elif test < line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
                            
    # cant use 0,0 as a test for lines whose intercept is the origin
                    elif line.c == 0:
                        test = line.x * 1 + line.y * 0
                        
                        if test > line.rhs:
                            plt.fill_between(x,y,9999999,alpha = 0.2)
                            
                        elif test < line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
    ######
                elif line.status == "<=":
                    if line.c > 0:
                        if test < line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
    
                        elif test > line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
                    elif line.c < 0:
                        if test < line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
    
                        elif test > line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
                            
    #cant use 0,0 as a test for lines whose intercept is the origin                  
                    elif line.c == 0:
                        test = line.x * 1 + line.y * 0
                        
                        if test < line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
                            
                        elif test > line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
    
    ######
            elif line.m == 0:
                ax.plot(x,y,label = line.__str__(),picker = True) #plot line on graph, label will be string representation i defined in lines module
    
                if line.status == "<=":
                    ax.fill_between(x,y,9999999,alpha = 0.2)
    
                elif line.status == ">=":
                    ax.fill_between(x,y,-9999999,alpha = 0.2)
    
    
    ####
    #if gradient is infinity use fill_betweenx
            elif line.m == np.inf:
                
                ax.plot(y,x,label = line.__str__(),picker = True
                        ) #plot line on graph, label will be string representation i defined in lines module
    
                if line.status == ">=":
                    ax.fill_betweenx(x,y,-9999999,alpha = 0.2)
                elif line.status == "<=":
                    ax.fill_betweenx(x,y,9999999,alpha = 0.2)
                 
            
    #adding legend, setting axis (i should make a function to determine axis),showing graph
        
        ax.axis([-2,np.amax(x),-2,np.amax(x)])
        ax.grid()
        ax.legend()
       
        return fig
    elif ax:
        #fig,ax = plt.subplots(figsize = (5,5),facecolor = "#EFEFE0")
        #ax.set_facecolor("#EFEFE0")
        
        for line in equations:
            
            y = in_terms_y(line,x) # create an array in terms of x (ie what we will plot)
            ready_plots.append(y) # append array to list
            
            
           
    # determining region to shade based on lines gradient attribute
    #if gradient is not infinity use fill_between
    #figured its because of intercept that determines side of line 0,0 lies
    #using that to determine where to shade
    
            if line.m != np.inf and line.m != 0:
                ax.plot(x,y,label = line.__str__(),picker = True) #plot line on graph, label will be string representation i defined in lines module
                
    
                test = line.y * 0 + line.x * 0 # new proposed. testing a value of in region then shading based on that
                
                
                if line.status == ">=":
                    if line.c > 0:
                        if test > line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
    
                        elif test < line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
    #nb we wont want lines that are >= with c < 0 
                    elif line.c < 0:
                        if test > line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
                        elif test < line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
                            
    # cant use 0,0 as a test for lines whose intercept is the origin
                    elif line.c == 0:
                        test = line.x * 1 + line.y * 0
                        
                        if test > line.rhs:
                            plt.fill_between(x,y,9999999,alpha = 0.2)
                            
                        elif test < line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
    ######
                elif line.status == "<=":
                    if line.c > 0:
                        if test < line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
    
                        elif test > line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
                    elif line.c < 0:
                        if test < line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
    
                        elif test > line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
                            
    #cant use 0,0 as a test for lines whose intercept is the origin                  
                    elif line.c == 0:
                        test = line.x * 1 + line.y * 0
                        
                        if test < line.rhs:
                            ax.fill_between(x,y,9999999,alpha = 0.2)
                            
                        elif test > line.rhs:
                            ax.fill_between(x,y,alpha = 0.2)
                            
    
    ######
            elif line.m == 0:
                ax.plot(x,y,label = line.__str__(),picker = True) #plot line on graph, label will be string representation i defined in lines module
    
                if line.status == "<=":
                    ax.fill_between(x,y,9999999,alpha = 0.2)
    
                elif line.status == ">=":
                    ax.fill_between(x,y,-9999999,alpha = 0.2)
    
    
    ####
    #if gradient is infinity use fill_betweenx
            elif line.m == np.inf:
                
                ax.plot(y,x,label = line.__str__(),picker = True
                        ) #plot line on graph, label will be string representation i defined in lines module
    
                if line.status == ">=":
                    ax.fill_betweenx(x,y,-9999999,alpha = 0.2)
                elif line.status == "<=":
                    ax.fill_betweenx(x,y,9999999,alpha = 0.2)
                 
            
    #adding legend, setting axis (i should make a function to determine axis),showing graph
        
        ax.axis([-2,np.amax(x),-2,np.amax(x)])
        #ax.grid()
        ax.legend()
       


def plot_line(line, x, ax, label,objective=False):
    """ function majorly to return line with matplotlib properties"""
    new_x = np.arange(-(np.amax(x)*10),np.amax(x)*10,10)
    #px + qy = c
    if objective: #for objective line i want it to always be on screen so its length will be way longer
        y = in_terms_y(line,new_x)
    
    
    
    line = ax.plot(new_x,y, label = label)[0]
    return line

def plot(line,x,ax,canvas, ):
    """
    
    Function to just plot a single line
    Parameters
    ----------
    line : Line object
        DESCRIPTION.
    x : array of x points
        
    ax : axes
        axes to plot line on

    Returns
    -------
    None.

    """
    y = in_terms_y(line, x)
    

  
    if line.y == 0:
        ax.plot(y,x, )#label = line.__str__())
    
    else:
        ax.plot(x,y,) #label = line.__str__())
          
    canvas.draw()
    
def empty_plot(x):
    fig,ax = plt.subplots(figsize = (6,6),facecolor = "#EFEFE0")
    ax.set_facecolor("white")
    ax.axis([-2,np.amax(x),-2,np.amax(x)])
    return fig,ax
    
    


    
    
    
    
