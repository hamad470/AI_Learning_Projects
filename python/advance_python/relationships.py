
# AGGREGATION RELATIONSHIP

class A:

    def __init__(self) -> None:
        self.name  = "A"
        pass
    def relation(self , b):
        self.b = b

        print("Relation Method: ",b.name_of_class)

    def name_of_current_class(self):
        print(self.name)


class B:
    def __init__(self) -> None:
        self.name_of_class = "B"
    def name(self):
        print("Name of this class is class B")






class Car:

    def __init__(self,engine):
        engine.number
        print(engine.number)

    def drive(self):
        print(" PLEASE START CAR's ENGINE ...")    

    def __private_method(self):
        print("mangliing Relation")    




class Engine:

    def __init__(self):
        self.number = "123"

engine = Engine()

car = Car(engine)
car.drive()
car._Car__private_method()




