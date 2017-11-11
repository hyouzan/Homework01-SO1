import math

class SchedulerSimulator:
	#.append(e) e non add per aggiunere
	def __init__(self,q,m):
		self.quantum = q
		self.max_procs = m
		self.time = 0
		self.counter = 0
		self.tempQ = q
		self.ready_queue = []
		self.blocked_queue = []
		self.temp_queue = []
		# self.file = f;
		self.newBlocked = []

	def advance_time(self, t):
		ready_queue = self.ready_queue
		blocked_queue = self.blocked_queue
		time = self.time
		quantum = self.quantum
		tempQ = self.tempQ
		temp_queue = self.temp_queue 
		newBlocked = self.newBlocked 
		

		
		intervallo = 0.1 
		# HO NOTATO CHE MI ARRIVANO VALORI TIPO 0.599999999 O 2.6000000001
		# CON 0.599999999 NON C'ERA PROBLEMA FINO ALLA N ESIMA CIFRA DECIMALE PERCHE IL VALORE DOPO 0.1 ERA NEGATIVO ED NON ENTRVA NELL IF DI SOTTO
		# SICCOME INVECE QUANDO VEDE QUEL 0.0000000001 CHE RIMANE LEVANDO 26 VOLTE 0.1 ME LO CONTA COME LA 27 VOLTA E NON DOVREBBE
		# ALLORA HO ARROTONDATO A 2 CIFRE IN MODO DA AVERE 0.59 E 2.60 CHE CICLA PERFETTAMENTE ANCHE SU T=2.6
		# DOVREBBE FUNZIONARE FINO ALLA 5 O 6 CIFRA DOPO LA VIRGOLA SE NON HO FATTO MALE IL RAGIONAMENTO

		t = round(t, 2)
		n_intervallo = math.ceil(t / intervallo)
		#self.printone("\n" + str(t) + "\n")
		lenBlock = len(blocked_queue)

		# TOLGO 0.1 ALLA VOLTA TEMPO 
		for i in range(n_intervallo):

			#SE LA READY QUEUE E VUOTA METTO I BLOCCATI IN ATTESA DIRETTAMENTE NELLA READY QUEUE
			if(len(ready_queue) == 0):
				if(len(temp_queue)!= 0):
					for item in range(len(temp_queue)):

						illreback = temp_queue[item]
						illreback["code_io"] = illreback["code_io"][1:]
						ready_queue.append(illreback)

						for x in range(len(blocked_queue)):
							if(temp_queue[item]["pid"] != blocked_queue[x]["pid"]):
								newBlocked.append(blocked_queue[x])
						blocked_queue = newBlocked
						newBlocked = []
					temp_queue = []

				#self.printone("\n BLOCKED" + str(blocked_queue) + "\n")
				if(len(blocked_queue) != 0):

					for y in range(len(blocked_queue)):
						if(blocked_queue[y]["code_io"][0] == 0):

							illreturn = blocked_queue[y]
							illreturn["code_io"] = illreturn["code_io"][1:]
							ready_queue.append(illreturn)
							#self.printone("\n HELLO QUI \n")
						else:
							newBlocked.append(blocked_queue[y])	
					blocked_queue = newBlocked
					newBlocked = []

			# TEMPQ E IL MIO TEMPO INTERNO ALLO SCHEDULER
			# QUANDO E ESAURITO VUOL DIRE CHE IL PROCESSO HA USATO TUTTO IL SUO TEMPO
			if(tempQ <= 0):
				#self.printone("\n FINE MIO QUANTUM \n")
				if(len(ready_queue) != 0):
					golast = ready_queue[0]
					ready_queue = ready_queue[1:]
					ready_queue.append(golast)	
				tempQ = quantum


				# SE CI SONO PROCESSI IN ATTESA DI ANDARE TRA I READY ENTRA IN QUESTO IF
				if(len(temp_queue)!= 0):
					# OGNI PROCESSO IN ATTESA NELLA TEMP QUEUE VIENE MESSO IN READY
					for item in range(len(temp_queue)):

						illreback = temp_queue[item]
						illreback["code_io"] = illreback["code_io"][1:]
						ready_queue.append(illreback)
						# I PROCESSI MESSI IN READY VANNO FUORI DALLA BLOCKED
						# LA TEMP QUEUE E SOLO AI FINI DEL CODICE INFATTI I PROCESSI IN ATTESA SONO COMUNQUE NELLA BLOCKED
						# E VENGONO TOLTI SOLO AL MOMENTO DELLA MESSA IN READY
						for x in range(len(blocked_queue)):
							if(temp_queue[item]["pid"] != blocked_queue[x]["pid"]):
								newBlocked.append(blocked_queue[x])
						blocked_queue = newBlocked
						newBlocked = []
					temp_queue = []

				# SE CI SONO PROCESSI CHE DEVONO ANDARE IN READY MA NON HANNO FATTO IN TEMPO A FINIRE NELLA TEMP
				if(len(blocked_queue) != 0):

					for y in range(len(blocked_queue)):
						if(blocked_queue[y]["code_io"][0] == 0):

							illreturn = blocked_queue[y]
							illreturn["code_io"] = illreturn["code_io"][1:]
							ready_queue.append(illreturn)
							#self.printone("\n HELLO QUI \n")
						else:
							newBlocked.append(blocked_queue[y])	
					blocked_queue = newBlocked
					newBlocked = []


			# SE LA READY QUEUE HA ELEMENTI ENTRO QUI
			if len(ready_queue) != 0:
				# SE IL TEMPO DEL PROCESSO NON HA RAGGIUNTO LO 0 CONTINUO A TOGLIERE 0.1 (FRAMMENTI DI INTERVALLO)
				if ready_queue[0]["code_io"][0] > 0:
					ready_queue[0]["code_io"][0] = ready_queue[0]["code_io"][0] - intervallo
					ready_queue[0]["code_io"][0] = round(ready_queue[0]["code_io"][0], 1)

				else: 
					# SE OLTRE AL TEMPO DEL PROCESSO HO DEI TEMPI DI I0 ENTRO QUI E MANDO IL PROCESSO IN BLOCKED
					# USO IL FATTO CHE NELLE POSIZIONI DISPARI CI SONO I TEMPI DI CPU E LO USO COME CONTROLLO 
					if( (len(ready_queue[0]["code_io"]) % 2) != 0 and len(ready_queue[0]["code_io"]) > 1):
						goblocked = ready_queue[0]
						goblocked["code_io"] = goblocked["code_io"][1:]
						ready_queue = ready_queue[1:]
						blocked_queue.append(goblocked)
						# TOLGO IL FRAMMENTO 0.1 AL PROCESSO CHE VA IN READY E FACCIO SCATTARE UN NUOVO QUANTO PER IL PROCESSO CHE ENTRA
						if len(ready_queue) != 0:
							ready_queue[0]["code_io"][0] = ready_queue[0]["code_io"][0] - intervallo
							ready_queue[0]["code_io"][0] = round(ready_queue[0]["code_io"][0], 1)
						tempQ = quantum

					else:
						# SE IL PROCESSO HA FINITO TUTTE LE SUE OPERAZIONE IO E CPU ESCE DALLA READY QUEUE
						# FACCIO PARTIRE IL NUOVO QUANTO SE CI STA UN ALTRO PROCESSO
						ready_queue = ready_queue[1:]
						if len(ready_queue) != 0:
							ready_queue[0]["code_io"][0] = ready_queue[0]["code_io"][0] - intervallo
							ready_queue[0]["code_io"][0] = round(ready_queue[0]["code_io"][0], 1)
						tempQ = quantum 
				# DIMINUISCO IL TEMPO DEL MIO SCHEDULER DI 0.1
				tempQ -= intervallo
				tempQ = round(tempQ, 1)
			
			else:
				# ENTRO QUI SE LA LISTA E VUOTA
				# MAGARI CI SONO PROCESSI IN BLOCKED QUINDI DEVO COMUNQUE FAR SCORRERE IL TEMPO
				tempQ -= intervallo
				tempQ = round(tempQ, 1)

			trovato = False

			# GESTIONE DEI BLOCKED
			if(len(blocked_queue) != 0):
				
				#self.printone("\n TEMPORARY" + str(temp_queue) + "\n")
				for j in range(len(blocked_queue)):
					# LEVO 0.1 AD OGNI PROCESSO IN BLOCKED CHE STA FACENDO I SUOI IO
					# SE STO IN POSIZIONE PARI SULLAL LISTA E NON HA FINITO IL TEMPO DI I0 DECREMENTO IL VALORE
					if blocked_queue[j]["code_io"][0] > 0 and len(blocked_queue[j]["code_io"]) % 2 == 0:
						blocked_queue[j]["code_io"][0] = blocked_queue[j]["code_io"][0] - intervallo
						blocked_queue[j]["code_io"][0] = round(blocked_queue[j]["code_io"][0], 1)
					# ALTRIMENTI HO FINITO
					else:

						# METTO IL PROCESSO CONCLUSO IN UNA TEMP QUEUE PARALLELA ALLA BLOCKED CHE CONTIENE I PROCESSI CHE HANNO FINITO
						# COSI CONTINUO A LAVORARE SULLA BLOCKED CON L IF DI SOPRA
						illbeback = blocked_queue[j]
						# vecchia prova in caso la rimetto per fare prove illbeback["code_io"] = illbeback["code_io"][1:]

						# SE HO GIA DEGLI ELEMENTI NELLA TEMP NON VOGLIO RI AGGIUNGERLO QUANTUM-QUANTUMRIMANENTE VOLTE 
						# QUINDI VERIFICO SE L ELEMENTO E GIA IN TEMP QUEUE E SE LO E IGNORO QUESTO PASSAGGIO
						# LA TEMP QUEUE VERRA ANALIZZATA ALAL FINE DEL QUANTO DEL MIO SIMULATORE 
						# LA HO UTILIZZATA PERCHE NON DEVO AGGIUNGERE NELLA READY QUEUE MENTRE IL PROCESSORE STA LAVORANDO
						# COME MI E SEMBRATO DI DEDURRE DALLE STAMPE NELLA CARTELLA CHECK

						if(len(temp_queue) != 0):
							for k in range(len(temp_queue)):
								if(illbeback["pid"] == temp_queue[k]["pid"]):
									trovato = True
							if(not trovato):
								temp_queue.append(illbeback)
								trovato = False
						else:
							temp_queue.append(illbeback)		



		
		
		self.temp_queue = temp_queue
		self.tempQ = tempQ
		self.ready_queue = ready_queue
		self.blocked_queue = blocked_queue
		self.time = time
		self.quantum = quantum
		self.newBlocked = newBlocked


	def add_proc(self, code_io): 
		# aggiunge un nuovo processo ready nel tempo del simualtore
		ready_queue = self.ready_queue
		counter = self.counter
		time = self.time

		# SE POSSO ANCORA AGGIUNGERE
		if counter < self.max_procs:
			pid = counter +1
			# dictio = {'code_io': code_io[counter], 'pid' : pid}
			# AGGIUNGO UN DIZIONARIO DI 2 ELEMENTI A READY QUEUE
			ready_queue.append({'code_io': code_io, 'pid' : pid})
		else:
			# SE NON POSSO METTO NONE
			pid = None
		counter = counter + 1

		self.ready_queue = ready_queue
		self.counter = counter
		self.time = time
		return pid

	# METODO DI STAMPA 						
	# def printone(self,arg):
	#	self.file.write(str(arg))	

	# METODI GET PER LE QUEUE
	def get_ready(self):
		#ritorna la lista dei processi nella coda ready
		return self.ready_queue[1:]

	def get_blocked(self): 
		#ritorna la lista dei processi blocked
		return self.blocked_queue
			
	# PRIMO DELLA LISTA READY
	def get_running(self):
		#ritorna il processo in esecuzione con pid e code_io
		if(len(self.ready_queue)!=0):
			return self.ready_queue[0]
