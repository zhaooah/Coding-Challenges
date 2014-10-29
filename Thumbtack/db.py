
import sys
import copy

class tDatabase:

	def __init__(self):

		#data storage and value counter
		self._db = {}
		self._valFreq = {}


		#data storage and value counter for transaction block
		#Stacks store recent transaction states
		self._blocks = []		
		self._blocks_valFreq = []		



	def _write(self,db,valFreq,key,val):

		#If key exists, but has different value,
		#decrement value counter
		if (key in db) and (val!=db[key]):

			valFreq[db[key]]-=1

			if valFreq[db[key]]==0:

				valFreq.pop(db[key])

		#Increment value counter
		if val in valFreq:

			valFreq[val]+=1

		else:

			valFreq[val]=1

		#Set key value pair
		db[key]=val




	def _read(self,source,key):


		if key not in source:

			return 'NULL'

		else:

			return source[key]


	def _delete(self,source,valFreq,key):


		if key in source:

			val=source[key]

			source.pop(key)

			#Decrement value counter

			valFreq[val] -= 1

			if valFreq[val]==0:

				valFreq.pop(val)
 
		else:

			print 'NULL'


	def _readValFreq(self,source,key):

		if key in source:

			print source[key]

		else:

			print 0


	def set(self, key, val):

		#Check if there is opening transaction block
		if not self._blocks:

			#Write data to data storage
			self._write(self._db,self._valFreq,key,val)

		else:

			#For opening block, write data to state buffer
			self._write(self._blocks[0],self._blocks_valFreq[0],key,val)





	def get(self, key):

		if not self._blocks:

			print self._read(self._db,key)

		else:

			print self._read(self._blocks[0],key)



	def unset(self, key ):

		if not self._blocks:

			self._delete(self._db,self._valFreq,key)

		else:

			self._delete(self._blocks[0],self._blocks_valFreq[0],key)




	def numequalto(self, key):

		if not self._blocks:

			self._readValFreq(self._valFreq,key)

		else:

			self._readValFreq(self._blocks_valFreq[0],key)



	def rollback(self):

		#Check if sif there is transaction in progress

		if not self._blocks:

			print 'NO TRANSACTION'

		else:

			self._blocks.pop(0)

			self._blocks_valFreq.pop(0)




	def begin(self):

		if not self._blocks:

			#If transaction state buffer is empty,
			#push a shallow copy (reference) of database,
			#copy item only when it is needed to be modified

			self._blocks.insert(0,{})

			self._blocks[0]=copy.copy(self._db)

			self._blocks_valFreq.insert(0,{})

			self._blocks_valFreq[0]=copy.copy(self._valFreq)


		else:

			#If transaction state buffer is not empty,
			#push a shallow copy (reference) of last transaction block

			self._blocks.insert(0,{})

			self._blocks[0]=copy.copy(self._blocks[1])


			self._blocks_valFreq.insert(0,{})			

			self._blocks_valFreq[0]=copy.copy(self._blocks_valFreq[1])




	def commit(self):

		if not self._blocks:

			print 'NO TRANSACTION'

		else:
				#Insert state buffer to database

				self._db=dict(self._db.items() + self._blocks[0].items())

				self._valFreq=dict(self._valFreq.items() + self._blocks_valFreq[0].items())

				self._blocks=[]

				self._blocks_valFreq=[]



if __name__ == "__main__":

	tDB=tDatabase()

	commandDict= {
		
		# { command : [ function, number of arguments ] }

		'SET': [tDB.set,2],
		'GET':	[tDB.get,1],
		'UNSET': [tDB.unset,1],
		'NUMEQUALTO': [tDB.numequalto,1],
		'BEGIN': [tDB.begin,0],
		'ROLLBACK': [tDB.rollback,0],
		'COMMIT': [tDB.commit,0]

	}



	while True:

		userInput = sys.stdin.readline().strip().split(' ')

		command = userInput[0]

		args = userInput[1:]

		if command == 'END':

			sys.exit()

		if command in commandDict:

			if len(args) == commandDict[command][1]:

					commandDict[command][0](*args)

			else:

				print 'Wrong number of arguments'

		else:
				print 'Invalid command'








