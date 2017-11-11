import math 
class MemorySimulator:
	def __init__(self,M,Mp,S,P,l ,f):
		self.Memoria = M
		self.MemoriaUtente = Mp
		self.bMemSecondaria = S
		self.Pagina = P
		self.listaproc = l
		self.file = f
		self.memFrame = []
		self.pageHit = 0
		self.pageMiss = 0
		self.counter = 0
		if(len(l) == 1):
			n = l[0]
			for i in range(n):
				self.memFrame.append((None,  0))
		else:
			pass



	def printone(self,arg):
		self.file.write(str(arg))

	def handle_request(self, addr, i):
		M = self.memFrame
		P =self.Pagina
		#pageMiss = self.pageMiss
		#pointer = self.pointer
		counter = self.counter
		Miss = False
		Hit = False 

		indprof = 0
		pageNum = int(addr / P)
		offset = addr - int(pageNum * P)

		
		tryins = (pageNum , 0)
		#CALCOLARE NUMERO DI MERDA

		if(counter < len(M)):

			for x in range(len(M)):
				if M[x][0] == pageNum and Hit is False:
					self.pageHit += 1
					Hit = True
				if M[x][0] == None and Miss is False and Hit is False:
					#self.printone("\n" + str(pageMiss) + "\n")
					M[x] = (pageNum, i)
					self.pageMiss = self.pageMiss + 1
					Miss = True	
					#self.printone("\n" + str(self.pageMiss) + "\n")
		else:
			pass
				# orologio CON POINTER LISTA DI 100 TRA 0 E 1
		
	
				


		return 0 , pageNum 
		
		self.counter = counter
		self.Pagina = P	
		self.memFrame = M


	def get_memory(self):
		return self.memFrame

	def get_stats(self):
		return 1000, self.pageMiss
