from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbcreation import Base, Models, Parts, Processes


C1dict = {"P1":12,"P2":4,"P5":5,"P6":7,"P10":1}
C2dict = {"P1":12,"P2":6,"P6":5,"P8":9,"P10":1}
C3dict = {"P1":12,"P2":7,"P5":5,"P7":15,"P9":4}
C4dict = {"P3":3,"P4":6,"P7":13,"P8":9,"P10":1}
C5dict = {"P3":3,"P4":6,"P7":18}
C6dict = {"P3":3,"P4":4,"P8":10,"P9":5}
C7dict = {"P5":8,"P6":8,"P9":5}

def Main():  

	#===##===##===##===##===##===##===#
	#Connection to SQLITE DB 
	#===##===##===##===##===##===##===#
	engine = create_engine('sqlite:///complete.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()

	#===##===##===##===##===##===##===#
	#Removal of all current entries  
	#===##===##===##===##===##===##===#

	removeParts = session.query(Parts).all()
	removeModels = session.query(Models).all()
	removeProcesses = session.query(Processes).all()

	for r in removeParts: 
		session.delete(r)
		session.commit()

	for r in removeModels: 
		session.delete(r)
		session.commit()

	for r in removeProcesses: 
		session.delete(r)
		session.commit()

	#===##===##===##===##===##===##===#
	#Populate database 
	#===##===##===##===##===##===##===#

	M1 = Models(name = 'M1', parts="P1,P2,P3,P4,P5")
	M2 = Models(name = 'M2', parts="P1,P3,P6,P8,P9")
	M3 = Models(name = 'M3', parts="P1,P2,P8,P9,P10")
	M4 = Models(name = 'M4', parts="P1,P4,P5,P7,P9")

	P1 = Parts(name = 'P1',processes="C1,C2,C3")
	P2 = Parts(name = 'P2',processes="C1,C2,C3")
	P3 = Parts(name = 'P3',processes="C4,C5,C6")
	P4 = Parts(name = 'P4',processes="C4,C5,C6")
	P5 = Parts(name = 'P5',processes="C1,C3,C7")
	P6 = Parts(name = 'P6',processes="C1,C2,C7")
	P7 = Parts(name = 'P7',processes="C3,C4,C5")
	P8 = Parts(name = 'P8',processes="C2,C4,C6")
	P9 = Parts(name = 'P9',processes="C3,C6,C7")
	P10 = Parts(name = 'P10',processes="C1,C2,C4")

	C1 = Processes(name='C1')
	C2 = Processes(name='C2')
	C3 = Processes(name='C3')
	C4 = Processes(name='C4')
	C5 = Processes(name='C5')
	C6 = Processes(name='C6')
	C7 = Processes(name='C7')

	session.add(M1)
	session.add(M2)
	session.add(M3)
	session.add(M4,M1)

	session.add(P1)
	session.add(P2)
	session.add(P3)
	session.add(P4)
	session.add(P5)
	session.add(P6)
	session.add(P7)
	session.add(P8)
	session.add(P9)
	session.add(P10)

	session.add(C1)
	session.add(C2)
	session.add(C3)
	session.add(C4)
	session.add(C5)
	session.add(C6)
	session.add(C7)	

	session.commit()
 
if __name__ == '__main__': 
	Main() 