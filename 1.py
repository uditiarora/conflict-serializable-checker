from collections import defaultdict 
import networkx
import matplotlib.pyplot as plt
class Graph(): 
    def __init__(self,vertices): 
        self.graph = defaultdict(list) 
        self.V = vertices 
  
    def addEdge(self,u,v): 
    	if(v not in self.graph[u]):
        	self.graph[u].append(v) 
  
    def isCyclicUtil(self, v, visited, recStack): 
        visited[v] = True
        recStack[v] = True
        for neighbour in self.graph[v]: 
            if visited[neighbour] == False: 
                if self.isCyclicUtil(neighbour, visited, recStack) == True: 
                    return True
            elif recStack[neighbour] == True: 
                return True
        recStack[v] = False
        return False
   
        
    def isCyclic(self): 
        visited = [False] * self.V 
        recStack = [False] * self.V 
        for node in range(self.V): 
            if visited[node] == False: 
                if self.isCyclicUtil(node,visited,recStack) == True: 
                    return True
        return False
    
    def topologicalSortUtil(self,v,visited,stack):
        visited[v] = True
        for i in self.graph[v]: 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack)
        stack.insert(0,v) 
 
    def topologicalSort(self): 
        visited = [False]*self.V 
        stack = [] 
        for i in range(self.V): 
            if visited[i] == False: 
                self.topologicalSortUtil(i,visited,stack)
        return stack, visited


file1 = open("input1.txt","r")
lines = file1.readlines()
line1 = lines[0]
line1 = line1.strip("\n")
line1 = line1.strip(" ")
line1 = line1.strip("TRANS:")
tno = line1.split(",")
for i in range(0, len(tno)):
	tno[i] = tno[i].strip(" ")
	tno[i] = tno[i].strip("T")
	tno[i] = int(tno[i])

line2 = lines[1]
line2 = line2.strip("\n")
line2 = line2.strip(" ")
line2 = line2.strip("DATA:")
dno = line2.split(",")
for i in range(0,len(dno)):
	dno[i] = dno[i].strip(" ")

# list of [transaction number, operation, data]
transactions = []

for i in range(3, len(lines)):
	line = lines[i];
	temp = []
	line = line.strip("\n")
	line = line.strip(" ")
	line = line.strip(";")
	line = line.strip("T")
	arr = line.split(":")
	num = int(arr[0])
	if(arr[1].count("R") == 1):
		string = arr[1][arr[1].index('(') + 1 : arr[1].index(')') ]
		string = string.strip(" ")
		temp = [num,"read",string]
	else:
		string = arr[1][arr[1].index('(') + 1 : arr[1].index(')') ]
		string = string.strip(" ")
		temp = [num,"write",string]
	transactions.append(temp)


g = Graph(len(tno)+1)
gx = networkx.DiGraph()
for i in tno:
	gx.add_node(i)

for i in range(0, len(transactions)-1):
	for j in range(i+1, len(transactions)):
		if(transactions[i][0] != transactions[j][0]):
			if(transactions[i][2] == transactions[j][2]):
				if((transactions[i][1] == "read" and transactions[j][1] == "read") == False):
					g.addEdge(transactions[i][0], transactions[j][0])
					gx.add_edge(transactions[i][0], transactions[j][0])
networkx.draw(gx, with_labels = True) 
plt.savefig("filename.png") 

if(g.isCyclic() == True):
	print("Not conflict serializable")
else:
	print("Conflict serializable")
	stack, visited = g.topologicalSort()
	stack.remove(0)
	print("Order of serialized transactions:")
	for i in range(0, len(tno)-1):
		print(str(stack[i])+" -->", end = " ")
	print(stack[-1])
	




