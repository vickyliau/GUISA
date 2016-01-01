from Tkinter import *
from tkFileDialog import *
import sys, Pmw, marshal, Tkinter, math, tkFont, UserList, string
from Pmw import MessageDialog
import numpy as num
import tkFileDialog
#import pysal
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pylab
from pylab import figure, show

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#-------------------------------------------------------------------------
class mydata(Frame):
	def __init__(self, parent):
        	Frame.__init__(self, parent)   
               	self.parent = parent
		self.menubar() #program starts with menubar

		#self.op=fileopen() #open fileIO.py when starting
		#self.op.myfile(self)
		
		#set two frames
		self.f=Frame(self.parent, width=600, height=680) 
		self.f1=Frame(self.parent, width=500, height=400)
		self.f2=Frame(self.parent, width=500, height=280)
		
		#set canvas
		self.parent.canvas=Canvas(self.f, width=600, height=680, bg='white')
		self.parent.canvas1=Canvas(self.f1, width=500, height=400, bg='white')
		#self.parent.canvas2=Canvas(self.f2, width=500, height=280, bg='white')

		#self.parent.canvas.create_oval(10,10,250,250, fill='gray90')
		#self.parent.canvas.create_line(1, 3, 50, 50, fill='black')
		
		self.f.pack(side=LEFT)
		self.f1.pack(side=TOP)
		self.f2.pack(side=RIGHT)
		#pack canvas
		self.parent.canvas.pack(side=LEFT)
		self.parent.canvas1.pack(side=TOP)
		#self.parent.canvas2.pack(side=RIGHT)
		
		# Bind mouse events to canvas
		self.parent.canvas.bind("<Button-1>", self.clicked) #bind the left button of the mouse with function
		self.parent.canvas.bind("<Enter>", self.moved) #The mouse pointer entered the widget (this event doesn't mean that the user pressed the Enter key!).http://www.pythonware.com/library/tkinter/introduction/events-and-bindings.htm
		#self.parent.canvas1.bind("<Button-1>", self.pressbar)

#-------------------------------------------------------------------------
		
	def clicked(self,event):
		self.OrgX, self.OrgY = event.x, event.y
		s = "Simple GIS: "+"Clicked Coordinate at x=%s  y=%s" % (self.OrgX, self.OrgY) #change back to original coordinates?  
        	self.parent.title(s) #if clicking the left button of the mouse, show the coordinate on the top of window 
				
	def moved(self,event):
		self.OrgX, self.OrgY = event.x, event.y 
		s = "Simple GIS: "+"Cursor Coordinate at x=%s  y=%s" % (self.OrgX, self.OrgY) #change back to original coordinates?
        	self.parent.title(s)
		
	def menubar(self):
		menubar = Menu(self.parent)
	# Create the File Pulldown, and add it to the menu bar
		fileMenu = Menu(menubar, tearoff=0)
		fileMenu.add_command(label = "New", command = self.FileNew)
		fileMenu.add_command(label = "Open", command = self.FileOpen)
		fileMenu.add_command(label = "Save", command = self.FileSave)
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=self.quit)
		menubar.add_cascade(label="File", menu=fileMenu)
		self.parent.config(menu=menubar)
	# Create the Edit Pulldown
		editmenu = Menu(menubar, tearoff = 0)
		editmenu.add_command(label = "Points", command = self.EditPoints)
		editmenu.add_command(label = "Lines", command = self.EditLines)
		editmenu.add_command(label = "Polygons", command = self.EditPolygons)
		menubar.add_cascade(label = "Edit", menu = editmenu)
		self.parent.config(menu=menubar)
	# Create the Tools Pulldown
		Toolsmenu = Menu(menubar, tearoff = 0)
		Toolsmenu.add_command(label = "Spatial Weights", command = self.Spatial_Weights)
		Toolsmenu.add_command(label = "Map Classification", command = self.MapClassification)
		menubar.add_cascade(label = "Tools", menu = Toolsmenu)
		self.parent.config(menu=menubar)
	# Create the DataVisualize Pulldown
		DataVisualizemenu = Menu(menubar, tearoff = 0)
		DataVisualizemenu.add_command(label = "Show Points", command = self.DataVisualizeShow_Points)
		DataVisualizemenu.add_command(label = "Draw Map", command = self.DataVisualizeDraw_Maps)
		menubar.add_cascade(label = "DataVisualize", menu = DataVisualizemenu)
		self.parent.config(menu=menubar)
	# Create the Statistics Pulldown
		statisticsmenu = Menu(menubar, tearoff = 0)
		statisticsmenu.add_command(label = "Nearest Neighbor Distance", command = self.statisticsNearNeighbor)
		statisticsmenu.add_command(label = "Save results", command = self.statisticsresults)
		menubar.add_cascade(label = "Statistics", menu = statisticsmenu)
		self.parent.config(menu=menubar)
	# Create the Explore Pulldown
		exploremenu = Menu(menubar, tearoff = 0)
		exploremenu.add_command(label = "Nearest Neighbor Distance Patterns", command = self.ExplorePoint_Patterns)
		menubar.add_cascade(label = "Explore", menu = exploremenu)
		self.parent.config(menu=menubar)
	# Create the Help Pulldown
		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label = "About", command = self.HelpAbout)
		helpmenu.add_command(label = "Tutorial", command = self.HelpTutorial)
		menubar.add_cascade(label = "Help", menu = helpmenu)
		self.parent.config(menu=menubar)
#-------------------------------------------------------------------------  
#menubar functions
	def FileNew(self): 
	#clear window
        	self.parent.canvas.delete(ALL)
	#canvas.delete(variables), remove the previous items
	#-------------------------------------------------------------------------
	def FileOpen(self):	
	#read data by string, transfer to a list, find max X, max Y, min X, min Y, reverse coordinates
		filecontents=askopenfilename(filetypes=[ ("comma_separatedfiles","*.csv"),("textfiles","*.txt"),("excelfiles","*.xls"),("pythonfiles","*.py"),("accessfiles","*.asc"),("arcgisfiles","*.dbf"), ("spssfiles","*.sav"), ("multi_usagefiles","*.dat")])
		if filecontents != None:
			fp=open(filecontents, 'r') #fp is just the tag to open
			filecontents=fp.readlines() #read all the lines of the file and return them as a list
			fp.close() #close file because data are already in PC's memory
	#search for the x's, y's max and min and then set the scale factor
		newdata=[] #create a new list
		for line in filecontents[1:]: #get rid of the header
			x, y=line.strip().split(',') 
			#mydata truly read the file in a 'list'. (1)transfer to a list by split (2) get rid of extra spaces by strip
		#print filecontents #print the original data
			x=float(x)
			y=float(y)
			newdata.append([x,y]) #why does it print as none?
		newdata=num.array(newdata)
		maxc=newdata.max(axis=0) # the maximum
		self.minc=newdata.min(axis=0) # the minimum
		canvasrange=maxc-self.minc # ranges of x and y
		#print self.minc
		myscale=canvasrange/num.array([600, 680]) #scaling x and y separately
		Cmyscale=myscale.max()-num.array([5]) # find the larger scale and shrink a little bit?
		newcoordinates=(newdata-self.minc)/Cmyscale #downscaling coordinates to fit needs of canvas
		#print newcoordinates #coordinates that show in canvas
		
		#reverse coordinates
		self.normalcoordinates=abs(num.array([0, 680])-newcoordinates) #(x, 680-y)
		#print self.normalcoordinates, type(self.normalcoordinates)

	#show origin data in another frame

		s = Scrollbar(self.f2) #set a scrollbar
		T = Text(self.f2) # set to fill in text
		T.focus_set()
		self.f2.pack(side=RIGHT)
		s.pack(side=RIGHT, fill=Y)
		T.pack(side=LEFT, fill=Y)
		s.config(command=T.yview)
		T.config(yscrollcommand=s.set)
		for i in filecontents[1:]: 
			T.insert(END, i)
		
	#-------------------------------------------------------------------------  
	def FileSave(self):
		print "ABC"
	#-------------------------------------------------------------------------  
	def EditPoints(self):
		self.parent.canvas.bind("<Button-1>", self.pointclicked)
				
	#-------------------------------------------------------------------------  
	def EditLines(self):
		self.parent.canvas.bind("<Button-1>", self.lineclicked)

	#-------------------------------------------------------------------------  
	def EditPolygons(self):
		self.parent.canvas.bind("<Button-1>", self.polugonclicked)

	#-------------------------------------------------------------------------  
	def MapClassification(self): #try to import pysal?
		print "ABC"
	#-------------------------------------------------------------------------  
	def Spatial_Weights(self): #try to import pysal?
		print "ABC"
	#-------------------------------------------------------------------------  
	def DataVisualizeShow_Points(self):
		for x,y in self.normalcoordinates:
			self.parent.canvas.create_oval(x, y, x+4, y+4,fill='black') #inherent from initial functions
			#points are not in the center of oval?
			x+=1
			y+=1
		#when the file opens, finishes processing and plots points, link mouse position with points by one click
	#-------------------------------------------------------------------------  
	def DataVisualizeDraw_Maps(self):
		#sorting them and draw line?
		for x,y in self.normalcoordinates:
			self.parent.canvas.create_line(x, y, x+1, y+1,fill='blue') 
			x+=1
			y+=1
	#-------------------------------------------------------------------------  
	def statisticsNearNeighbor(self):
		a=self.normalcoordinates
		self.tablesize=int(a.shape[0])#the first number (the larger one) is the table size (tuple, using index). (x*x)
		#print self.tablesize, type(self.tablesize)

		newtable=[] #create a list
		for x, y in self.normalcoordinates:
			for p, q in self.normalcoordinates:
				c=math.sqrt((x-p)**2+(y-q)**2)
				newtable.append(c)
				#finish near neighbor but still in a bunch of single float numbers
				#print c, type(c)
			
		#convert numbers into a table
		self.newtable=num.array(newtable) #change near neighborhood value into an array
								
		#transfer array for exporting table (1)using index function of array (2)change into string
		myindexr=range(self.tablesize*self.tablesize) #a whole list
		myindexarray=num.array(myindexr) #change into an array
		myindexshape=myindexarray.reshape(self.tablesize, self.tablesize) #become square
		myindex=myindexshape.T #index.transpose

		self.t=self.newtable[myindex] #change into a whole table in an array
		u=num.sort(self.t) #sort all array
		self.w=u.T[1]	#find nearest neighbor	
		#print self.w, type(self.w)

		#change an array data into a string in order to save as a file
		#self.s = "\n".join([ "\t".join(map(str,row)) for row in self.t]) #change any two point distance into a list
		self.s = "\n".join(str(n) for n in self.w) #let nearest neighbor into a string

	#-------------------------------------------------------------------------  
	def statisticsresults(self):
		self.nearneighbor=tkFileDialog.asksaveasfilename(filetypes=[ ("textfile","*.txt")])
		if self.nearneighbor != None:
			fp=open(self.nearneighbor, 'w') #open a new file
			fp.write(self.s)
			fp.close()
		else:
			pass
			
	#-------------------------------------------------------------------------  
	def ExplorePoint_Patterns(self):
		distancesort=num.sort(self.w)-self.w.min()
		#print distancesort
		
		myrange=self.w.max()-self.w.min() #range
		self.mycenter=myrange/4
		#print self.mycenter
		
#count numbers
		mycount1=[]
		mycount2=[]
		mycount3=[]
		mycount4=[]
		for i in distancesort:
			if i < self.mycenter:
				#print i
				mycount1.append(distancesort)
			elif i > self.mycenter and i < self.mycenter*2:
				#print i
				mycount2.append(distancesort)
			elif i > self.mycenter*2 and  i < self.mycenter*3:
				#print i
				mycount3.append(distancesort)
			elif i > self.mycenter*3:
				#print i
				mycount4.append(distancesort)
			else:
				pass
		self.mycount1=len(list(mycount1))
		self.mycount2=len(list(mycount2))
		self.mycount3=len(list(mycount3))
		self.mycount4=len(list(mycount4))
		print self.mycount1 , self.mycount2, self.mycount3, self.mycount4
		
#embed matplotlib into tkinter
		f1=Figure(figsize=(6,5)) #set the size
		self.a=f1.add_subplot(111)

		#set plot in canvas
		self.myplot= FigureCanvasTkAgg(f1, self.parent.canvas1)
		self.myplot.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)
		self.myplot._tkcanvas.pack(side=RIGHT, fill=BOTH, expand=1)
	
		# set plot data
		N=4
		self.mycount=(self.mycount1, self.mycount2, self.mycount3, self.mycount4) #for quantities of the plot
		self.ind = num.arange(N)  # the x locations for the groups
		self.width = 0.5       # the width of the bars		
		colors=['r','r','r','r']
		self.rects1 = self.a.bar(self.ind, self.mycount, self.width, color=colors)
				
		# add some
		self.a.set_ylabel('Counts')
		self.a.set_xlabel('Nearest Neighbor distance (meters)')
		self.a.set_title('Number distribution of the nearest neighbor distances')
		self.a.set_xticks(self.ind+self.width)
		self.a.set_xticklabels( (round(self.mycenter, 2), round(self.mycenter*2, 2), round(self.mycenter*3, 2), round(self.mycenter*4, 2)) )
		#ax.legend( (self.rects1[0], rects2[0]), ('Men', 'Women') )
		
		#mouse moving, mouse selecting in matplotlib & GUI in Tkinter
		self.parent.canvas.bind("<Button-1>", self.canvasplot) #click points in the canvas
		self.myplot.mpl_connect('button_press_event', self.pressbar)#click bar in the plot
		

		"""
		#open a new window
		N=4
		self.mycount=(self.mycount1, self.mycount2, self.mycount3, self.mycount4) #for quantities of the plot
		self.ind = num.arange(N)  # the x locations for the groups
		self.width = 0.5       # the width of the bars

		self.fig = plt.figure() #open a new outer canvas, but this way can not run both window at the same time
		self.ax = self.fig.add_subplot(111)
		colors=['r','r','r','r']
		self.rects1 = self.ax.bar(self.ind, self.mycount, self.width, color=colors)
		
		# add some
		self.ax.set_ylabel('Counts')
		self.ax.set_xlabel('Nearest Neighbor distance (Kilometers)')
		self.ax.set_title('Cumulative distribution of the nearest neighbor distances')
		self.ax.set_xticks(self.ind+self.width)
		self.ax.set_xticklabels( (self.mycenter, self.mycenter*2, self.mycenter*3, self.mycenter*4) )
		#ax.legend( (self.rects1[0], rects2[0]), ('Men', 'Women') )
		
		#mouse moving, mouse selecting in matplotlib
		self.fig.canvas.mpl_connect('button_press_event', self.pressbar)#click button
						
		#draw near-neighborhood lines after selecting the bar in the plot
		#self.parent.canvas.bind("<Button-1>", self.linkmouse) 
		
		
		#lines in canvas link with bars in the plot
		

		plt.show()		
		"""

	
	#-------------------------------------------------------------------------  
	def HelpAbout(self):
	#version explanations        
		self.dialog=MessageDialog(self, title="About Simple GIS for Taiwan", message_text="Copytight(C)2016\nYan-ting (Vicky) Liau\nE-mail: yliau1@hotmail.com\nAll rights reserved")
		result=self.dialog.activate()	
	#-------------------------------------------------------------------------  
	def HelpTutorial(self):
		print "ABC"
		#open a pdf

#-------------------------------------------------------------------------
#########################################################################################################################
#after plotting, when click the point on the canvas
	def canvasplot(self, event):
		if self.normalcoordinates == None: 
			#when none of points are read in and plot notthing and the linkage will not work. 
			pass
		else: #select point and change into red color
			self.OrgX, self.OrgY = event.x, event.y #catch the coordinates
			self. mousearray=num.array([self.OrgX, self.OrgY])
			s = "Simple GIS: "+"Clicked Coordinate at x=%s  y=%s" % (self.OrgX, self.OrgY)
			self.parent.title(s)
			
			#self.myplot.mpl_connect('axes_leave_event', self.pointlink)

			for i, s in enumerate(self.normalcoordinates): #set a loop for index as i
				#for u, t in self.normalcoordinates:
				x, y=s
				p=round(x) #not easy to select float, so round coordinates
				q=round(y)
				#print num.array([p, q])
				#set a allowed deviation (buffer) if the mouse click is not absolutely precise?
				if self. mousearray in num.array([p, q]): 
					#print self. mousearray #separate arrays for each points
					self.parent.canvas.create_oval(p, q, p+4, q+4,fill='red')
					
					print i, self.normalcoordinates[i], self.w[i] 
					#print index & coordinate & nearest neighbor which is selected by mouse
					
					#self.myplot.mpl_connect('button_release_event', self.pointlink)

					if self.w[i] < self.mycenter:
						print i
						colors=['yellow','red','red','red']
						self.rects1 = self.a.bar(self.ind, self.mycount,self.width, color=colors)
					elif self.w[i] < self.mycenter*2 and self.w[i] > self.mycenter:
						colors=['red','yellow','red','red']
						self.rects1 = self.a.bar(self.ind, self.mycount,self.width, color=colors)
					elif self.w[i] < self.mycenter*3 and self.w[i] >self.mycenter*2:
						colors=['red','red','yellow','red']
						self.rects1 = self.a.bar(self.ind, self.mycount,self.width, color=colors)
					elif self.w[i] > self.mycenter*3:
						colors=['red','red','red', 'yellow']
						self.rects1 = self.a.bar(self.ind, self.mycount,self.width, color=colors)
					else:
						pass
					

				else:
					pass
				"""

	def pointlink(self, event):
		for i, s in enumerate(self.normalcoordinates):
			x, y=s
			p=round(x) #not easy to select float, so round coordinates
			q=round(y)
			if self. mousearray in num.array([p, q]):
				self.parent.canvas.create_oval(p, q, p+4, q+4,fill='red')
				print i, self.normalcoordinates[i], self.w[i]

				if self.w[i] < self.mycenter:
					print i
					colors=['yellow','red','red','red']
					self.a.bar(self.ind, self.mycount,self.width, color=colors)
				elif self.w[i] < self.mycenter*2 and self.w[i] > self.mycenter:
					print i
					colors=['red','yellow','red','red']
					self.a.bar(self.ind, self.mycount,self.width, color=colors)
				elif self.w[i] < self.mycenter*3 and self.w[i] >self.mycenter*2:
					print i
					colors=['red','red','yellow','red']
					self.a.bar(self.ind, self.mycount,self.width, color=colors)
				elif self.w[i] > self.mycenter*3:
					print i
					colors=['red','red','red', 'yellow']
					self.a.bar(self.ind, self.mycount,self.width, color=colors)
				else:
					pass
			"""
#-------------------------------------------------------------------------
#########################################################################################################################
#digitize points, lines and polygon
	def pointclicked(self, event):
		self.OrgX, self.OrgY = event.x, event.y #catch the coordinates
		s = "Simple GIS: "+"Clicked Coordinate at x=%s  y=%s" % (self.OrgX, self.OrgY) #change back to original coordinates?  
        	self.parent.title(s)
		self.parent.canvas.create_oval(self.OrgX, self.OrgY, self.OrgX+4,self.OrgY+4,fill='blue') 

#-------------------------------------------------------------------------
	def lineclicked(self, event):
		self.OrgX, self.OrgY = event.x, event.y
		s = "Simple GIS: "+"Clicked Coordinate at x=%s  y=%s" % (self.OrgX, self.OrgY)
		self.parent.title(s)
		self.parent.canvas.create_line(self.OrgX, self.OrgY, self.OrgX+1, self.OrgY+1,fill='green') #?

#-------------------------------------------------------------------------
	def polygonclicked(self, event):
		self.OrgX, self.OrgY = event.x, event.y
		s = "Simple GIS: "+"Clicked Coordinate at x=%s  y=%s" % (self.OrgX, self.OrgY)
		self.parent.title(s)
		#self.parent.canvas.create_line(self.OrgX, self.OrgY, self.OrgX,self.OrgY,fill='blue') #?

#-------------------------------------------------------------------------
#######################################################################################################################
#when click the plot
	def pressbar(self, event):
		x=event.xdata # the clicked locations
		y=event.ydata
		print "Clicked Coordinate at x=%s  y=%s" % (x,y) #any selected point
		event.canvas.figure.patch.set_facecolor('green') #work for outside canvas
    		event.canvas.draw()

		if x <0.5: #change color as any selected bar
			colors=['yellow','r','r','r']
			self.a.bar(self.ind, self.mycount,self.width, color=colors)

			for i, s in enumerate(self.w): 
		#let whole array without arrangement into a list with index, i is the index, s is the value
				if s < self.mycenter: #when the number in a list is the smallest
					#print self.normalcoordinates[i] #the original coordinates of near neighbor
					x,y =self.normalcoordinates[i] #x, y belongs to numpy.int32
					self.parent.canvas.create_oval(x, y, x+4, y+4,fill='red') 
					#self.parent.canvas.create_line(x, y, x+4, y+4,fill='green') 
				else:
					pass

		elif x>1 and x<1.5:
			colors=['r','yellow','r','r']
			self.a.bar(self.ind, self.mycount,self.width, color=colors)
		
			for i, s in enumerate(self.w): 
				if s > self.mycenter and s < self.mycenter*2:
					x,y =self.normalcoordinates[i] 
					self.parent.canvas.create_oval(x, y, x+4, y+4,fill='red') 
				
				else:
					pass

		elif x>2 and x<2.5:
			colors=['r','r','yellow','r']
			self.a.bar(self.ind, self.mycount,self.width, color=colors)
		
			for i, s in enumerate(self.w): 
				if s > self.mycenter*2 and  s < self.mycenter*3:
					x,y =self.normalcoordinates[i] 
					self.parent.canvas.create_oval(x, y, x+4, y+4,fill='red') 	
				else:
					pass

		elif x>3 and x<3.5:
			colors=['r','r','r','yellow']
			self.a.bar(self.ind, self.mycount,self.width, color=colors)
		
			for i, s in enumerate(self.w):
				if s > self.mycenter*3:
					x,y =self.normalcoordinates[i] 
					self.parent.canvas.create_oval(x, y, x+4, y+4,fill='red') 
				else:
					pass


		else:
			pass


#-------------------------------------------------------------------------
def main():
	root = Tk()
	root.geometry("%dx%d+%d+%d" % (1100,680,150800,2798337))
	root.maxsize(1100,680)
	root.minsize(1100,680)
	root.title("Simple GIS for Taiwan")
	app = mydata(root)
	root.mainloop()  
#------------------------------------------------------------------------- 
if __name__ == '__main__':
    main()
    
