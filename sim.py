# Kasidakis Theodoros 2258
# This is a simulation of a Wirelles Sensor Network.
# In this simulation we try to improve the total lifetime of WSNs consisting of nodes
# with varying initial energy.For this purpose we use the Local Search Algorithm(Pino,Choudhury,Al-Turjman).
# Local Search Algorithm has as an input a number of disjoint Dominating Sets.
# To create the Dominating Sets we use the Algorithm For Domatic Partition(Islam,Akl,Meijer)

import WSNnode
import random
import time

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def Domatic_Partition(graph,nodes):

	dominating_sets=[] # Disjoint Dominating Sets
	delta=100000
	temp_DS=[] # a temporary Dominating Set used in each round to contain the dominating nodes
	incompatible=1/(nodes+1)
	list_with_minUncov=[]
	min_uncovered=10000
	min_dom=10000
	list_with_mindom=[]
	all_nodes_incompatible=1

	for i in range(nodes):
		if graph[i].getNumOfNeighbors()<delta :
			delta=graph[i].getNumOfNeighbors()

	for i in range(nodes):
		Nu=graph[i].getNumOfNeighbors() # N(u) = {v|(u,v) E EdgeSet, u!v} , N[u] = N(u)U{u}
		Nu=Nu+1
		graph[i].setUncovered(1/Nu)
		graph[i].setDom(0);

	i=1

	while i<=(delta+1): # Algorithm for Domatic Partition

		list_with_minUncov=[]
		min_uncovered=10000
		min_dom=10000
		list_with_mindom=[]
		all_nodes_incompatible=1

		for k in range(nodes): # Find the smallest compatible node u in V\(D1 U D2 U D3..U temp_D)
			if graph[k].getIsInDS()!=1 and graph[k].getUncovered()!=incompatible and graph[k].getDSprevious()!=1:
				if(graph[k].getUncovered()<min_uncovered):
					min_uncovered=graph[k].getUncovered()
					all_nodes_incompatible=0

		if (all_nodes_incompatible==0):

			for j in range(nodes):
				if(graph[j].getUncovered()==min_uncovered):
					list_with_minUncov.append(graph[j])
			if(len(list_with_minUncov)>1): # two nodes have the same uncovered neighbors,so compare with dom values. #
				for j in range(nodes):
					if(graph[j].getUncovered()==min_uncovered):
						if(graph[j].getDom()<min_dom):
							min_dom=graph[j].getDom()

				for j in range(nodes):
					if graph[j].getUncovered()==min_uncovered and graph[j].getDom()==min_dom:
						list_with_mindom.append(graph[j])

					#this node is added to the temp_DS because has the min dom number (or min id)
				list_with_mindom[0].setIsDSprevious(1)
				temp_DS.append(list_with_mindom[0].getID())
				list_with_mindom[0].setIsInDS(1)
				list_with_mindom[0].IncDomVal()


			else: #this node is added to the temp_DS because it has the max uncovered neighbors
				temp_DS.append(list_with_minUncov[0].getID())
				list_with_minUncov[0].setIsInDS(1)
				list_with_minUncov[0].setIsDSprevious(1)
				list_with_minUncov[0].IncDomVal()

		if(all_nodes_incompatible==1): ## all nodes are incompatible so we move to the next Dominating Set or we terminate the algoritm ##
			dominating_sets.append(temp_DS)
			temp_DS=[]
			i=i+1
			for j in range(nodes):
				for k in range(graph[j].getNumOfNeighbors()):
					if(graph[j].neighbors[k].getIsInDS()==1):
						graph[j].IncDomVal()

			for j in range(nodes):
				graph[j].setUncovered(1/(graph[j].getNumOfNeighbors() +1))
				graph[j].setIsInDS(0)

			continue

		# now we must update uncovered neighbors and neighbors in dominating sets for each node and repeat the algorithm #
		for j in range(nodes):
			if(graph[j].getIsInDS()==0): # check only the nodes which are not in temp_DS{}
				uncovered_val=graph[j].getFirstUncovered()

				for k in range(graph[j].getNumOfNeighbors()): # check if anyone of the neighbors is in the temp_DS , so it is dominated by itself

					if(graph[j].neighbors[k].getIsInDS()==1):
						uncovered_val = uncovered_val - 2
					else: # check if the neighbors of the neighbors are dominated by another vertex
						for l in range(graph[j].neighbors[k].getNumOfNeighbors()):
							if(graph[j].neighbors[k].neighbors[l].getIsInDS()==1):
								uncovered_val = uncovered_val - 1

				if(uncovered_val<=0):
					graph[j].setUncovered(1/(nodes+1))
				else:
					graph[j].setUncovered(1/uncovered_val)

		all_nodes_incompatible=1
	## end of while loop ##
	return dominating_sets
## end of function for the Domatic Partition ##

## main programm ##

wsn_graph=[]
dominating_sets=[]
rate=0.05

print("==== SIMULATION OF A WIRELLES SENSOR NETWORK ====")
print("")
num_of_nodes=input("Enter the number of nodes of the WSN: ")

for i in range(int(num_of_nodes)):
	node=WSNnode.WSNnode(i)
	wsn_graph.append(node)

for i in range(int(num_of_nodes)):
	for j in range(int(num_of_nodes)):
		if i!=j:
			print("Is node [" + wsn_graph[j].getID() +  "] in the communication range of node ["+ wsn_graph[i].getID()+"] ? ....(y/n)....:")
			answer=input()
			if answer=="y":
				wsn_graph[i].addToNeighbors(wsn_graph[j])

print("")

for i in range(int(num_of_nodes)):
	print("Node [" + wsn_graph[i].getID() + "] can communicate with: ")
	for j in range(wsn_graph[i].getNumOfNeighbors()):
		print("[" + wsn_graph[i].neighbors[j].getID() + "]")

print("")

dominating_sets=Domatic_Partition(wsn_graph,int(num_of_nodes))
prGreen("=====================")
prGreen("## Dominating Sets ##")
for i in range(len(dominating_sets)):
	prGreen("D("+str(i)+"):")
	prGreen(dominating_sets[i])
prGreen("=====================")

for i in range(int(num_of_nodes)):
	wsn_graph[i].setEnergy(random.random())

for i in range(int(num_of_nodes)):
	prRed("["+wsn_graph[i].getID()+"] <-->[ENERGY]:"+str(wsn_graph[i].getEnergy()))
	
## Local Search Algorithm implementation ##
for i in range(len(dominating_sets)): ## examine each Dominating Set ##
	for j in range(len(dominating_sets[i])): ## examine each node of the Dominating Set ##
		node_for_change=dominating_sets[i][j]
		for k in range(i+1,len(dominating_sets)): ## examine the other Dominating Sets ##
			for l in range(len(dominating_sets[k])): ## examine each node and start swaps ##
				temp_DS1=dominating_sets[i].copy()
				temp_DS2=dominating_sets[k].copy() ## temp_DS1 and temp_DS2 are the DS at which we will try to change nodes ##
				energy_list1=[]
				energy_list2=[]
				temp_energy_list1=[]
				temp_energy_list2=[]
				for r in range(len(temp_DS1)):
					for p in range(int(num_of_nodes)):
						if(temp_DS1[r]==wsn_graph[p].getID()):
							energy_list1.append(wsn_graph[p].getEnergy())
						#endif
					#endfor
				#endfor
				for r in range(len(temp_DS2)):
					for p in range(int(num_of_nodes)):
						if(temp_DS2[r]==wsn_graph[p].getID()):
							energy_list2.append(wsn_graph[p].getEnergy())
						#endif
					#endfor
				#endfor
				temp=temp_DS1[j]
				temp_DS1[j]=temp_DS2[l]
				temp_DS2[l]=temp
				for r in range(len(temp_DS1)):
					for p in range(int(num_of_nodes)):
						if(temp_DS1[r]==wsn_graph[p].getID()):
							temp_energy_list1.append(wsn_graph[p].getEnergy())
						#endif
					#endfor
				#endfor
				for r in range(len(temp_DS2)):
					for p in range(int(num_of_nodes)):
						if(temp_DS2[r]==wsn_graph[p].getID()):
							energy_list2.append(wsn_graph[p].getEnergy())
						#endif
					#endfor
				#endfor
				print("=== New Temporary Dominating Sets ===")
				print(temp_DS1)
				print(temp_DS2)
				all_nodes_are_dominated=0
				neighbor_not_found=0
				for n in range(int(num_of_nodes)): # traverse the whole Sensor Network #
					domination_flag=0
					for m in range(len(temp_DS1)): # check if they have a neighbor which belongs to temp_DS #
						if(wsn_graph[n].getID()!=temp_DS1[m]):
							ret_val=wsn_graph[n].isMyNeighbor(temp_DS1[m])
							if (ret_val==1):
								all_nodes_are_dominated=all_nodes_are_dominated+1
								domination_flag=1
								break
							#endif#
							else:
								neighbor_not_found=neighbor_not_found+1
							#endelse#
						else:
							all_nodes_are_dominated=all_nodes_are_dominated+1
						#endelse#
					#endfor#
					if(neighbor_not_found==len(temp_DS1)):
						print("--> Swap "+dominating_sets[i][j]+" with "+dominating_sets[k][l]+".")
						print("--> Cancel Swap")
						print(temp_DS1)
						print("is not a Dominating Set")
						print("")
						print("")
						time.sleep(1)
						break # Cancel the Swap and move on to perform a different Swap #
					#endif#
				#endfor#
				if(all_nodes_are_dominated==int(num_of_nodes)): # temp_DS1 is Dominating Set .The same procedure must be made for temp_DS2 #
					all_nodes_are_dominated=0
					neighbor_not_found=0
					for n in range(int(num_of_nodes)): # traverse the whole Sensor Network #
						domination_flag=0
						for m in range(len(temp_DS2)): # check if they have a neighbor which belongs to temp_DS #
							if(wsn_graph[n].getID()!=temp_DS2[m]):
								ret_val=wsn_graph[n].isMyNeighbor(temp_DS2[m])
								if (ret_val==1):
									all_nodes_are_dominated=all_nodes_are_dominated+1
									domination_flag=1
									break
								#endif#
								else:
									neighbor_not_found=neighbor_not_found+1
								#endelse#
							#endif#
							else:
								all_nodes_are_dominated=all_nodes_are_dominated+1
							#endelse#
						#endfor#
						if(neighbor_not_found==len(temp_DS2)):
							print("--> Swap "+dominating_sets[i][j]+" with "+dominating_sets[k][l]+".")
							print("--> Cancel Swap")
							print(temp_DS2)
							print("is not a Dominating Set")
							break # Cancel the Swap and move on to perform a different Swap #
						#endif#
					#endfor#
					if(all_nodes_are_dominated==int(num_of_nodes)): # temp_DS2 is also a Dominating Set.Now we must make an total_lifetime check.
						print("===Energy Check===")
						min_enrg1=min(energy_list1)
						min_enrg2=min(energy_list2)
						temp_min1=min(temp_energy_list1)
						temp_min2=min(temp_energy_list2)
						sum=min_enrg1+min_enrg2
						temp_sum=temp_min1+temp_min2
						if(sum<temp_sum):
							print("=== MAKE SWAPS PERMANENT ===")
						#endif
						else:
							print("=== Cancel Swaps ===")
						#endelse
					#endif#
				#endif# # end of checking if temp_DS2 is a Dominating Set #
			#endfor#
		#endfor#
	#endfor#
#endfor#
# End of Local Search Algorithm #
## end of main programm ##
