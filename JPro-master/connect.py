from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbcreation import Base, Models, ProductionQueue

productiontimes = {"C1":{"P1":12,"P2":4,"P5":5,"P6":7,"P10":1},
										"C2":{"P1":12,"P2":6,"P6":5,"P8":9,"P10":1}, 
										"C3":{"P1":12,"P2":7,"P5":5,"P7":15,"P9":4},
										"C4":{"P3":3,"P4":6,"P7":13,"P8":9,"P10":1},
										"C5":{"P3":3,"P4":6,"P7":18},
										"C6":{"P3":3,"P4":4,"P8":10,"P9":5},
										"C7":{"P5":8,"P6":8,"P9":5},
}

class Connect():  
	#===##===##===##===##===##===##===#
	#Connection to SQLITE DB 
	#===##===##===##===##===##===##===#
	def __init__(self):
		self.engine = create_engine('sqlite:///complete.db')
		Base.metadata.bind = self.engine
		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()
	print ('Connected to database')

	#===##===##===##===##===##===##===#
	#Methods   
	#===##===##===##===##===##===##===#

#	print(session.query(ProductionQueue).first().model)	
#	def getTime(part, process): 
#		print("ProductionTime is: ", productiontimes[process][part])
#		return
	
#	print (getTime('P5','C7'))
