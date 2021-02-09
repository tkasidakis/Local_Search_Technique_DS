
class WSNnode():

	def __init__(self,myid):

		if myid==0:
			self.id="A"
		elif myid==1:
			self.id="B"
		elif myid==2:
			self.id="C"
		elif myid==3:
			self.id="D"
		elif myid==4:
			self.id="E"
		elif myid==5:
			self.id="F"
		elif myid==6:
			self.id="G"

		self.uncov=0
		self.first_uncovered_value=1
		self.dom=0
		self.IsInDS=0
		self.num_of_neighbors=0
		self.isDSprevious=0
		self.energy=0.0
		self.neighbors=[]

	def getID(self):
		return self.id

	def isMyNeighbor(self,id):
		neighbor_found=0
		for i in range(len(self.neighbors)):
			if (self.neighbors[i].getID()==id):
				neighbor_found=1
				break
			#endif
		#endfor
		if(neighbor_found==1):
			return 1
		#endif
		else:
			return 0
		#endelse

	def getEnergy(self):
		return self.energy

	def getUncovered(self):
		return self.uncov

	def getDom(self):
		return self.dom

	def getIsInDS(self):
		return self.IsInDS

	def getNumOfNeighbors(self):
		return self.num_of_neighbors

	def getFirstUncovered(self):
		return self.first_uncovered_value

	def setID(self,id):
		self.id=id

	def setEnergy(self,enrg):
		self.energy=enrg

	def setFirstUncoveredVal(self,val):
		self.first_uncovered_value=val

	def setUncovered(self,uncov):
		self.uncov=uncov

	def setDom(self,dom):
		self.dom=dom

	def setIsInDS(self,val):
		self.IsInDS=val

	def addToNeighbors(self,node):
		self.neighbors.append(node)
		self.num_of_neighbors = self.num_of_neighbors + 1
		self.first_uncovered_value = self.first_uncovered_value +1

	def IncDomVal(self):
		self.dom = self.dom + 1

	def setIsDSprevious(self,val):
		self.isDSprevious=val

	def getDSprevious(self):
		return self.isDSprevious
