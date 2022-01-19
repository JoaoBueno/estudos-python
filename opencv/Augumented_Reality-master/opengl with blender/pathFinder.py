'''
* Team Id : 71
* Author List : Ravi, Sujit,raj
* Filename: echo.py
*Functions:adjacent_nodes,next_direction,Pos,findNodes,long
* Theme: Thirsty Crow
* Global Variables: traversal_nodes,arena
'''
    
arena=[[0,0,0,0,0,1,1,0,0,0,0,0],
		  [0,0,0,1,1,0,0,1,1,0,0,0],
		  [0,1,1,0,0,1,1,0,0,1,1,0],
		  [1,0,0,1,1,0,0,1,1,0,0,1],
		  [0,1,1,0,0,1,1,0,0,1,1,0],
		  [1,0,0,1,1,0,0,1,1,0,0,1],
		  [0,1,1,0,0,1,1,0,0,1,1,0],
		  [1,0,0,1,1,0,0,1,1,0,0,1],
		  [0,1,1,0,0,1,1,0,0,1,1,0],
		  [0,0,0,1,1,0,0,1,1,0,0,0],
		  [0,0,0,0,0,1,1,0,0,0,0,0]]
traversal_nodes=[]

"""
Function Name : adjacent_nodes()
Input: cell no-x , and axis- axiss
Output: nearby coordinates
Purpose: search all the coordnates of the cell and returns the coordinates related to the axis. example: if x is 2  and axiss is 2 , the it will return (1,3),(3,4)
"""
def adjacent_nodes(x,axiss):
	xy=[[0,0],[0,0]]
	if axiss==1:
		xy[0][0]=x[0]
		xy[0][1]=x[1]
		xy[1][0]=x[0]
		xy[1][1]=x[1]+3
	if axiss==2:
		xy[0][0]=x[0]-1
		xy[0][1]=x[1]+1
		xy[1][0]=xy[0][0]+2
		xy[1][1]=xy[0][1]+1
	if axiss==3:
		xy[0][0]=x[0]-1
		xy[0][1]=x[1]+2
		xy[1][0]=xy[0][0]+2
		xy[1][1]=xy[0][1]-1
		
	return xy

"""
Function Name : next_direction()
Input: row/column no. of nodes
Output: direction , 0- upperdiagnal , 1= lower diagnal, 2=horizontal
Purpose: using Greedy algorithm , it searches for next shortest path
"""
def next_direction(a1,a2):
  if a1==a2:
	  return "2"
  elif a1>a2:
	  return "0"
  else:
	  return "1"

"""
Function Name : next_position()
Input: starting point-(si,sj) and final point- f
Output: return the next move 
Purpose: using Greedy algorithm , it searches for next shortest path
"""
def next_position(si,sj,f):
  a=next_direction(si,f[0])
  b=next_direction(sj,f[1])
  return a+b


"""
Function Name : priority()
Input: cellNumber , flag
Output: returns the priority number from the 1-5  
Purpose: by assigining the priority number to each of the pebbles , to set the order of traversing pebble
"""
def priority(cellNumber,flag):
	if cellNumber==5 or cellNumber==10 or cellNumber==15:
		return abs(1-flag)
	if cellNumber==2 or cellNumber==6 or cellNumber==11 or cellNumber==16:
		return abs(2-flag)
	if cellNumber==4 or cellNumber==8 or cellNumber==13 or cellNumber==18:
		return abs(4-flag)
	if cellNumber==9 or cellNumber==14 or cellNumber==19:
		return abs(5-flag)
	else:
		return 3

	

"""
Function Name : findNodes()
Input: current row and column value of robot
Output: next current row and column value of robot
Purpose: recursion method to find next path
"""
def findNodes(i,j,f):
  global traversal_nodes
  traversal_nodes.append([i,j])
  
  if pow(i-f[0],2) + pow(j-f[1],2)<=2:
	  traversal_nodes.append(f)
	  return 

  position=next_position(i,j,f)
 
  if position=="01":
	  if arena[i-1][j+1]:
		  findNodes(i-1,j+1,f)
	  else:
		  findNodes(i,j+1,f)

  elif position=="21":
	  if arena[i][j+1]:
		  findNodes(i,j+1,f)
	  else:
		  findNodes(i-1,j+1,f)

  elif position=="11":
	  if arena[i+1][j+1]:
		  findNodes(i+1,j+1,f)
	  else:
		  findNodes(i,j+1,f)

  elif position=="12":
	  if j==0 or arena[i+1][j+1]:
		  findNodes(i+1,j+1,f)
	  else:
		  findNodes(i+1,j-1,f)

  elif position=="10":
	  if arena[i+1][j-1]:
		  findNodes(i+1,j-1,f)
	  else:
		  findNodes(i,j-1,f)

  elif position=="20":
	  if arena[i][j-1]:
		  findNodes(i,j-1,f)
	  else:
		  findNodes(i-1,j-1,f)

  elif position=="00":
	  if arena[i-1][j-1]:
		  findNodes(i-1,j-1,f)
	  else:
		  findNodes(i,j-1,f)

  else:
	  if j==0 or arena[i-1][j+1]:
		  findNodes(i-1,j+1,f)
	  else:
		  findNodes(i-1,j-1,f)

  
  return
"""
Function Name : findPath()
Input: area_config,Robot_Start
Output: paths , Id of pebbles
Purpose: 1. split the given input in ids, cells, axis
         2. sort the pebbles data according the priority
         3. make the string from start to end position
                      L=LEFT
                      R=RIGHT
                      B=BUZZER
                      P= 120DEGREE LEFT
                      Q= 120DEGREE RIGHT
                      E= END OF THE STRING

        4. reeturn the string "paths"
"""

def findPath(area_config,Robot_Start):
	initial_nodes=[[1,4],[2,2],[3,4],[2,6],[3,0],[4,2],[5,4],[4,6],[3,8],[5,0],[6,2],[7,4],[6,6],[5,8],[7,0],[8,2],[9,4],[8,6],[7,8]]
	paths= ""
	waterPitcher=[]
	ids=[]
	cells=[]
	axis=[]
	start_point=[]
	pebble=[]
	flag=1
	j=0
	counterarray=[]
	if Robot_Start=="START-1":
		flag=0
	else:
		flag=6
	counterarray=[]
	for k in area_config:
		v=area_config[k]
		if k==0:
			waterPitcher.append([k,v[1],int(v[2].split("-")[0])])
			continue
		pebble.append([k,v[1],int(v[2].split("-")[0]),priority(v[1],flag)])

		
	pebble.sort(key=lambda x:x[3])
	for i in range(0,len(pebble)):
		ids.insert(j,pebble[i][0])
		cells.insert(j,pebble[i][1])
		axis.insert(j,pebble[i][2])
		ids.insert(j+1,waterPitcher[0][0])
		cells.insert(j+1,waterPitcher[0][1])
		axis.insert(j+1,waterPitcher[0][2])
		j=j+2
	if Robot_Start=="START-1":
		x=5;y=0
		start_point=[x,y]
		previous_node=[x,y-1]
	else:
		x=5;y=11
		start_point=[x,y]
		previous_node=[x,y+1]

		
	j=0;
	for i in range(0,len(ids)):
	       axis_nodes=adjacent_nodes(initial_nodes[cells[i]-1],axis[i])
	       su1=abs(start_point[0]-axis_nodes[0][0])+abs(start_point[1]-axis_nodes[0][1])
	       su2=abs(start_point[0]-axis_nodes[1][0])+abs(start_point[1]-axis_nodes[1][1])
	       if su1<su2:
		       destination_node=[axis_nodes[0][0],axis_nodes[0][1]]
		       j=j+1
		       counterarray.insert(j,axis_nodes[1])
	       else:
		       destination_node=[axis_nodes[1][0],axis_nodes[1][1]]
		       j=j+1
		       counterarray.insert(j,axis_nodes[0])
	       findNodes(start_point[0],start_point[1],destination_node)
	       start_point=destination_node
	traversal_nodes.append(traversal_nodes[-1])
	z=-1
	for i in range(0,len(traversal_nodes)-1):
		current_node=traversal_nodes[i];next_nodes=traversal_nodes[i+1]
		if current_node==next_nodes:
			z=z+1
			############################################
			if current_node[0]+1 == previous_node[0] and current_node[1]-1 == previous_node[1]: #1
				if counterarray[z][0]==current_node[0]:
					paths=paths + 'P'
				elif counterarray[z][0] >current_node[0]:
					paths=paths + 'Q'
				
			if current_node[0]+1 == previous_node[0] and current_node[1]+1 == previous_node[1]: #4
				if counterarray[z][0]>current_node[0]:
					paths=paths + 'P'
				elif counterarray[z][0]==current_node[0]:
					paths=paths + 'Q'
			if current_node[0]-1 == previous_node[0] and current_node[1]-1 == previous_node[1]: #2
				if counterarray[z][0] < current_node[0]:
					paths=paths + 'P'
				elif counterarray[z][0]==current_node[0]:
					paths=paths + 'Q'
			if current_node[0]-1 == previous_node[0] and current_node[1]+1 == previous_node[1]: #5
				if counterarray[z][0]==current_node[0]:
					paths=paths + 'P'
				elif counterarray[z][0] < current_node[0]:
					paths=paths + 'Q'
			if current_node[0] == previous_node[0] and current_node[1]-1 == previous_node[1]: #3
				if counterarray[z][0] < current_node[0]:
					paths=paths + 'P'
				elif counterarray[z][0] > current_node[0]:
					paths=paths + 'Q'
			if current_node[0] == previous_node[0] and current_node[1]+1 == previous_node[1]: #6
				if counterarray[z][0] > current_node[0]:
					paths=paths + 'P'
				elif counterarray[z][0] < current_node[0]:
					paths=paths + 'Q'


			###################################################
			paths=paths+'B'
			current_node=next_nodes
			if i>(len(traversal_nodes)-3):
				break
			next_nodes=traversal_nodes[i+2]
			
		
		if next_nodes==previous_node:
			paths=paths+'H'
			previous_node=current_node
			continue
		if current_node[0]+1 == previous_node[0] and current_node[1]-1 == previous_node[1]: #1
			if current_node[0]==next_nodes[0]:
				paths=paths+'R'
			else:
				paths=paths+'L'
		if current_node[0]+1 == previous_node[0] and current_node[1]+1 == previous_node[1]: #4
			if current_node[0]==next_nodes[0]:
				paths=paths+'L'
			else:
				paths=paths+'R'
		if current_node[0]-1 == previous_node[0] and current_node[1]-1 == previous_node[1]: #2
			if current_node[0]==next_nodes[0]:
				paths=paths+'L'
			else:
				paths=paths+'R'
		if current_node[0]-1 == previous_node[0] and current_node[1]+1 == previous_node[1]: #5
			if current_node[0]==next_nodes[0]:
				paths=paths+'R'
			else:
				paths=paths+'L'
		if current_node[0] == previous_node[0] and current_node[1]-1 == previous_node[1]: #3
			if current_node[0]>next_nodes[0]:
				paths=paths+'L'
			else:
				paths=paths+'R'
		if current_node[0] == previous_node[0] and current_node[1]+1 == previous_node[1]: #6
			if current_node[0]>next_nodes[0]:
				paths=paths+'R'
			else:
				paths=paths+'L'
		previous_node=current_node
	
	paths=paths+"E"
	return paths


