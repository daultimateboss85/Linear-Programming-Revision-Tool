# -*Nodes Class*-
"""
Created on Thu Dec 29 11:38:41 2022

@author: judad
"""

class Node:
    def __init__(self,coordinate,lines):
        """
        Parameters
        ----------
        coordinate : Tuple
            Contains x and y coordinate for node to be placed on graph
        lines : Tuple
            Contains lines that intersected to get node
        """
        self.x = coordinate[0] #xcoordinate of node
        self.y = coordinate[1] #ycoordinate
        self.lines = lines #lines that intersect to form node
        self.neighbours = [] #list containing neighbouring nodes
        self.coming_from = [] #the node could be gotten from several ways 
          
        
    def add_neighbour(self,neighbour):
        """add a neighbouring node to a list of neighbouring nodes"""
        if neighbour not in self.neighbours:
            self.neighbours.append(node_neighbour(neighbour,(self.x,self.y)))
            
            
    def __str__(self):
        return f"Node({self.x},{self.y})"
        
    def __repr__(self):
        return f"{self.__str__()}\n"
    
    

class node_neighbour(Node):
    """i need some kind of weight function trying to use this to get over it"""
    #same as a node but this just carries extra weight :)
    def __init__(self,node,incoming):
        self.x = node.x
        self.y = node.y                                                                        
        self.lines = node.lines
        ##distance between the nodes is the weight
        #negative if neighbour is to the left of node or if neighbour is below node (if and only if line they lie on doesnt have changes in x)
        
        incoming_x,incoming_y = incoming
        
        self.edge_weight = ((incoming_x-self.x)**2 + (incoming_y-self.y)**2)**0.5
        
        if incoming_x > self.x:
            self.edge_weight = -self.edge_weight
        
        #deals with node that lie on a line x = blah
        elif incoming_x == self.x:
            if incoming_y > self.y :
                self.edge_weight = -self.edge_weight
        
    def __str__(self):
        return f"Neighbour({self.x},{self.y})"
            
    def __repr__(self):
        return f"Neighbour({self.__str__()})\n"
    

class Graph:
    def __init__(self,nodes):
        self.Nodes = nodes #nodes that make up graph
        
        #add neighbours between all nodes that have an intersection between lines attributes
        for node in self.Nodes: 
            for vert in self.Nodes:
                if node == vert:
                    continue #skip comparing yourself
                else:
                    if set(node.lines) & set(vert.lines):
                        node.add_neighbour(vert)
                        
        self.addedges()
    
    def addedges(self):
        """cuts neighbours to only those immediately to the left or right or above or below node"""
        
        for node in self.Nodes: #for each node
            new_neighbs = [] #new neighbours without others
            for line in node.lines: #for each line the node is a part of
                
                #positive weighted for to the left and above and vice-versa
                pos_weights = [] 
                pos_neighbs = []
                neg_weights = []
                neg_neighbs = []
                
                for vertex in node.neighbours: #for each neighbouring node
                    if line in vertex.lines: #if i have the intial line 
                
                        #check the weights and determine if weight is positive or negative
                        if vertex.edge_weight > 0:
                            pos_neighbs.append(vertex)
                            pos_weights.append(vertex.edge_weight)
                        elif vertex.edge_weight < 0:
                            neg_neighbs.append(vertex)
                            neg_weights.append(vertex.edge_weight)
                
                #node to left or above will be node with minimum positive weight and vice
                min_pos = min(pos_weights) if pos_weights else None
                min_neg = max(neg_weights) if neg_weights else None
                
                right_node = None #restarting them
                left_node = None
                
                #find the min_pos node and min_neg node and call them right node and left node respectively
                for good_node in pos_neighbs:
                    if good_node.edge_weight ==min_pos:
                        right_node = good_node
                  
                for other_good_node in neg_neighbs:
                    if other_good_node.edge_weight == min_neg:
                        left_node = other_good_node
                
                new_neighbs.append(right_node) if right_node else None
                new_neighbs.append(left_node) if left_node else None
                
            #giving the node new neighbours
            node.neighbours = new_neighbs
            
    def print_graph(self):
        for  node in self.Nodes:
            print(f"{node} - {node.neighbours}\n")
        
    def get_node(self,coordinate):
        #get the corresponding node to a coordinate
        for node in self.Nodes:
            if  coordinate == (node.x,node.y):
                return node
        
    def find_cycles(self,Node, List):       
        Cycles = [] #will contain the cycles

        if len(List) > len(self.Nodes):
            return   #if the length of the list is greater than the number of nodes no cycle was found
        
        for neighbour in Node.neighbours: #for each neighbou
            new_neighb = self.get_node((neighbour.x,neighbour.y)) #get the node
            new_neighb.coming_from.append(Node) 
                
            if new_neighb in Node.coming_from and new_neighb in List: #if new_neighbour is the node we are coming from go to another node
                continue

            if new_neighb in List:
           #if the neighbour is already in the list then there is a cycle found
                index = List.index(new_neighb)
                cycle = List[index:]  #cycle will be from the first occurence of node to the end 
                
                Cycles.append(cycle) #put the cycle in a list                
                return Cycles
            #if node being visited isnt the one that isnt the one im coming from
            #and if it hasnt already been visited 
            
            new_list = List[:]
            new_list.append(new_neighb) #add it to a list

            cycle  = self.find_cycles(new_neighb,new_list) #find_cycles on node being visited
            Cycles.extend(cycle) 
            
        return Cycles
