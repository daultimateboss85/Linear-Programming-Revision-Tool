

import customtkinter as ctk
from questions import LPquestion 
from freq_used import Page, def_button,def_lbl,Radio_group
import random        
from matplotlib .backends.backend_tkagg import(FigureCanvasTkAgg,NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from func_plot1 import plot ,empty_plot,plot_linobj
import numpy as np
from questions import Graphing_question, validate, validates,suit_y
from objective_line import get_objective_line
from lines_for_lp import get_lineLP

random.seed(543)
class Done_Section(Page):
    """Page showing user has completed a section"""
    def __init__(self,master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        message_lbl = def_lbl(self, text = "You have completed this section", font = ("Arial",40))
        message_lbl.grid(row = 0,column = 0)
        
        return_lbl = def_button(self, text = "return to Practice Page", command = lambda:self.master.show_page(Practice_Page))
        return_lbl.grid(row = 0, column = 0,sticky = "se")


class Home_Page(Page):
    """Home page- First one that will be seen"""
    def __init__(self,master):
        
        super().__init__(master)
  
        self.grid_columnconfigure(0, weight = 1)
        
        ##heading_frame ie frame that contains linear programming
        heading_frame = ctk.CTkFrame(self,height = 200, fg_color="#EFEFE0", border_width=2, border_color = "white")
        heading_frame.grid(row = 0, column = 0, sticky = "ew", padx = 50, pady = 90)
    
        heading_frame.grid_propagate(False)
        heading_frame.grid_columnconfigure(0, weight = 1)
        heading_frame.grid_rowconfigure(0, weight = 1)

        lbl_heading = ctk.CTkLabel(heading_frame,text = "LINEAR PROGRAMMING",fg_color ="#EFEFE0",font=("Arial",45, "bold"),
                                   text_color= "#7A513A")
        lbl_heading.grid(row=0,column = 0, pady = 20, sticky = "ew", padx = 10)
        
        ##lower frame
        
        lower_frame = ctk.CTkFrame(self,fg_color ="#EFEFE0", height = 150,)
        lower_frame.grid(row = 1,column = 0, sticky = "ew", padx = 50,pady = 50)
    
        lower_frame.grid_columnconfigure(0, weight = 1)
        
        ##buttons
        #practice button
        self.practice_button = def_button(lower_frame, text = "Practice",border_width= 2,font=("Arial",40), width = 300, 
                                          height = 100,
                                          command = lambda:self.master.show_page(Practice_Page))
        
        self.practice_button.grid(row = 0,column = 0,pady = 10, sticky = "nse")

        #revision button
        self.revision_button = def_button(lower_frame, text = "Revision", border_width= 2,font=("Arial",40), width = 300, height = 100)
        
        self.revision_button.grid(row = 0, column = 0,pady =10, sticky = "nsw")
        
class Practice_Page(Page):
    """Page shown after Practice button is clicked"""
    def __init__(self,master):
         super().__init__(master)
         
         
         self.grid_columnconfigure(1, weight = 1)
         self.grid_rowconfigure(1, weight = 1)


         self.gen_revision_btn = def_button(self,text = "General Revision", font= ("Arial",65))       
         self.gen_revision_btn.grid(row = 1,column = 1)
         

         self.sol_vertex_btn = def_button(self,text = "Solutions via vertex method",font= ("Arial",25),anchor  = "centre",
                                          command = lambda: self.master.show_page(Sol_vertex))
         self.sol_vertex_btn.grid(row = 1, column =0, sticky = "w")
         
        
         self.forming_lp_btn = def_button(self,text = "Formulating a LP problem",font = ("Arial",25))
         self.forming_lp_btn.grid(row = 0,column = 1,sticky = "s")
         
         self.graphing_lp_btn = def_button(self,text = "Graphing a LP problem",font = ("Arial",25),
                                           command = lambda: self.master.show_page(Graphing))
         self.graphing_lp_btn.grid(row = 1, column = 2)
         
         self.objective_line_btn = def_button(self, text = "Solutions via objective line",font = ("Arial",25),
                                              command = lambda:self.master.show_page(Sol_obj))
         self.objective_line_btn.grid(row = 2, column = 1,sticky = "n")
        
class Main(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color= "#EFEFE0")
        
        self.question = None
        
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        
        self.height *=0.75*0.75
        self.width *=0.75*0.75
        
        self.resizable(True,True)
        self.minsize(self.width,self.height)
        self.geometry(f"{self.width}x{self.height}")

        self.pages = {}
        
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight =1)

        self.graphing = 0 
        self.rest = 0
        for F in (Home_Page,Practice_Page, Graphing, Done_Section,Sol_obj, Sol_vertex): #pages dictionary will have Pages name as keys and page object as value
            frame = F(self)

            self.pages[F] = frame
        self.show_page(Home_Page)


    def show_page(self,New_Page):
        
        #ensuring graphing problems are done first
        if self.graphing or New_Page == Home_Page or New_Page == Practice_Page or New_Page ==  Graphing or New_Page == Done_Section or New_Page == Sol_obj or  New_Page == Sol_vertex:
            for page in self.pages.keys():
                self.pages[page].grid_remove() #remove all pages and put on new page
            
            if New_Page != Graphing or self.graphing == 0:
                self.pages[New_Page].grid(row =0, column = 0, sticky = "nsew",padx=20, pady = 20)
            
            #getting new graphing page as previous one will be solved already
            else:
                self.pages[Graphing] = Graphing(self)
                self.pages[Graphing].grid(row =0, column = 0, sticky = "nsew",padx=20, pady = 20)
        else:
            from tkinter import messagebox
            messagebox.showinfo("","Practice Graphing a LP problem first")
            print("Practice Graphing problems First")
       
    def replace_page(self,rep_Page):
        """repalce a page we have done"""
        new_page = rep_Page(self) 
        self.pages[rep_Page] = new_page
        
    def get_new_question(self):
        """get a new overhead question"""
        self.question = LPquestion(3, 100)

class Graphing(Page):
    """This page handles Graphing Linear Problems"""
    def __init__(self,master):
        super().__init__(master)
        
        self.question = LPquestion(3,100) #top level question
        self.master.question = self.question
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0 ,weight =1)

        #arranged them all this way to avoid changing row and column configure
        title = def_lbl(self,text = "Graphing a LP problem",font = ("Arial",40))
        title.grid(row = 0,column = 0,sticky = "n",pady = 25)
        
        #opening text displaying all the inequalities
        opening_text = "Lets Graph these inequalities:\n"
        for equation in self.question.equations:
            opening_text+= "\n" + equation.__str__()
        
        self.large_lbl = def_lbl(self,text = opening_text,font=("Arial",25))
        self.large_lbl.grid(row = 0, column =0) 
        
        go_btn = def_button(self,text = "Lets' GOOO",font = ("Arial",25), command =lambda: self.subroutine())
        go_btn.grid(row = 0, column = 0, sticky = "se",padx = 250,pady = 80)
        
        self.current = -1 #initialised to -1 so intial call will be 0 and so on 
        
    def subroutine(self):
        """Changing equations"""
        self.clear() #clear frame
        self.current += 1
         #current equation
        self.max_current = len(self.question.equations) #max number of equations
        
        if self.current != self.max_current: #there are still more equations to solve
            ##load new Page that has graph 
            new_page = Page_with_Graph(self,self.question.equations[self.current],100)
            new_page.grid(row = 0,column =0,sticky = "nsew")
        else:
            self.master.graphing +=1
            self.master.show_page(Done_Section)
            self.master.replace_page(Graphing)
            

class Page_with_Graph(Page):
    """This Page will be where users graph equations one by one"""
    
    def __init__(self,master,equation,end_x):
        ##all widgets here shouldnt change for current equation
        super().__init__(master,)#fg_color="white",border_color = "black",border_width = 2)
        #values intialised to 0
        self.yintercept = 0
        self.xintercept = 0
        self.areashade = 0
        
        self.equation = equation
        part1 = ("y-intercept","x-intercept","area to shade")
        
        self.generator = (element for element in  part1) #generator object - can invoke next() to bring up next part of question
        #when a user has gotten a part correct we get a new question using the next element from the generator

        self.grid_columnconfigure((0,1),weight = 1)
        self.grid_rowconfigure(1,weight = 1)
        #title at top
        title = def_lbl(self,text = "Graphing a LP problem",font = ("Arial",40))
        title.grid(row = 0,column = 0,sticky = "e", pady = 30) 
        
        #equation currently being worked on
        self.main_label = def_lbl(self,text = f"Graphing {equation}",font = ("Arial",30,"underline"))
        self.main_label.grid(row =1,column = 0,sticky = "nw")
        
        self.x = np.arange(0,end_x+1) #end of x-axis
        self.lenaxis = end_x
        self.graph_frame = ctk.CTkFrame(self,fg_color ="#EFEFE0") #frame that will hold graph
        self.graph_frame.grid(row =1,column = 1)
        
        self.fig, self.axes = empty_plot(self.x)
       
        self.axes.grid()
        
        self.graph_canvas = FigureCanvasTkAgg(self.fig,self.graph_frame)
        self.graph_canvas.get_tk_widget().grid(row=0,column = 0, sticky = "e")
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas,self.graph_frame,pack_toolbar=False)
        self.toolbar.grid(row=1, column = 0)
        
        self.question_frame = Page(self)#,fg_color = "grey")
        #contents of this frame changes based on question part
        self.question_frame.grid(row = 1,column = 0,sticky = "nsew",pady= 100)
        self.question_frame.grid_columnconfigure(0, weight = 1)
        self.question_frame.grid_rowconfigure((0,1)
                                              ,weight = 1)
        
        self.refresh()
    
    def refresh(self):
        #putting dots at x and y intercept when done by user
        if self.yintercept and self.equation.c: #if the line has a yintercept
            c1 = plt.Circle([0,self.equation.c],radius = 1,picker = True, color = "black")
            self.axes.add_artist(c1)
            self.graph_canvas.draw()
        if self.xintercept and self.equation.xc:
            c1 = plt.Circle([self.equation.xc,0],radius = 1,picker = True, color = "black")
            self.axes.add_artist(c1)        
        
        if self.yintercept and self.xintercept:
            
            plot(self.equation,self.x,self.axes,self.graph_canvas)
            
            self.graph_canvas.draw()
        self.question_frame.clear() #clear the question frame new question will be put in here
        
        question_types = ["fill_blank","MCQ",]
        question_types1 = ["fill_blank","MCQ","touch"]
        
        try: 
            #access mode of the question would be the next element from the generator
            self.access_mode = next(self.generator)
            
            #including touch type questions for area to shade questions
            self.question_type = random.choice(question_types) if self.access_mode != "area to shade" else random.choice(question_types1)
            if self.equation.rhs == self.lenaxis or self.equation.x==1 and self.equation.y ==1 and self.equation.rhs == self.lenaxis:
                if self.access_mode == "area to shade":
                    self.question_type = "touch"
                               
            elif (self.equation.c ==  None or self.equation.xc == None) and self.access_mode == "area to shade":
                self.question_type = "touch"

            if self.question_type == "fill_blank": #should try to optimize this more
                
                self.question_obj,self.question_text, = Graphing_question(self.access_mode,nec_info= self.equation).get_question(self.question_type,axes = self.axes,lenaxis = self.lenaxis) #question object,question prompt
    
                self.entry = ctk.CTkEntry(self.question_frame)
                
                if self.question_obj.style == 1: # ____ is the blah blahblah - entry before
                    #entry widget for user answer
                    self.entry.grid(row=0,column=0,sticky = "nw")
                    #question stem
                    self.question_lbl = def_lbl(self.question_frame,text = self.question_text)
                    self.question_lbl.grid(row=0,column = 0,sticky = "n" ,padx = 20)
                    
                elif self.question_obj.style == 0: # what is the blah blah blah --entry is after
                    self.entry.grid(row = 0,column = 0,sticky = "ne",padx = 70)
                    self.question_lbl = def_lbl(self.question_frame,text = self.question_text)
                    self.question_lbl.grid(row=0,column = 0,sticky = "nw" )
                    
            elif self.question_type == "MCQ":
                self.question_obj,self.question_text,self.options = Graphing_question(self.access_mode, self.equation).get_question(self.question_type,axes=self.axes,lenaxis=self.lenaxis) #question object,question prompt, options
                
                #question stem
                self.question_lbl = def_lbl(self.question_frame,text = self.question_text)
                self.question_lbl.grid(row=0,column = 0,sticky = "nw")
                
                self.radio_group = Radio_group(self.question_frame,len(self.options), self.options) #radio buttons
                self.radio_group.grid(row = 0, column = 0,sticky = "w")
                    
            elif self.question_type == "touch":
                self.question_obj,self.question_text = Graphing_question(self.access_mode, self.equation).get_question(self.question_type) #question object,question prompt, options
                self.question_lbl = def_lbl(self.question_frame,text = self.question_text)
                self.question_lbl.grid(row=0,column = 0,sticky = "nw")
              
                self.cidpress = self.graph_canvas.mpl_connect("button_press_event", self.submit)

             #submit , next part, next equation button
            self.next_button = def_button(self,text = "Submit",command =self.submit)
            self.next_button.grid(row = 2,column = 1)
            self.graph_canvas.draw()
        except StopIteration: 
            #all elements in generator have been used up ==> we are done with all parts of equation
            plot_linobj([self.equation], self.x, self.axes)
            #self.axes.legend()
            self.graph_canvas.draw()
            #configure the button to move on to next equation
            self.next_button.configure(command= self.master.subroutine,text = "Next Equation")
            
    def submit(self,event = None):
        """Validating user entry regardless of question type"""
        ###we need to deal with value errors
        
        # if dealing with x intercept or y intercept part is 1 
        try:
            if self.question_type == "fill_blank":
                self.user_entry = self.entry.get() #get user input
                
                if self.question_obj.part ==1: #we are dealing with x or y intercept
                
                    if self.equation.m != 0 and self.equation.m != np.inf:
                        if float(self.user_entry) == self.question_obj.answer: #compare float with answer
                            print("CorrecT") 
                            correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                            correct.grid(row = 2,column = 0, sticky = "ew")
                            #set part of question done to 1
                            if self.access_mode == "y-intercept":
                                self.yintercept = 1 
                                
                            elif self.access_mode == "x-intercept":
                                 self.xintercept = 1
                            
                            self.next_button.configure(command = self.refresh,text = "Next Part") #go to next part if correct
                            
                        else:
                            print("Wrong")
                            wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                            wrong.grid(row = 2,column = 0, sticky = "ew")
                    
                    elif self.equation.m == np.inf:
                        if self.access_mode  == "y-intercept":
                            if self.user_entry == "NA":
                                print("CorrecT")
                                self.next_button.configure(command = self.refresh,text = "Next Part") #go to next part if correct
                                self.yintercept =1
                                correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                                correct.grid(row = 2,column = 0, sticky = "ew")
                            else:
                                print("Wrong")
                                wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                                wrong.grid(row = 2,column = 0, sticky = "ew")
                                
                        elif self.access_mode == "x-intercept":
                            if float(self.user_entry) == self.question_obj.answer: #compare float with answer
                                print("CorrecT") 
                                correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                                correct.grid(row = 2,column = 0, sticky = "ew")
                                self.xintercept = 1
                                self.next_button.configure(command = self.refresh,text = "Next Part") #go to next part if correct
                                
                            else:
                                print("Wrong")
                                wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                                wrong.grid(row = 2,column = 0, sticky = "ew")
                        
                    elif self.equation.m == 0:
                        if self.access_mode == "x-intercept":
                            if self.user_entry == "NA":
                                print("Correct")
                                correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                                correct.grid(row = 2,column = 0, sticky = "ew")
                                self.xintercept = 1
                                self.next_button.configure(command = self.refresh,text = "Next Part") #go to next part if correct   
                            else:
                                print("Wrong")  
                                wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                                wrong.grid(row = 2,column = 0, sticky = "ew")
                                
                        elif self.access_mode=="y-intercept":
                            if float(self.user_entry) == self.question_obj.answer: #compare float with answer
                                print("CorrecT") 
                                correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                                correct.grid(row = 2,column = 0, sticky = "ew")
                                self.yintercept = 1
                                self.next_button.configure(command = self.refresh,text = "Next Part") #go to next part if correct
                                
                            else:
                                print("Wrong")
                                wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                                wrong.grid(row = 2,column = 0, sticky = "ew")
    
                elif self.question_obj.part == 2:
                    if self.user_entry == self.question_obj.answer:
                        print("CorrecT")
                        correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                        correct.grid(row = 2,column = 0, sticky = "ew")
                        self.areashade = 1
                        
                        self.next_button.configure(command = self.refresh,text = "Next Part") #go to next part if correct
                    
                    else:
                        print("Wrong")
                        wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                        wrong.grid(row = 2,column = 0, sticky = "ew")
            elif self.question_type == "MCQ":
                self.user_entry = self.radio_group.variable.get() #get option chosen by user
    
                if self.user_entry == self.question_obj.answer:
                    print("CorrecT")
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                    if self.access_mode == "y-intercept":
                        self.yintercept = 1
                    elif self.access_mode == "x-intercept":
                         self.xintercept = 1
                    elif self.access_mode == "area to shade":
                        self.areashade = 1
                   
                    self.next_button.configure(command = self.refresh,text = "Next Part")# go to next part if correct
                else:
                    print("Wrong")
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")
            elif event.xdata and event.ydata: #means graph was clicked- an area to shade question
                
                test  = validate(self.equation,event)
                if test == "CorrecT":
                    print("CorrecT")
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                    self.graph_canvas.mpl_disconnect(self.cidpress)
                    self.next_button.configure(command = self.refresh,text = "Next Part")# go to next part if correct
                else:
                    print("Wrong")
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")
        
        except ValueError:
            invalid = def_lbl(self.question_frame, text = "Invalid input!", font = ("Arial",30))
            invalid.grid(row = 2,column = 0, sticky = "ew")
            print("Invalid input")

class Sol_obj(Page):
    def __init__(self,master):
       
        super().__init__(master)
        self.minimax = self.master.question.minimax
        print(self.minimax)
        #text when describing if problem should be minimized or maximized
        self.minimax_text = "Maximize" if self.minimax == "high" else "Minimize"
        self.grid_columnconfigure((0,1), weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.equations = self.master.question.equations
        
        #question frame changes while user interacts
        self.question_frame = Page(self)
        self.question_frame.grid(row = 2,column = 0,sticky = "nsew")
        
        self.question_frame.grid_rowconfigure((0,2), weight = 1)
        self.question_frame.grid_columnconfigure(0, weight = 1)
      
        end_x = 100
        #title
        title = def_lbl(self, text = "Solution using objective line",font = ("Arial",40))
        title.grid(row = 0,column = 0, pady = 25,sticky = "n")
        
        self.x = np.arange(0,end_x+1) #end of x-axis
        self.lenaxis = end_x
        self.graph_frame = Page(self) #frame that will hold graph
        self.graph_frame.grid(row =2,column = 1 )
        
        #graph 
        self.fig, self.axes = empty_plot(self.x)
        plot_linobj(self.master.question.equations, self.x,ax=self.axes)
        self.axes.grid()
        #self.axes.get_legend().remove()
        self.graph_canvas = FigureCanvasTkAgg(self.fig,self.graph_frame)
        self.graph_canvas.get_tk_widget().grid(row=0,column = 0, sticky = "e")
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas,self.graph_frame,pack_toolbar=False)
        self.toolbar.grid(row=1, column = 0)
        
        #objective function        
        self.obj_line = get_lineLP(1,self.lenaxis, objective = True)

        m_lists = [line.m for line in self.equations]
        
        #to ensure objectve line is not parallel to any lines
        while self.obj_line.m in m_lists:
            self.obj_line = get_lineLP(1, self.lenaxis, objective = True)

        #opening text displaying all the inequalities
        opening_text = f"Lets {self.minimax_text} {self.obj_line} subject to these inequalities:\n"
        for equation in self.equations:
            opening_text+= "\n" + equation.__str__()
            
        #lbl for opening text 
        open_lbl = def_lbl(self.question_frame, text = opening_text)
        open_lbl.grid(row =0, column = 0, sticky = "n", pady = 90)
        
        over_head_text = def_lbl(self, text = f"{self.minimax_text} {self.obj_line}")
        over_head_text.grid(row =1, column = 0 )
     
        #next_button
        self.next_button = def_button(self, text = "Let's Gooo", command = self.refresh)
        self.next_button.grid(row = 3, column = 1)
        
       
        self.graph_canvas.draw()
        
        #stages of questioning
        stages = ["id_region","suit_y","shift_obj", "get_point"]
        self.stages = (stage for stage in stages)
        
    def refresh(self):
        
        self.next_button.configure(text = "Find the region",command = None)
        try:
            self.stage = next(self.stages)
            self.question_frame.clear()
            # identify the feasible region
            if self.stage == "id_region":
                self.cid_press = self.graph_canvas.mpl_connect("button_press_event", self.check)
                text = def_lbl(self.question_frame, text = "Click on the feasible region")
                text.grid(row = 0, column = 0, sticky = "n", pady = 90)
              
            #choose a suitable y intercept:
            elif self.stage == "suit_y":
                text = def_lbl(self.question_frame, text = f"The objective function is {self.obj_line.__str__()}.\nSuggest a suitable value for the y intercept of the objective function", )#justify = "left")
                text.grid(row = 0, column =0, sticky = "nw",pady = 90)
                
                self.entry = ctk.CTkEntry(self.question_frame)
                self.entry.grid(row = 0,column = 0, sticky = "ne", pady = 95, padx = 30)
                self.next_button.configure(text = "Submit",command = self.check)
            
            #shift objective until feasible region is reached
            elif self.stage == "shift_obj":
                text = def_lbl(self.question_frame, text = f"Drag the objective function until Optimum solution is reached")
                text.grid(row = 0, column = 0, sticky = "n", pady = 90)
          
                self.objective_function = get_objective_line(self.equations, self.x, self.axes, self.lenaxis, chosen = self.obj_line, minimax= self.minimax)
                self.objective_function.connect()
                
                self.axes.legend()
                self.graph_canvas.draw()
                self.next_button.configure(text = "Submit",command = self.check)
                
            elif self.stage == "get_point":
                text = def_lbl(self.question_frame, text = f"What are the coordinates of the optimal solution\n(xcoordinate,ycoordinate)?")
                text.grid(row = 0,column = 0, sticky = "n", pady = 90)
                
                self.entry  = ctk.CTkEntry(self.question_frame)
                self.entry.grid(row = 0, column = 1, sticky = "ne", pady= 90, padx = 30)
                
                self.next_button.configure(text = "Submit",command = self.check)
                
        except StopIteration:
            self.master.get_new_question()
            
            self.master.show_page(Done_Section)
            self.master.replace_page(Sol_obj)
            print("We done now")

    def check(self, event = None):
        try:
        #identify feasible region check
            if self.stage == "id_region":
                if event.xdata and event.ydata:
                    if validates(self.equations,event):
                        print("True")
                        correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                        correct.grid(row = 2,column = 0, sticky = "ew")
                        self.graph_canvas.mpl_disconnect(self.cid_press)
                        self.next_button.configure(text ="Next", command = self.refresh)
                    else:
                        print("False")
                        wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                        wrong.grid(row = 2,column = 0, sticky = "ew")
                        self.next_button.configure(text ="you shall not pass", command = None)
            
            #identify suitable y check
            if self.stage == "suit_y":
                entry = float(self.entry.get())
                state, new = suit_y(self.obj_line, entry, self.lenaxis)
               
                if state:
                    print("State",state)
                    self.obj_line = new
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                    self.next_button.configure(text ="Next", command = self.refresh)
                
                else:
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")
            #shift objecitve line until solution
            if self.stage == "shift_obj":  
                #we want to stop when we hit  optimum solution
                #line is essentially changing while being shifted
                #in short extrapolate new line made and see if the optimum solution will be on it if so disconnect
                place_to_stop = self.objective_function.optimum_x_y[1] - np.interp(self.objective_function.optimum_x_y[0], self.objective_function.line2d.get_xdata(),self.objective_function.line2d.get_ydata())
                if  -1< place_to_stop <1:#making solution more robust
                    self.objective_function.disconnect()
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                    self.next_button.configure(text ="Next", command = self.refresh)
                else:
                    print("Not there yet")
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")
            
            if self.stage == "get_point":
                #input should be in form (xcoord,ycoord)
                entry = self.entry.get()
                xcoordlist,ycoordlist = entry.split(",")
                
                #getting the x and y coordinate from entry in order to compare with answer
                #could compare entire string but then id have to specify decimal places and it will result in 0.000
                xcoord = float(xcoordlist.split("(")[1])
                ycoord = float(ycoordlist.split(")")[0])
                
                if xcoord == float(f"{self.objective_function.optimum_x_y[0]:.3f}") and ycoord == float(f"{self.objective_function.optimum_x_y[1]:.3f}"):
                    print("I'm him")
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                    self.next_button.configure(text ="Next", command = self.refresh)

                else:
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")

        except ValueError:
            print("Invalid input")
            invalid = def_lbl(self.question_frame, text = "Invalid input!", font = ("Arial",30))
            invalid.grid(row = 2,column = 0, sticky = "ew")
        
def change_string_tup(string):
    """Change string match from user input to tuple"""
    
    xcoordlist,ycoordlist = string.split(",")
    #getting the x and y coordinate from entry in order to compare with answer
    xcoord = float(xcoordlist.split("(")[1])
    ycoord = float(ycoordlist.split(")")[0])
    
    return (xcoord,ycoord)       

from linprog import max_obj
class Sol_vertex(Page):
    def __init__(self,master):
        super().__init__(master)
        
        self.minimax = self.master.question.minimax
        print(self.minimax)
        #text when describing if problem should be minimized or maximized
        self.minimax_text = "Maximize" if self.minimax == "high" else "Minimize"
        self.grid_columnconfigure((0,1), weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.equations = self.master.question.equations
        
        #question frame changes while user interacts
        self.question_frame = Page(self)
        self.question_frame.grid(row = 2,column = 0,sticky = "nsew")
        
        self.question_frame.grid_rowconfigure((0,2), weight = 1)
        self.question_frame.grid_columnconfigure(0, weight = 1)
      
        #title
        title = def_lbl(self, text = "Solution using Vertex method",font = ("Arial",40))
        title.grid(row = 0,column = 0, pady = 25,sticky = "n")
               
        end_x = 100
        
        self.x = np.arange(0,end_x+1) #end of x-axis
        self.lenaxis = end_x
        self.graph_frame = Page(self) #frame that will hold graph
        self.graph_frame.grid(row =2,column = 1 )
        
        #graph 
        self.fig, self.axes = empty_plot(self.x)
        plot_linobj(self.master.question.equations, self.x,ax=self.axes)
        self.axes.grid()
        #self.axes.get_legend().remove()
        self.graph_canvas = FigureCanvasTkAgg(self.fig,self.graph_frame)
        self.graph_canvas.get_tk_widget().grid(row=0,column = 0, sticky = "e")
        self.toolbar = NavigationToolbar2Tk(self.graph_canvas,self.graph_frame,pack_toolbar=False)
        self.toolbar.grid(row=1, column = 0)
        
        #objective function        
        self.obj_line = get_lineLP(1,self.lenaxis, objective = True)

        m_lists = [line.m for line in self.equations]
        
        #to ensure objectve line is not parallel to any lines
        while self.obj_line.m in m_lists:
            self.obj_line = get_lineLP(1, self.lenaxis, objective = True)
            
        self.opt_solution,_,_ = max_obj(self.equations, self.master.question.minimax,lenaxis = self.lenaxis,objective=self.obj_line) #optimum solution
        #opening text displaying all the inequalities
        opening_text = f"Lets {self.minimax_text} {self.obj_line} subject to these inequalities:\n"
        for equation in self.equations:
            opening_text+= "\n" + equation.__str__()
            
        #lbl for opening text 
        open_lbl = def_lbl(self.question_frame, text = opening_text)
        open_lbl.grid(row =0, column = 0, sticky = "n", pady = 75)
        
        over_head_text = def_lbl(self, text = f"{self.minimax_text} {self.obj_line}")
        over_head_text.grid(row =1, column = 0 )
     
        #next_button
        self.next_button = def_button(self, text = "Let's Gooo", command = self.refresh)
        self.next_button.grid(row = 3, column = 1)
        
        self.graph_canvas.draw()
        
        stages = ["id_region","get_coordinates","obtain_opt"]
        self.stages = (stage for stage in stages)
        
        
    def refresh(self):
        self.next_button.configure(text = "Find the region",command = None)
        try:
            self.stage = next(self.stages)
            self.question_frame.clear()
            # identify the feasible region
            if self.stage == "id_region":
                self.cid_press = self.graph_canvas.mpl_connect("button_press_event", self.check)
                text = def_lbl(self.question_frame, text = "Click on the feasible region")
                text.grid(row = 0, column = 0, sticky = "n", pady = 75)
              
            elif self.stage == "get_coordinates":
                self.question_frame.grid_rowconfigure(0, weight = 0)
                text = def_lbl(self.question_frame, text = f"Write out the coordinates of the vertices of the feasible region\n(xcoordinate,ycoordinate), suggest splitting over multiple lines")
                text.grid(row = 0,column = 0, sticky= "n",pady = 20 )
                self.question_frame.grid_rowconfigure(1, weight = 1)
      
                self.text_box = ctk.CTkTextbox(self.question_frame)
                self.text_box.grid(row = 1,column = 0, sticky = "nsew" ,padx = 20)
                
                self.next_button.configure(text = "Submit",command = self.check)
                
            elif self.stage == "obtain_opt":
                text = def_lbl(self.question_frame, text = f"What is the optimal solution")
                text.grid(row = 0,column = 0, sticky = "n", pady = 75)
                
                self.entry  = ctk.CTkEntry(self.question_frame)
                self.entry.grid(row = 0, column = 1, sticky = "nw", pady= 75, padx = 30)
                
                self.next_button.configure(text = "Submit",command = self.check)
                
        except StopIteration:
            self.master.get_new_question()
            self.master.show_page(Done_Section)
            self.master.replace_page(Sol_vertex)
            print("We done now")
    
    def check(self, event = None):
        try:
        #identify feasible region check
            if self.stage == "id_region":
                if event.xdata and event.ydata:
                    if validates(self.equations,event):
                        print("True")
                        correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                        correct.grid(row = 2,column = 0, sticky = "ew")
                        self.graph_canvas.mpl_disconnect(self.cid_press)
                        self.next_button.configure(text ="Next", command = self.refresh)
                    else:
                        print("False")
                        wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                        wrong.grid(row = 2,column = 0, sticky = "ew")
                        self.next_button.configure(text ="you shall not pass", command = None)
                        
            elif self.stage == "get_coordinates":

                nodes = self.master.question.nodes
                vertex_list = [(round(node.x,3),round(node.y,3)) for node in nodes]
                
                print(vertex_list)
                
                answer_text = self.text_box.get("0.0","end")
                print(answer_text)
                
                from re import findall
                #regex to find coordinates from user input
                pattern = r"\( *\d+\.?\d{0,3} *, *\d+\.?\d{0,3} *\)"
                
                user_answers = findall(pattern,answer_text)
                new_user_answers = [change_string_tup(answer) for answer in user_answers]
                print(user_answers)
                print(new_user_answers)
                if len(user_answers) == len(vertex_list):
                    print("We can continue")
                else:
                    print("There are some you have not identified")
                
                if new_user_answers == vertex_list:
                    print("You got it man")
                    self.next_button.configure(text ="Next", command = self.refresh)
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                else:
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")
                    print("Check again!")
                    
            elif self.stage =="obtain_opt":
                answer = self.entry.get()
                print(self.opt_solution)
                if float(answer) == round(self.opt_solution,3):
                    print("Youve done it")
                    correct = def_lbl(self.question_frame, text = "Correct", font = ("Arial",30))
                    correct.grid(row = 2,column = 0, sticky = "ew")
                    self.next_button.configure(text ="Next", command = self.refresh)
                
                else:
                    wrong = def_lbl(self.question_frame, text = "Wrong", font = ("Arial",30))
                    wrong.grid(row = 2,column = 0, sticky = "ew")
                    
        except ValueError:
            invalid= def_lbl(self.question_frame, text = "Invalid input", font = ("Arial",30))
            invalid.grid(row = 2,column = 0, sticky = "ew")
            print("Invalid input")
            
app = Main()
app.mainloop()




        
        

        
            
