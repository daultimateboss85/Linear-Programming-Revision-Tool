
import customtkinter as ctk

class Page(ctk.CTkFrame):
    """All pages inherit from this class"""
    def __init__(self,master,fg_color = "#EFEFE0",**kw):
        super().__init__(master,corner_radius=0,fg_color = fg_color,**kw)
        self.master = master
        
    def clear(self):
        for child in self.winfo_children():
            child.destroy()
            
class def_button(ctk.CTkButton):
    """All buttons inherit from this class"""
    def __init__(self,master,border_width=2,fg_color ="#EFEFE0", border_color="white",
                 hover_color="grey92",font=("Arial",11),text_color="#7A513A",text="Place_holder",**kw):
        super().__init__(master,border_width =border_width,border_color =border_color,hover_color = hover_color,
                         font=font,text_color = text_color,fg_color = fg_color, text = text,**kw)
        
class def_lbl(ctk.CTkLabel):
    """All labels will inherit from this class."""
    def __init__(self,master, fg_color ="#EFEFE0",text_color="#7A513A",font = ("Arial",20),**kw):
        super().__init__(master,fg_color=fg_color, text_color=text_color,font=font, **kw)

        
class Radio_group(Page):
    """Mini frame that holds multiple radiobuttons sharing same variable"""
    def __init__(self,master,number,options):
        super().__init__(master,)
        self.master = master
        self.variable = ctk.StringVar(self,"")
        
        self.rad_btns = []
        self.options = options
        
        for i in range(number):
            radio_button = ctk.CTkRadioButton(self,variable = self.variable, value = options[i],text = options[i],
                                             font = ("Arial",20), text_color="#7A513A" ,border_color = "white")
            
            radio_button.grid(row = i,column = 0,sticky = "w")
            

            self.rad_btns.append(radio_button)